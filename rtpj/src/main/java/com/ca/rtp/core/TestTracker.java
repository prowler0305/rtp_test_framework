package com.ca.rtp.core;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Enumeration;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.TimeUnit;

/**
 * This class keeps accounting information for the executed tests.
 * Created by bergr05 on 2/25/2016.
 */
public class TestTracker {

    // Get a logger
    private static final Logger log = LogManager.getLogger(TestTracker.class);

    public final static String FAILED_MSG  = "*** TEST FAILED  *** ";
    public final static String PASSED_MSG  = "*** TEST PASSED  *** ";
    public final static String SKIPPED_MSG = "*** TEST SKIPPED *** ";
    public final static String RUNNING_MSG = "*** RUNNING TEST *** ";
    public final static String PASSED = "PASSED";
    public final static String FAILED = "FAILED";

    private static volatile int total = 0;
    private static volatile int passed = 0;
    private static volatile int skipped = 0;
    private static volatile int failed = 0;
    private static long start = 0;
    private static long end = 0;

    // ANSI Colors
    private static final String white = (char)27 + "[0;37m";
    private static final String red = (char)27 + "[0;31m";
    private static final String blue = (char)27 + "[1;34m";
    private static final String cyan = (char)27 + "[0;36m";
    private static final String yellow = (char)27 + "[0;33m";
    private static final String clear = (char)27 + "[0m";

    private static volatile ConcurrentHashMap<String, String> failures = new ConcurrentHashMap<>();
    private static volatile ConcurrentHashMap<String, String> skips = new ConcurrentHashMap<>();

    public synchronized static void upPassed() {
        passed++;
        upTotal();
    }

    public synchronized static void upFailed(String name, String reason) {
        failed++;
        failures.put(name, reason);
        upTotal();
    }

    public synchronized static void upSkipped(String name, String reason) {
        skipped++;
        skips.put(name, reason);
        upTotal();
    }

    private synchronized static void upTotal() {
        total++;
    }

    public static void timerStart() {
        start = System.nanoTime();
    }

    public static void timerStop() {
        end = System.nanoTime();
    }

    public static long getDuration(String unit) {

        TimeUnit tu = TimeUnit.valueOf(unit.toUpperCase().trim());

        if (end == 0) {
            end = System.nanoTime();
        }

        switch(tu) {
            case NANOSECONDS:
                return end - start;
            case MICROSECONDS:
                return TimeUnit.NANOSECONDS.toMicros(end - start);
            case MILLISECONDS:
                return TimeUnit.NANOSECONDS.toMillis(end - start);
            case SECONDS:
                return TimeUnit.NANOSECONDS.toSeconds(end - start);
            default:
                return TimeUnit.NANOSECONDS.toSeconds(end - start);
        }
    }

    public static int getTotal() {
        return total;
    }

    public static int getPassed() {
        return passed;
    }

    public static int getSkipped() {
        return skipped;
    }

    public static int getFailed() {
        return failed;
    }

    public synchronized static void reset() {
        failed = 0;
        total = 0;
        skipped = 0;
        passed = 0;
    }

    public static String print(){
       return "Total Tests : " + total
               + " Passed  : " + passed
               + " Failed  : " + failed
               + " Skipped : " + skipped
               + " Duration: " + getDuration("Milliseconds") + "(ms)";
    }

    /**
     * Format the TestTracker results.
     * @return String - The formatted results.
     */
    public static String toStringFormatted(){
        String finalResult;
        if(failed == 0) {
            if(skipped == 0) {
               finalResult = blue + PASSED + clear;
            } else {
                finalResult = yellow + FAILED+"*"+ clear;
            }
        } else {
            finalResult = red + FAILED + clear;
        }

        String template = "\n%s\nFinal Result: %s \nTotal: %s \nPassed: %s \nFailed: %s \nSkipped: %s \nDuration: %s, %s \n%s \n%s";
        return String.format(template,
                JsonTestRunner.starLine(),
                finalResult,
                total,
                passed,
                failed,
                skipped,
                getDuration("Seconds") + "(s)",
                getDuration("Milliseconds") + "(ms)",
                getDetails(),
                JsonTestRunner.starLine());
    }

    /**
     * Get the failures/skipped details.
     * @return Formatted string representing the result details.
     */
    public static synchronized String getDetails() {
        StringBuilder builder = new StringBuilder("");
        Enumeration<String> keys;

        if(failures.size() > 0 || skips.size() > 0) {
            builder.append("Details: ");
        } else {
            return "";
        }

        if(failures.size() > 0) {
            builder.append("\n  Failures: ");
            keys = failures.keys();
            while (keys.hasMoreElements()) {
                String key = keys.nextElement();
                String reason = failures.get(key).equals("") ? "No Detailed Reason Available." : failures.get(key);
                builder.append("\n      Test: " + red + key + clear + "\n       Reason: " + cyan + reason + clear);
            }
        }

        if (skips.size() > 0) {
            builder.append("\n  Skipped: ");
            keys = skips.keys();
            while (keys.hasMoreElements()) {
                String key = keys.nextElement();
                String reason = skips.get(key).equals("") ? "No Detailed Reason Available." : skips.get(key);
                builder.append("\n      Test: " + yellow + key + clear + "\n        Reason: " + cyan + reason + clear);
            }
        }

        return builder.toString();
    }
}
