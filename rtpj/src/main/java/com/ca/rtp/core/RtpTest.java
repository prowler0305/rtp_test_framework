package com.ca.rtp.core;

import java.util.HashMap;

/**
 * Created by bergr05 on 2/25/2016.
 */
public interface RtpTest {

    /**
     * The invoke method is called directly from the TestRunner.java program
     * and is the main entry point into a given RtpTest.
     * @param parms A hashmap containing all parameters for a given test.
     *              The parameters are in key,value pairs.
     * @return A boolean indicating the result of the test (PASS/FAIL).
     */
    boolean invoke(HashMap<String, String> parms);
}
