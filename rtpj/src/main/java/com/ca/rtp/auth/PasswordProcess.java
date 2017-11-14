//package com.ca.rtp.auth;
//
//import com.ca.rtp.core.utilities.ExceptionUtilities;
//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;
//
//import java.io.IOException;
//import java.io.InputStream;
//
///**
// * Created by bergr05 on 3/1/2016.
// */
//class PasswordProcess {
//
//    private static final Logger log = LogManager.getLogger(PasswordProcess.class);
//
//    /**
//     * Execute the ptg-auth command to retrieve the user's password from the local machine store.
//     * This function requires that the PTG2 python framework be installed on the machine executing this
//     * routine.
//     * @param command The PTG2 command to execute.
//     * @return String
//     */
//    public static String execute(String command) {
//        Runtime rt = Runtime.getRuntime();
//        Process ps = null;
//        StringBuilder sb = new StringBuilder();
//
//        try {
//            ps = rt.exec(command);
//            InputStream is = ps.getInputStream();
//
//            if (ps.waitFor() == 0) {
//                int a = is.read();
//
//                while (a != -1) {
//                    sb.append((char) a);
//                    a = is.read();
//                }
//            }
//        } catch (IOException e) {
//            log.error("{}", ExceptionUtilities.stacktraceToString(e));
//        } catch (InterruptedException ie) {
//            log.error("{}", ExceptionUtilities.stacktraceToString(ie));
//        }
//        finally {
//            if(ps != null) {
//                ps.destroy();
//            }
//        }
//
//        return parsePassword(sb.toString().trim(), command);
//    }
//
//    /**
//     * Parse the password from the returned command output.
//     * @param output The result of the command.
//     * @return String
//     */
//     static String parsePassword(String output, String command) {
//        String password;
//
//        int lastNewLine = output.lastIndexOf("\n");
//        if(lastNewLine != -1){
//            password = output.substring(lastNewLine+1, output.length());
//        } else {
//            password = output;
//        }
//
//        // TODO: remove this and remove the string command from the function call.
//        if(command.contains("QADBA01")) {
//         log.info("Password Command: {}", command);
//         log.info("Password Result: {} ", output);
//         log.info("Password {}", password);
//        }
//
//        return password;
//    }
//
//}
