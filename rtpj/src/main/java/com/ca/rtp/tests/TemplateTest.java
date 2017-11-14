package com.ca.rtp.tests;

import com.ca.rtp.core.RTPExecutor;
import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.RtpTest;

import java.sql.CallableStatement;
import java.util.HashMap;

/**
 * This template test can be used to execute a single SQL statement.
 * The only modification required is to set the class SQL string value @SQL.
 *
 * Created by bergr05 on 3/17/2016.
 * Copyright (c) 3/17/2016 CA Technologies. All rights reserved.
 */
public class TemplateTest implements RtpTest {

    // @SQL Enter the SQL statement to execute below:
    private String sql = "<insert sql statement here>";

    /**
     * Constructor
     */
    public TemplateTest() {

    }

    /**
     * The invoke method is called directly from the TestRunner.java program
     * and is the main entry point into a given RtpTest.
     *
     * @param parms A hashmap containing all parameters for a given test.
     *              The parameters are in key,value pairs.
     * @return A boolean indicating the result of the test (PASS/FAIL).
     */
    public boolean invoke(HashMap<String, String> parms) {

        String user = parms.get("USERID"); // Get the userid.
        String ssid = parms.get("SSID"); // Get the target SSID.

        // Create the RTPExecutor
        RTPExecutor exec = new RTPExecutor(user, ssid, sql);

        // Validate user and SSID parameters.
        if (!exec.validateUserAndSSID(user, ssid)) {
            return false;
        }

        // Execute the SQL statement
        CallableStatement stmt;
        try {
            stmt = exec.execute();
            exec.closeStmt(stmt);
        } catch (RtpException rtpe) {
            rtpe.print();
            return false;
        } finally{
            exec.close();
        }

        // Return the result
        return true;
    }
}