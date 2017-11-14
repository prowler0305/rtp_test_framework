package com.ca.rtp.core.os;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.io.InputStream;

/**
 * Execute a os command.
 * Created by bergr05 on 3/1/2016.
 */
public class Command {

    // Get a logger
    private static final Logger log = LogManager.getLogger(Command.class);

    /**
     * Execute an os command.
     * @param command The host os command to execute.
     * @return String
     */
    public static String execute(String command) throws RtpException{
        Runtime rt = Runtime.getRuntime();
        StringBuilder sb = new StringBuilder();

        // Create a new process to execute the command.
        Process ps;
        try {
            ps = rt.exec(command);

        } catch (IOException e) {
            throw new RtpException("Error executing command:" + command, e);
        }

        // Read the result of the command.
        InputStream is = ps.getInputStream();
        try {
            if (ps.waitFor() == 0) {
                int a = is.read();

                while (a != -1) {
                    sb.append((char) a);
                    a = is.read();
                }
            }
        } catch (IOException e) {
            throw new RtpException("Error executing command:" + command, e);
        } catch (InterruptedException ie) {
            throw new RtpException("Error executing command:" + command, ie);
        } finally {
            try {
                is.close();
            } catch (IOException ioe) {
                log.error("Error closing file. \n Trace: {}", ExceptionUtilities.stacktraceToString(ioe));
            }
            ps.destroy();
        }

        return sb.toString();
    }
}
