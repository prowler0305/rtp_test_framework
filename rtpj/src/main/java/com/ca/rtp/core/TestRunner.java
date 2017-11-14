package com.ca.rtp.core;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by bergr05 on 2/25/2016.
 */
public class TestRunner {

    // Get a logger
    private static final Logger log = LogManager.getLogger(TestRunner.class);

    public static void main (String args[]) {

        log.info("******************************");
        log.info("*      RTP Test Runner       *");
        log.info("******************************");

        if (args.length == 0) {
            log.fatal("No Tests Found. Tests must be passed as arguments.");
            log.info("Example: java -jar jarFile.jar test1 test2 test3");
            System.exit(0);
        }

        boolean result = false;

        final String failed = "*** TEST FAILED *** ";
        final String passed = "*** TEST PASSED *** ";
        final String skipped = "*** TEST SKIPPED *** ";
        final String running = "*** RUNNING TEST *** ";

        final String pkg = "com.ca.rtp.tests.%s";

        ArrayList<String> testParms = new ArrayList<>();
        ArrayList<String> tests = new ArrayList<>();
        HashMap<String, String> testArgs;

        for (String name: args) {
            if (name.startsWith("--")) {
                testParms.add(name);
            } else {
                tests.add(name);
            }
        }

        testArgs = parseArguments(testParms);


        for (String name : tests) {

            Object test;
            name = String.format(pkg,name);

            try {
                Class<?> testClass = Class.forName(name);
                test = testClass.newInstance();
            } catch (ClassNotFoundException cnf) {
                log.error(skipped + "The class: " + name + " was not found. ");
                log.info("Tests must be located in the package 'com.ca.rtp.tests'");
                TestTracker.upSkipped(name, "The class was not found.");
                continue;
            } catch (InstantiationException ie) {
                log.error(skipped + "The class: " + name + " could not be instantiated. " + ie.getMessage());
                TestTracker.upSkipped(name, "The class could not be instantiated.");
                continue;
            } catch (IllegalAccessException ia) {
                log.error(skipped + "The class: " + name + " could not be instantiated. " + ia.getMessage());
                TestTracker.upSkipped(name, "The class could not be instantiated.");
                continue;
            }

            if (test instanceof RtpTest) {
                log.info(running + name);

                try {
                    result = ((RtpTest) test).invoke(testArgs);
                } catch (Exception e) {
                    log.error(failed + " Trace: {}", ExceptionUtilities.stacktraceToString(e));
                    TestTracker.upFailed(name, e.getMessage());
                    continue;
                }

                if(!result) {
                    log.info(failed + name);
                    TestTracker.upFailed(name, "");
                } else {
                    log.info(passed + name);
                    TestTracker.upPassed();
                }

            } else {
                log.error(skipped + name + " does not implement the RtpTest interface.");
                TestTracker.upSkipped(name, "The test does not implement the RtpTest interface.");
            }
         }

        log.info("");
        if(!result) {
            log.info("Final Result: FAILED");
            log.info(TestTracker.toStringFormatted());
            System.exit(-1);
        } else {
            log.info("Final Result: PASSED");
            log.info(TestTracker.toStringFormatted());
            System.exit(0);
        }
    }

    /**
     * Process all parameters for the tests.  Add them to a hashmap and return the map.
     *
     * Example: --SSID=DD0G
     * Key: SSID Value: DD0G
     *
     * @param parms input parameters
     * @return HashMap
     */
    private static HashMap<String, String> parseArguments(ArrayList<String> parms) {
        HashMap<String, String> args = new HashMap<>();
        for (String parm : parms) {

            String key = parseKey(parm);
            String value = parseValue(parm);

            System.out.println("Parm: " + parm);
            if (key.startsWith("SSID")) {
                value = value.toUpperCase();

                if (value.length() > 4 ) {
                    System.out.println("Error: SSID is not valid." + value);
                    value = "";
                }
                args.put(key,value);

            } else if (key.equals("USERID")) {
                value = value.toUpperCase();
                if (value.length() > 8) {
                    System.out.println("Error: USERID is not valid." + value);
                    value = "";
                }
                args.put(key, value);
            } else {
                  args.put(key, value);
            }
        }

        return args;
    }

    private static String parseKey(String arg) {
        return arg.substring(arg.indexOf("--")+2, arg.indexOf("="));
    }

    private static String parseValue(String arg) {
        return arg.substring(arg.indexOf("=")+1);
    }

}
