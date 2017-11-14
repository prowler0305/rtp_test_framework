package com.ca.rtp.core;

import com.ca.rtp.core.json.ExternalJsonTestReader;
import com.ca.rtp.core.json.JsonTest;
import com.ca.rtp.core.json.JsonTestReader;
import com.ca.rtp.core.json.JsonTestSuite;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.ca.rtp.core.utilities.RtpLogger;
import com.fasterxml.jackson.databind.JsonNode;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

/**
 * JsonTestRunner is the main entry point for the RTP JSON Test Suite.
 * Created by schke19 on 4/12/2016.
 */
public class JsonTestRunner {

    // Asynchronous logger initialization
    static {
        RtpLogger.init();
    }

    // Get a logger
    private static final Logger log = LogManager.getLogger(JsonTestRunner.class);

    /**
     * RTPJ Main entry point.
     * @param args String[]
     */
    public static void main (String args[]) {

        log.info(starLine());
        log.info("*    RTPJ JSON Test Runner    *");
        log.info(starLine());

        if (args.length == 0) {
            log.fatal("No Tests Found. Tests must be passed as arguments.");
            log.info("Example: java com.ca.rtp.core.JsonTestRunner test1.JSON test2.JSON");
            System.exit(0);
        }

        ArrayList<String> testParms = new ArrayList<>();
        ArrayList<String> tests = new ArrayList<>();

        // Process all execution arguments.
        for (String name : args) {
            if (name.startsWith("--")) {
                testParms.add(name);
            } else {
                tests.add(name);
            }
        }

        // Process optional command line arguments.
        HashMap<String, String> parms = new HashMap<>();
        try {
           parms = parseArguments(testParms);
        } catch (RtpException rtpe) {
            rtpe.print();
            log.fatal("Error processing input parameters, correct and restart the test.");
            System.exit(-1);
        }

        ConnectionInfo cInfoOverride;
        try {
            cInfoOverride = createCommandLineConnectionInfo(parms);
        } catch (RtpException rtpe) {
            rtpe.print();
            log.fatal("A problem was detected with the command line connection arguments. Aborting execution.");
            System.exit(-1);
            return;
        }

        String useridOverride = createCommandLineUserid(parms);

        // Start the test execution timer.
        TestTracker.timerStart();

        // Process all JSON Test files.
        for (String name : tests) {

            // Read a JSON Test File.
            log.info("Processing test file: {}", name);
            JsonTestReader testReader;
            if (parms.containsKey("LIBRARY")) {
                String path = parms.get("LIBRARY");
                testReader = new ExternalJsonTestReader(name, path);
            }
            else {
                testReader = new JsonTestReader(name);
            }

            JsonNode root;
            try {
                root = testReader.read();
            } catch (RtpException rtpe) {
                rtpe.print();
                TestTracker.upSkipped(name, rtpe.getMessage());
                continue;
            }

            // Check for a test suite
            JsonNode suite = root.path("suite");
            if (!suite.isMissingNode()) {
                executeTestSuite(suite, cInfoOverride, useridOverride, parms);
            } else {
                // Check for a file with a single test
                JsonNode testNode = root.path("test");
                if (!testNode.isMissingNode()) {
                    JsonTest test = new JsonTest(testNode, cInfoOverride, useridOverride, name);
                    try {
                        test.build();
                    } catch (RtpException rtpe) {
                        rtpe.print();
                        TestTracker.upSkipped(test.name, rtpe.getMessage());
                        log.info(TestTracker.toStringFormatted());
                        System.exit(-1);
                        return;
                    }
                    execute(test);
                }
                else {
                    log.error("JSON file {} does not contain a suite or test parameter.", name);
                    log.info("{} {}",TestTracker.SKIPPED_MSG, " - " + name);
                    TestTracker.upSkipped(name, "The JSON file does not contain a suite or test parameter.");
                }
            }
        }

        TestTracker.timerStop();

        if (TestTracker.getFailed() > 0 || TestTracker.getSkipped() > 0) {
            log.info("{}",TestTracker.toStringFormatted());
            System.exit(-1);
        } else {
            log.info("{}",TestTracker.toStringFormatted());
            System.exit(0);
        }
    }

    /**
     *  Execute a test suite
     */
    private static void executeTestSuite(JsonNode suite, ConnectionInfo cInfoOverride, String useridOverride, HashMap<String, String> parms) {
        JsonTestSuite testSuite;
        if (parms.containsKey("LIBRARY"))
            testSuite = new JsonTestSuite(suite, cInfoOverride, useridOverride, parms.get("LIBRARY"));
        else
            testSuite = new JsonTestSuite(suite, cInfoOverride, useridOverride);
        ArrayList<JsonTest> jsonTests;

        try {
            jsonTests = testSuite.build();
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }
        // TODO: multi threading at the tests object level.
        // Execute all tests within the test suite
        for(JsonTest test : jsonTests) {
            execute(test);
        }
    }

    /**
     * Execute a single JsonTest
     * @param test a JsonTest
     */
    private static void execute(JsonTest test) {
        try {
            log.info("{} - {} {SSID={} USERID={}} Description: {}",TestTracker.RUNNING_MSG, test.name, test.getConnectionInfo().getSSID(), test.getUserid(), test.getDescription());

            ArrayList<ThreadAndTest> threadsAndTests = new ArrayList<>();

            for (int i = 0; i < test.getThreadingInfo().threads; i++) {
                ThreadAndTest t = new ThreadAndTest(new JsonTestDriver(test.clone()));

                // Sleep between starting each thread.
                int sleep = test.getThreadingInfo().sleep;
                if (sleep> 0) {
                    log.debug("Sleeping for {} seconds before starting next thread.", sleep);
                    Thread.sleep(TimeUnit.SECONDS.toMillis(sleep));
                }

                t.getThread().start();
                threadsAndTests.add(t);

                // Check if test is to execute all threads in parallel.
                if(!test.getThreadingInfo().parallel)
                    t.getThread().join();

            }

            // If executing in parallel then wait for all threads to complete.
            if(test.getThreadingInfo().parallel) {
                for (ThreadAndTest t : threadsAndTests) {
                    t.getThread().join();
                }
            }

            for (ThreadAndTest t : threadsAndTests) {
                if(!t.getTestDriver().getTest().getFinalResult()) { // If any thread failed
                    TestTracker.upFailed(test.name, t.getTestDriver().getTest().getFailures()); // Mark test failed
                    log.error("{} {}",TestTracker.FAILED_MSG, " - " + test.name);
                    return; // No need to check rest of threads, skip rest of method
                }
            }

            // If we got here the test is considered passed because all drivers on all threads were marked as passed
            TestTracker.upPassed();
            log.info("{} - {}",TestTracker.PASSED_MSG, test.name);
        } catch (Exception e) {
            log.error("Exception executing a test: {} ", ExceptionUtilities.stacktraceToString(e));
            TestTracker.upFailed(test.name, e.getMessage());
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
    private static HashMap<String, String> parseArguments(ArrayList<String> parms) throws RtpException {

        String key;
        String value;
        HashMap<String, String> args = new HashMap<>();

        for (String parm : parms) {
            try {
                key = parseKey(parm);
                value = parseValue(parm);
            } catch (Exception e) {
                throw new RtpException("Error Parsing Input Parameter: " + parm);
            }

            log.debug("Parm: {} ", parm);
            if (key.equals("SSID")) {
                value = value.toUpperCase();

                if (value.length() > 4 ) {
                    log.error("Error: SSID is not valid. Value: {}", value);
                    value = "";
                }
                args.put(key,value);

            } else if (key.equals("USERID")) {
                value = value.toUpperCase();
                if (value.length() > 8) {
                    log.error("Error: USERID is not valid. Value: {}", value);
                    value = "";
                }
                args.put(key, value);
            } else if (key.equals("LOG")) {
                value = value.toUpperCase();
                RtpLogger.changeLevel(value);

            } else {
                  args.put(key, value);
            }
        }

        return args;
    }

    /**
     * Create connection information from the command line arguments
     * @param args HashMap<String, Strins>
     * @return ConnectionInfo
     */
    private static ConnectionInfo createCommandLineConnectionInfo(HashMap<String, String> args) throws RtpException {
        // Get the command line SSID
        if(args.containsKey("SSID")) {
            log.info("Processing command line SSID override.");
            ConnectionInfo cInfo = Subsystems.getConnectionInfo(args.get("SSID"));

            if (args.containsKey("LPAR")){
                log.info("Processing command line LPAR override.");
                cInfo = new ConnectionInfo(cInfo.getSSID(), args.get("LPAR"), cInfo.getPort());
            }
            return cInfo;
        }
        else {
            return JsonTest.DEFAULT_CONNECTION;
        }
    }

    /**
     * Create the userid information from the command line arguments
     * @param args HashMap
     * @return String
     */
    private static String createCommandLineUserid(HashMap<String, String> args) {
        // Get the command line userid
        if(args.containsKey("USERID")) {
            log.info("Processing command line USERID override.");
            return args.get("USERID");
        } else {
            return JsonTest.DEFAULT_USERID;
        }
    }

    private static String parseKey(String arg) {
        return arg.substring(arg.indexOf("--")+2, arg.indexOf("=")).toUpperCase();
    }

    private static String parseValue(String arg) {
        return arg.substring(arg.indexOf("=")+1);
    }

    public static String starLine() {
        return "*******************************";
    }

    private static class ThreadAndTest { //TODO: Come up with any kind of better name for this class
        Thread thread = null;
        JsonTestDriver test = null;

        ThreadAndTest(JsonTestDriver test) {
            this.test = test;
            this.thread = new Thread(test);
        }

        public Thread getThread() {
            return thread;
        }

        public JsonTestDriver getTestDriver() {
            return test;
        }
    }

}
