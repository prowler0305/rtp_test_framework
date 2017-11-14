package com.ca.rtp.core.json;

import com.ca.rtp.core.ConnectionInfo;
import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.Subsystems;
import com.ca.rtp.core.TestTracker;
import com.fasterxml.jackson.databind.JsonNode;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * The JsonTestSuite class is used to process the JSON object suite node and all its tests.
 * Created by bergr05 on 4/19/2016.
 * Copyright (c) 4/19/2016 CA Technologies. All rights reserved.
 */
public class JsonTestSuite {

    // Get a logger
    private static final Logger log = LogManager.getLogger(JsonTestSuite.class);

    private final JsonNode suite;
    private ConnectionInfo cInfo;
    private String userid;
    private String externalLibraryPath;

    public JsonTestSuite(JsonNode suite, ConnectionInfo cInfo, String userid) {
        this.suite = suite;
        this.cInfo = cInfo;
        this.userid = userid;
        this.externalLibraryPath = "";
    }

    public JsonTestSuite(JsonNode suite, ConnectionInfo cInfo, String userid, String path) {
        this.suite = suite;
        this.cInfo = cInfo;
        this.userid = userid;
        this.externalLibraryPath = path;
    }

    public ArrayList<JsonTest> build() throws RtpException {
        ArrayList<JsonTest> tests = new ArrayList<>();

        JsonNode connNode = suite.path("connection");
        if(!connNode.isMissingNode()) {
            processConnection(connNode);
        }

        JsonNode testsNode = suite.path("tests");
        if(!testsNode.isMissingNode() && testsNode.isArray()) {
            for (JsonNode testNameNode : testsNode) {
                JsonTestReader reader;
                if (externalLibraryPath.isEmpty()) {
                    reader = new JsonTestReader(testNameNode.asText());
                }
                else {
                    reader = new ExternalJsonTestReader(testNameNode.asText(), externalLibraryPath);
                }

                JsonNode root;
                try {
                    root = reader.read();
                } catch (RtpException e) {
                    TestTracker.upSkipped(testNameNode.asText(), e.getMessage()); //Skip this test, but continue with other tests in the suite.
                    throw e;
                }

                JsonNode testNode = root.path("test");
                if (!testNode.isMissingNode()) {
                    JsonTest test = new JsonTest(root.path("test"), cInfo, userid, testNameNode.asText());
                    try {
                        test.build();
                    } catch (RtpException rtpe) {
                        rtpe.print();
                        TestTracker.upSkipped(testNameNode.asText(), rtpe.getMessage());
                        continue;
                    }
                    tests.add(test);
                }
            }
        } else {
            throw new RtpException("JSON test suite does not contain the required {tests} array.");
        }

        return tests;
    }

    /**
     * The processConnection method retrieves the required connection information from the JSON map.
     * The current "connection" node is processed for the following nodes:
     *  - ssid
     *  - userid
     * @param connNode The "connection" node in the JSON map.
     */
    private void processConnection(JsonNode connNode) throws RtpException {

        Iterator<String> conn = connNode.fieldNames();

        while (conn.hasNext()) {

            String field = conn.next();
            String value;
            try {
                value = connNode.get(field).asText();
            } catch (Exception e) {
                log.warn("Test is missing a value for Node: {} {}", connNode.toString(), field);
                value = "";
            }

            switch (field) {
                case "ssid":
                    if(this.cInfo.getSSID().equals("")) {
                        this.cInfo = Subsystems.getConnectionInfo(value);
                        log.debug("Using suite level connection information. SSID: {}", value);
                    }
                    break;
                case "userid":
                    if(this.userid.equals("")) {
                        log.debug("Using suite level userid information. USERID: {}", value);
                        userid = value;
                    }
                    break;
                default:
                    log.warn("Test contains an unrecognized Field: {} {}", connNode.toString(), field);
                    break;
            }
        }
    }
}
