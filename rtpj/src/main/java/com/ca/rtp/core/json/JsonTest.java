package com.ca.rtp.core.json;

import com.ca.rtp.core.*;
import com.fasterxml.jackson.databind.JsonNode;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.Filter;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * The JsonTest class reads a RTP JSON test file and creates the expected
 * objects to be used for the test execution phase.
 * Created by bergr05 on 3/22/2016.
 *
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
public class JsonTest {

    // Get a logger
    private static final Logger log = LogManager.getLogger(JsonTest.class);

    // Default Connection Information
    public static final ConnectionInfo DEFAULT_CONNECTION = new ConnectionInfo("","","");
    public static final String DEFAULT_USERID = "";

    private ConnectionInfo cInfo;
    private ThreadingInfo tInfo;
    private ArrayList<Statement> statements;
    private String userid;
    private long seed;
    private final JsonNode testNode;
    public final String name;
    private ArrayList<ResultSummary> results;
    private String description;

    public JsonTest(JsonNode testNode, ConnectionInfo conn, String userid, String name){
        // Initialize the defaults.
        this.testNode = testNode;
        this.statements = new ArrayList<>();
        this.results = new ArrayList<>();
        this.cInfo = new ConnectionInfo(conn.getSSID(),conn.getHost(), conn.getPort());
        this.tInfo = new ThreadingInfo(1,false, 0);
        this.userid = userid;
        this.name = name;
        this.seed = 0L;
        this.description = "";
    }

    /**
     * The parse function reads a JSON file and parses the structure into RTP test components for execution.
     * @throws RtpException
     */
    public void build() throws RtpException {

        // Get the test's description.
        description = testNode.path("description").asText();

        // Process a test's multithreaded object
        JsonNode threading = testNode.path("threading");
        tInfo = processThreading(threading);

        // Process Test Connection Information
        JsonNode conn = testNode.path("connection");
        if(conn.isMissingNode()) {
            TestTracker.upSkipped(this.name, "JSON test does not contain the required {connection} object.");
            throw new RtpException("JSON test does not contain the required {connection} object.");
        } else {
            processConnection(conn);
        }

        // Process optional seed pair
        JsonNode seedNode = testNode.path("seed");
        if (!seedNode.isMissingNode()) {
            seed = seedNode.asLong();
        }

        // Process Statements
        JsonNode stmts = testNode.path("statements");
        if(stmts.isMissingNode()) {
            TestTracker.upSkipped(this.name, "JSON test does not contain the required {statements} array.");
            throw new RtpException("JSON test does not contain the required {statements} array.");
        } else {
            if(stmts.isArray()) {
                for (JsonNode stmt : stmts) {
                    processStatement(stmt);
                }
            }
        }
    }

    /**
     * The processStatement method retrieves the required statement information from the JSON map.
     * The current "statement" node is processed for the following nodes:
     *  - text
     *  - type
     *  - sub-type
     *  - repeat
     *  - args
     * @param stmtNode The "statement" node in the JSON map.
     */
    private void processStatement(JsonNode stmtNode) {

        Iterator<String> stmt = stmtNode.fieldNames();
        String text = "";
        String type = "";
        int repeat = 1;
        int sleep = 0;
        int batches = 0;
        String subType = "";
        ArrayList<Parameter> parameterList = new ArrayList<>();
        Expectations expectations = new Expectations();

        while (stmt.hasNext()) {

            String field = stmt.next();
            StatementTypes st;

            try {
                st = StatementTypes.valueOf(field.toUpperCase());
            } catch (IllegalArgumentException iae) {
                st = StatementTypes.NONE;
            }

            switch (st) {
                case TEXT:
                    text = stmtNode.get(field).asText("");
                    break;

                case TYPE:
                    type = stmtNode.get(field).asText("").toUpperCase();
                    break;

                case ARGS:
                    parameterList = processStatementArguments(stmtNode.path(field));
                    break;

                case SUBTYPE:
                    subType = stmtNode.get(field).asText("").toUpperCase();
                    break;

                case REPEAT:
                    repeat = stmtNode.get(field).asInt();
                    break;

                case EXPECT:
                    expectations = processExpectations(stmtNode.path(field));
                    break;

                case SLEEP:
                    sleep = stmtNode.get(field).asInt();
                    break;

                case BATCHES:
                    batches = stmtNode.get(field).asInt();
                    break;

                case DESCRIPTION:
                    batches = stmtNode.get(field).asInt();
                    break;

                default:
                    log.warn("The test contains an unrecognized Field: {} in {}", field, stmtNode.toString());
                    break;
            }
        }

        // Add this statement to the list.
        statements.add(new Statement(text, type, subType, repeat, expectations, parameterList, sleep, batches));
    }

    /**
     * The processStatementArguments method retrieves the required statement arguments information from the JSON map.
     * The current "args" node is processed for the following nodes:
     *  - value
     *  - datatype
     *  - type
     *  - seed
     * @param argsNode The "args" node in the JSON map for a given statement.
     * @return ArrayList<Parameter> The Parameter List for a given statement.
     */
    private ArrayList<Parameter> processStatementArguments(JsonNode argsNode) {

        ArrayList<Parameter> parameterList = new ArrayList<>();

        // Process arguments array

        for (JsonNode argNode : argsNode) {
            Iterator<String> names = argNode.fieldNames();
            Arguments arguments = new Arguments();

            arguments.setSeed(this.seed);

            String dataType = "";
            String type = "";
            String subType = "";

            // Process each field of an argument
            while (names.hasNext()) {
                String field = names.next();
                ArgumentTypes arg;

                // Extract an argument field & value
                try {
                    arg = ArgumentTypes.valueOf(field.toUpperCase());
                } catch(IllegalArgumentException iae) {
                    arg = ArgumentTypes.NONE;
                }

                switch (arg) {

                    case VALUE:
                        arguments.setValue(argNode.get(field));
                        break;

                    case DATATYPE:
                        dataType = argNode.get(field).asText("").toUpperCase();
                        break;

                    case TYPE:
                        type = argNode.get(field).asText("").toUpperCase();
                        break;

                    case SUBTYPE:
                        arguments.setSubtype(argNode.get(field).asText("").toUpperCase());
                        break;

                    case LENGTH:
                        //length = argNode.get(field).asInt();
                        arguments.setLength(argNode.get(field).asInt());
                        break;

                    case KEY:
                        arguments.setKey(argNode.get(field).asText("").toUpperCase());
                        break;

                    case MAX:
                        arguments.setMax(argNode.get(field).asInt());
                        break;

                    case RANDOMIZE:
                        arguments.setRandomize(argNode.get(field).asBoolean());
                        break;

                    case DESCRIPTION:
                        break;

                    default:
                        log.warn("The test contains an unrecognized Field: {} in {}", field, argNode.toString());
                        break;
                }
            }

            //TODO: Move this to specific parameter implementations.
            if ((type.equals("STATIC") || type.equals("INCREMENTED")) && !arguments.getSubType().equals("OUT")) {
                arguments.setValue(Converter.parameterValueToObject((JsonNode)arguments.getValue(), dataType));
            }

            parameterList.add(ParameterFactory.buildParameter(type, dataType, arguments));
        }

        return parameterList;
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
                log.warn("Test is missing value for Node: {} Field: {}",connNode.toString(), field);
                value = "";
            }

            switch (field) {
                case "ssid":
                    if (this.cInfo.getSSID().equals("")) {
                        log.debug("Using Test level connection information. SSID: {}", value);
                        this.cInfo = Subsystems.getConnectionInfo(value);
                    }
                    break;
                case "userid":
                    if (this.userid.equals("")) {
                        userid = value;
                        log.debug("Using Test level userid information. USERID: {}", value);
                    }
                    break;
                default:
                    log.warn("Test contains unrecognized Field: {} in {}", field, connNode.toString());
                    break;
            }
        }
    }

    /**
     * The processThreading method retrieves the required threading information from the JSON map.
     * The current "threading" node is processed for the following nodes:
     *  - threads
     *  - parallel
     * @param threadingNode The "connection" node in the JSON map.
     * @return ThreadingInfo
     */
    private ThreadingInfo processThreading(JsonNode threadingNode) {

        if(threadingNode.isMissingNode()) {
            return new ThreadingInfo(1,false, 0);
        }

        Iterator<String> fields = threadingNode.fieldNames();
        int threads = 1;
        boolean parallel = false;
        int sleep = 0;
        while (fields.hasNext()) {

            String field = fields.next();

            switch (field) {
                case "threads":
                    threads = threadingNode.get(field).asInt();
                    break;
                case "parallel":
                    parallel = threadingNode.get(field).asBoolean();
                    break;
                case "sleep":
                    sleep = threadingNode.get(field).asInt();
                    break;
                default:
                    log.warn("Test contains an unrecognized Field: {} in {}", field, threadingNode.toString());
                    break;
            }
        }

        return new ThreadingInfo(threads, parallel, sleep);
    }

    /**
     * The processExpectations method retrieves the required statement expectation information from the JSON map.
     * The current "expectations" node is processed for the following nodes:
     *  - sqlerror
     *  - rows
     *  - columns
     * @param expectationNode The "expectations" node in the JSON map.
     * @return ThreadingInfo
     */
    private Expectations processExpectations(JsonNode expectationNode) {

        if(expectationNode.isMissingNode()) {
            return new Expectations();
        }

        Iterator<String> fields = expectationNode.fieldNames();
        Integer sqlerror = 0;
        Integer rows = -1;
        Integer columns = -1;
        boolean ignore = false;

        while (fields.hasNext()) {

            String field = fields.next();

            switch (field) {
                case "sqlerror":
                    sqlerror = expectationNode.get(field).asInt();
                    break;
                case "rows":
                    rows = expectationNode.get(field).asInt();
                    break;
                case "columns":
                    columns = expectationNode.get(field).asInt();
                    break;
                case "ignore":
                    ignore = expectationNode.get(field).asBoolean();
                    break;
                default:
                    log.warn("Test contains an unrecognized Field: {} in {}", field, expectationNode.toString());
                    break;
            }
        }

        return new Expectations(sqlerror, rows, columns, ignore);
    }

    /**
     * Get the Connection information.
     * @return A ConnectionInfo object
     */
    public ConnectionInfo getConnectionInfo() {
        // Get the Connection Information
        return this.cInfo;
    }

    /**
     * Get the userid value.
     * @return A userid String object.
     */
    public String getUserid() {
        // Get the userid
        return this.userid;
    }

    public ArrayList<Statement> getStatements() {
        return this.statements;
    }

    /**
     * Clone the current JsonTest Object.
     * @return JsonTest
     */
    public JsonTest clone() {

        // Clone the Statement ArrayList
        ArrayList<Statement> stmtList = new ArrayList<>();

        for (Statement stmt : this.statements) {
            stmtList.add(stmt.clone());
        }

        JsonTest cloneTest = new JsonTest(this.testNode, this.cInfo, this.userid, this.name);
        cloneTest.tInfo = this.tInfo;
        cloneTest.seed = this.seed;
        cloneTest.statements = stmtList;

        return cloneTest;
    }

    public ThreadingInfo getThreadingInfo() {
        return this.tInfo;
    }

    public void addResult(ResultSummary result) {
        this.results.add(result);
    }

    public ArrayList<ResultSummary> getResults() {
        return this.results;
    }

    /**
     * Returns the result of the test.
     * @return boolean
     */
    public boolean getFinalResult() {
        for (ResultSummary result : this.results) {
            if (!result.getStatus()) {
                return ResultSummary.FAILED;
            }
        }

        return ResultSummary.PASSED;
    }

    public long getSeed() {
        return this.seed;
    }

    public String getDescription() {
        return this.description;
    }

    public void setSeed(long seed) {
        this.seed = seed;
    }


    /**
     * Returns a formatted list of reasons for a given test's failure.
     * @return String
     */
    public String getFailures() {
        StringBuilder sb = new StringBuilder("");
        for (ResultSummary result : this.results) {
            if(!result.getStatus()) {
                sb.append("\n       { " + result.getFailureReason() + "}");
            }
        }

        return sb.toString();
    }
}