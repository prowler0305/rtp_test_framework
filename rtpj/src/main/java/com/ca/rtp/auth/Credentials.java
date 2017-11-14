package com.ca.rtp.auth;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.os.Command;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedReader;
import java.io.Console;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * The Credentials objects contains the user id and encrpyted password for a user.
 * Created by bergr05 on 2/23/2016.
 */
public class Credentials {
    private static volatile boolean userPrompted = false;
    private volatile boolean sealed = false;
    private final String userid;
    private final Encryptor sealer;
    private final boolean ptg = true;

    private static final Logger log = LogManager.getLogger(Credentials.class);

    public Credentials(String userid) {
        this.userid = userid;
        this.sealer = new Encryptor();
    }

    /**
     * Gets the userid variable
     */
    public String getUserid(){
        return this.userid;
    }

    /**
     * The resetPassword method will delete a password from the store for a given system and user.
     * @param system System being accessed.
     * @param user User name
     * @return boolean
     */
    public synchronized boolean resetPassword (String system, String user) {
        String command = String.format("ptg-auth --system %s --userid %s --delete", system, user);
        try {
            Command.execute(command);
            CredentialsCache.remove(user);
            sealer.destroy();
            sealed = false;
            return true;
        } catch (Exception e) {
            log.error("Error resetting password for System: {} User: {} \n Trace: {}",
                    system, user, ExceptionUtilities.stacktraceToString(e));
            return false;
        }
    }

    /**
     * The setPassword method will save a new password to the store for a given system and user.
     * @param system System being accessed.
     * @param user User name
     * @return boolean
     */
    public synchronized boolean setPassword(String system, String user) {
        String command = String.format("ptg-auth --system %s --userid %s --prompt", system, user);
        try {
            Command.execute(command);
            sealer.destroy();
            sealed = false;
            return true;
        } catch (Exception e) {
            log.error("Error setting password for System: {} User: {} \n Trace: {}",
                    system, user, ExceptionUtilities.stacktraceToString(e));
            return false;
        }
    }

    /**
     * The getPassword method retrieves the password from the local store for the given system and user.  If the
     * password does not exist in the store, it will be requested from the user using a popup dialog.
     */
    public synchronized String getPassword(String system, String user) throws RtpException {

        if(sealed) {
            String sealedPass = Decryptor.unseal(sealer.getSealed(),sealer.getKey());
            return sealedPass;
        } else {
            String pw;
            String command = String.format("ptg-auth --system %s --userid %s", system, user);
            log.debug("Password command - " +  command);
            try {
                // Execute the PT2G command
                String output = Command.execute(command);

                if(user.equalsIgnoreCase("QADBA01")) { // Debug for common problems
                    log.debug("PTG2 Password Process Output: {}", output);
                }

                pw = parsePassword(output);
                if (pw.isEmpty()) {
                    setPassword(system, user);
                    pw = parsePassword(Command.execute(command));
                    if (pw.equals("")) {
                        log.warn("PTG2 auth service has failed to return the password.  Getting password from console.");
                        pw = getPasswordFromConsole();
                    }
                }

                sealer.seal(pw);
                sealed = true;

                return pw;
            } catch (RtpException rtpe1) {
                if(!userPrompted) {
                    String consolePassword;
                    try {
                        // Try to get the password from the user console.
                        consolePassword = getPasswordFromConsole();
                    } catch (RtpException rtpe2) {
                        // All password attempts have failed.  Print the first exception, then throw the last one.
                        rtpe1.print();
                        throw new CredentialsException("Error retrieving password for user: " + user, rtpe2);
                    } finally {
                        userPrompted = true;
                    }
                    sealer.seal(consolePassword);
                    sealed = true;
                    return consolePassword;
                }

                throw rtpe1;
            }
        }
    }

    /**
     * Parse the password from the returned command output.
     * @param output The result of the command.
     * @return String
     */
    private String parsePassword(String output) {
        if (output.isEmpty()) {
            return output;
        }
        String[] lines = output.split("\r?\n");

        for(String line : lines) {
            if (line.length() > 8 || line.length() < 4 ){
                continue;
            } else {
                return line.trim();
            }
        }
        return output;
    }

    /**
     * Get password from the user console.
     * @return String
     */
    private synchronized String getPasswordFromConsole() throws RtpException {
        String pass = "";

        log.info("Enter mainframe password: ");
        Console console = System.console();

        if (console != null) {
            pass = new String(console.readPassword("Password: "));
        } else {
            try {
                BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                pass = br.readLine();
                br.close();
            } catch (IOException e) {
                throw new RtpException("Error getting password from console.", e);
            }
        }

        return pass;
    }
}
