package com.ca.rtp.core;

import com.ca.rtp.auth.CredentialsCache;
import com.ca.rtp.auth.CredentialsException;
import com.ca.rtp.core.json.*;
import com.ca.rtp.core.json.Parameter;
import com.ca.rtp.core.json.Statement;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.config.plugins.util.ResolverUtil;

import java.sql.*;
import java.util.ArrayList;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

/**
 * The JsonTestDriver executes a single JsonTest.
 * Created by schke19 on 3/22/2016.
 */
public class JsonTestDriver implements Runnable  {

    // Get a logger
    private static final Logger log = LogManager.getLogger(JsonTestDriver.class);

    private Connection conn;
    private static volatile boolean abort = false; // Used in multithreaded tests as an early exit valve

    private OutputManager outputManager;
    private JsonTest test;

    public JsonTestDriver(JsonTest test) {
        this.outputManager = new OutputManager(OutputFormat.CSV, OutputDevice.CONSOLE);
        this.test = test;
    }

    /**
     * Execute a test.
     */
    public void run() {
        try {
            if(!abort) {
                execute(test);
            } else {
                log.info("Aborting test due to previous errors.");
            }
        } catch (RtpException rtpe) {
            if (rtpe.getCause() instanceof CredentialsException) {
                abort = true;
            }
            rtpe.print();

            ResultSummary summary = new ResultSummary();
            summary.setStatus(ResultSummary.FAILED);
            summary.setFailureReason(test.getFailures() + " " + rtpe.getMessage() + " " + rtpe.getCause().getMessage());
            test.addResult(summary);

        } catch (Exception e) {
            ResultSummary summary = new ResultSummary();
            summary.setStatus(ResultSummary.FAILED);
            summary.setFailureReason(test.getFailures() + " " + e.getMessage());
            test.addResult(summary);
        }
    }

    /**
     * Executes a single JsonTest.
     */
    public void execute(JsonTest test) throws RtpException {

        // Start to execute the test
        log.debug("Thread: { {} executing test: {} ", Thread.currentThread().getName(), test.name);

        long seed = test.getSeed() != 0 ? test.getSeed() : 0;

        // Define results
        ArrayList<ResultSummary> results = new ArrayList<>();

        // Declare "holders" for the three potential types of statement
        java.sql.Statement immediateStatement = null;
        PreparedStatement preparedStatement = null;
        CallableStatement callableStatement = null;

        Properties clientProps = new Properties();
        clientProps.setProperty("ApplicationName", test.name);

        conn = Connector.connect(test.getConnectionInfo(), CredentialsCache.get(test.getUserid()), clientProps);

        log.debug("Database Connected Successfully. ID: {}", conn.toString());
        int stmtNumber = 0; // Init statement counter

        for (Statement statement : test.getStatements()) {
            stmtNumber++;

            log.debug("Statement Hash: {}", statement.hashCode());
            log.debug("{}: Expecting SQLError: {}", statement.hashCode(), statement.getExpectations().getSqlerror());
            log.debug("{}: Expecting Rows: {}", statement.hashCode(), statement.getExpectations().getRows());
            log.debug("{}: Expecting Columns: {}", statement.hashCode(), statement.getExpectations().getColumns());

            switch (statement.getType()) {
                case "IMMEDIATE":
                    immediateStatement = Connector.createStatement(conn);
                    break;
                case "PREPARE":
                    log.debug("{}: Preparing Statement {}",statement.hashCode(),statement.getText());
                    preparedStatement = Connector.createPreparedStatement(conn, statement.getText());
                    break;
                case "CALL":
                    log.debug("{}: Preparing Statement {}",statement.hashCode(),statement.getText());
                    callableStatement = Connector.createCallableStatement(conn, statement.getText());
                    break;
                case "BATCH":
                    log.debug("{}: Preparing Batch Statements {}",statement.hashCode(),statement.getText());
                    executeBatch(test, conn, statement, stmtNumber, seed);
                    continue; // Process next statement.
            }

            String origText = statement.getText();

            for (int executionNumber = 1; executionNumber <= statement.getRepeat(); executionNumber++) {

                ResultSummary summary = new ResultSummary();

                try {

                    switch (statement.getType()) {
                        case "IMMEDIATE":

                            // Process any literal parameters.  Only valid on immediate statements.
                            setLiteralParameters(statement, seed);

                            log.debug("{}: Executing Statement: Length: {} Text: {}", statement.hashCode(), statement.getText().length(), statement.getText());
                            if(immediateStatement.execute(statement.getText())) {
                                summary.processResult(immediateStatement, outputManager, stmtNumber);
                                summary.setStatus(ResultSummary.PASSED);
                            }
                            break;
                        case "PREPARE":
                            setLiteralParameters(statement, seed);
                            preparedStatement = Connector.createPreparedStatement(conn, statement.getText());
                            setParameters(statement.getParameterList(), preparedStatement);
                            log.debug("{}: Executing Statement: Length: {} Text: {}", statement.hashCode(), statement.getText().length(), statement.getText());
                            if(preparedStatement.execute()) {
                                summary.processResult(preparedStatement, outputManager, stmtNumber);
                                summary.setStatus(ResultSummary.PASSED);
                            }
                            break;
                        case "CALL":
                            setParameters(statement.getParameterList(), callableStatement);
                            log.debug("{}: Executing Statement: {}", statement.hashCode(), statement.getText());
                            if(callableStatement.execute()) {
                                summary.processResult(callableStatement, outputManager, stmtNumber);
                                summary.setStatus(ResultSummary.PASSED);
                            }
                            getOutParameters(statement.getParameterList(), callableStatement);
                            break;
                    }

                    checkResultSetExpectations(summary, statement, stmtNumber);

                } catch (SQLException e) {

                    if (statement.getExpectations().ignore) {
                        log.debug("STMT {}: The following SQL error is being ignored due to test parameters. SQL Error: {}", stmtNumber, e.getMessage());
                        summary.setStatus(ResultSummary.PASSED);
                    } else if (statement.getExpectations().getSqlerror() != e.getErrorCode()) {
                        log.error("{}: Failed during Execute. \n Trace: {}", statement.hashCode(), ExceptionUtilities.stacktraceToString(e));
                        summary.setStatus(ResultSummary.FAILED);
                        summary.setFailureReason("STMT("+stmtNumber+") " + e.getMessage());
                    } else {
                        log.debug("{}: Expected SQLError {} has occurred", statement.hashCode(), statement.getExpectations().getSqlerror());
                        summary.setStatus(ResultSummary.PASSED);
                    }
                } catch (Exception e) {
                    log.error("{}: Failed during Execute. \n Trace: {}", statement.hashCode(), ExceptionUtilities.stacktraceToString(e));
                    summary.setStatus(ResultSummary.FAILED);
                    summary.setFailureReason("STMT("+stmtNumber+") " + e.getMessage());
                }

                test.addResult(summary);
                pause(statement.sleep, stmtNumber);

                // Reset text
                statement.setText(origText);

            }

        }

        try {
            String token = conn.toString();
            conn.close();
            log.debug("Database Connection Closed. ID: {}", token);
        } catch (SQLException e) {
            ResultSummary summary = new ResultSummary();
            log.error("Error closing the database connection. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            summary.setStatus(ResultSummary.FAILED);
            summary.setFailureReason(e.getMessage());
            results.add(summary);
        }

        return;
    }

    /**
     * Execute a prepared statement in batch mode.  This is used when processing the statement type of "BATCH".
     * @param test The JsonTest
     * @param conn The DB2 Connection
     * @param statement The JsonTest statement being executed
     * @param stmtNumber The current JsonTest statement number
     */
    private void executeBatch(JsonTest test, Connection conn, Statement statement, int stmtNumber, long seed) {
        String origText = statement.getText();

        for (int executionNumber = 1; executionNumber <= statement.getRepeat(); executionNumber++) {

            ResultSummary summary = new ResultSummary();

            // Process any literal parameters.  Only valid on immediate statements.
            setLiteralParameters(statement, seed);

            try {
                PreparedStatement preparedStatement = Connector.createPreparedStatement(conn, statement.getText());

                // Add the number of rows indicated by the "batches" statement parameter.
                log.debug("Adding {} rows for batch execution.", statement.getBatches());
                for (int j = 0; j < statement.getBatches(); j++) {
                    setParameters(statement.getParameterList(), preparedStatement);
                    preparedStatement.addBatch();
                }

                log.debug("{}: Executing Batch Statement: {}", statement.hashCode(), statement.getText());
                int[] results = preparedStatement.executeBatch();  // Execute the batch statement.

                boolean result = true;
                for(int k = 0; k < results.length; k++) {
                    if (results[k] != java.sql.Statement.SUCCESS_NO_INFO && results[k] < 0) {
                        log.error("{}: Failed during Execute Batch for Statement Number. Error: {}", stmtNumber, results[k]);
                        result = false;
                        //break; // Quit after first error found.
                    }
                }

                // Check batch execution result
                if(result) {
                    summary.setStatus(ResultSummary.PASSED);
                } else {
                    summary.setStatus(ResultSummary.FAILED);
                    summary.setFailureReason("STMT("+stmtNumber+") Failed to execute in batch mode." );
                }

            } catch (SQLException e) {

                if (statement.getExpectations().ignore) {
                    log.debug("STMT {}: The following SQL error is being ignored due to test parameters. SQL Error: {}", stmtNumber, e.getMessage());
                    summary.setStatus(ResultSummary.PASSED);
                } else if (statement.getExpectations().getSqlerror() != e.getErrorCode()) {
                    log.error("{}: Failed during Execute. \n Trace: {}", statement.hashCode(), ExceptionUtilities.stacktraceToString(e));
                    summary.setStatus(ResultSummary.FAILED);
                    summary.setFailureReason("STMT("+stmtNumber+") " + e.getMessage());
                } else {
                    log.debug("{}: Expected SQLError {} has occurred", statement.hashCode(), statement.getExpectations().getSqlerror());
                    summary.setStatus(ResultSummary.PASSED);
                }
            } catch (Exception e) {
                log.error("{}: Failed during Execute. \n Trace: {}", statement.hashCode(), ExceptionUtilities.stacktraceToString(e));
                summary.setStatus(ResultSummary.FAILED);
                summary.setFailureReason("STMT("+stmtNumber+") " + e.getMessage());
            }

            test.addResult(summary);
            pause(statement.sleep, stmtNumber);

            // Reset all parameter values to their original values except the literal parameters.
            resetParameterValues(statement);

            // Reset text
            statement.setText(origText);

        }
    }

    private void setParameters(ArrayList<Parameter> parameterList, PreparedStatement statement) {
        CallableStatement callableStatement; //Instantiate this in case we have to use it for an OUT or INOUT parameter
        if (!parameterList.isEmpty()) {
            int i = 0;
            int j = 1; // Prepared parameter counters.
            try {
                while (i < parameterList.size()) {
                    Parameter parameter = parameterList.get(i);

                    /*
                     *  Process Type but:
                     *    skip setting the parameter value if sub-type is OUT
                     *    skip setting the parameter value if sub-type is LITERAL
                     */
                    if (!parameter.getSubType().contains("OUT") && !parameter.getSubType().equals("LITERAL")) {
                        switch (parameter.getType()) {
                            case "GENERATED":
                                GeneratedParameter generatedParameter = (GeneratedParameter) parameter;
                                statement.setObject((j), generatedParameter.getValue());
                                j++;
                                break;
                            case "STATIC":
                                StaticParameter staticParameter = (StaticParameter) parameter;
                                statement.setObject((j), staticParameter.getValue());
                                j++;
                                break;
                            case "INCREMENTED":
                                IncrementedParameter incrementedParameter = (IncrementedParameter) parameter;
                                statement.setObject((j), incrementedParameter.getValue());
                                incrementedParameter.increment();
                                j++;
                                break;
                        }
                    }

                    /*
                     *  Process Sub-Type
                     */
                    switch (parameter.getSubType()) {
                        case "OUT":
                            callableStatement = (CallableStatement) statement;
                            callableStatement.registerOutParameter((i+1), Converter.getSqlType(parameter.getDataType()));
                            break;
                        case "INOUT":
                            callableStatement = (CallableStatement) statement;
                            callableStatement.registerOutParameter((i+1), Converter.getSqlType(parameter.getDataType()));
                            break;
                    }

                    i++; // Move to next parameter.
                }
            } catch (SQLException e) {
                log.error("Failed setting parameters. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            }
        }
    }

    private void setLiteralParameters(Statement statement, long seed) {

        ArrayList<Parameter> parameterList = statement.getParameterList();

        for (int i = 0; i < parameterList.size(); i++) {
            Parameter parameter = parameterList.get(i);
            final String key = parameter.getArguments().getKey();
            parameter.getArguments().setSeed(seed);
            if (parameter.getSubType().toUpperCase().equals("LITERAL") && !key.equals("")) {
                switch (parameter.getType()) {
                    case "GENERATED":
                        GeneratedParameter generatedParameter = (GeneratedParameter) parameter;
                        statement.setText(statement.getText().replace(key, generatedParameter.getValue().toString()));
                        break;
                    case "STATIC":
                        StaticParameter staticParameter = (StaticParameter) parameter;
                        statement.setText(statement.getText().replace(key, staticParameter.getValue().toString()));
                        break;
                    case "INCREMENTED":
                        IncrementedParameter incrementedParameter = (IncrementedParameter) parameter;
                        statement.setText(statement.getText().replace(key, incrementedParameter.getValue().toString()));
                        incrementedParameter.increment();
                        break;
                }
            }
        }
    }

    /**
     * Reset all non-literal values to their starting values.  Only used for repeated batch inserts.
     * @param statement The batch statement.
     */
    private void resetParameterValues(Statement statement) {

        ArrayList<Parameter> parameterList = statement.getParameterList();

        for (int i = 0; i < parameterList.size(); i++) {
            Parameter parameter = parameterList.get(i);
            if (!parameter.getSubType().toUpperCase().equals("LITERAL")) {
                    parameter.resetOriginalValue();
                }
        }
    }

    private void getOutParameters(ArrayList<Parameter> parameterList, CallableStatement statement) {
        if (!parameterList.isEmpty()) {
            int i = 0;
            try {
                while (i < parameterList.size()) {
                    Parameter parameter = parameterList.get(i);
                    if (parameter.getSubType().equals("OUT") || parameter.getSubType().equals("INOUT")) {
                            log.debug("{}: (IN)OUT Parameter at index {} {} {} ",statement.hashCode(), (i+1), " = ", statement.getObject(i+1));
                    }
                    i++; // Move to next parameter.
                }
            } catch (SQLException e) {
                log.error("Failed getting stored procedure OUT parameters. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            }
        }
    }

    private void checkResultSetExpectations(ResultSummary s, Statement stmt, int stmtNumber) throws SQLException {

        Expectations ex = stmt.getExpectations();
        StringBuilder msg = new StringBuilder();

        if (ex.ignore) {
            log.debug("STMT {}: Result Rows/Columns are being ignored due to test parameters.", stmtNumber);
            return;
        }

        if (ex.getColumns() != -1) {
            if (ex.getColumns() != s.getColumnCount()) {
                String template = "STMT %s: Expected %s Columns but found %s";
                log.error("{}: Expected {} Columns but found {}", stmt.hashCode(), ex.getColumns(), s.getColumnCount());
                msg.append("{" + stmtNumber + " " + String.format(template, stmt.hashCode(), ex.getColumns(), s.getColumnCount()) + "}     ");
                s.setStatus(ResultSummary.FAILED);
            }
            else {
                log.debug("{}: Expectation Passed. Number of Columns {} found", stmt.hashCode(), ex.getColumns());
            }
        }

        if (ex.getRows() != -1) {
            if (ex.getRows() != s.getRowCount()) {
                String template = "STMT %s: Expected %s Rows but found %s";
                s.setFailureReason(String.format(template, stmt.hashCode(), ex.getRows(), s.getRowCount()));
                log.error("{}: Expected {} Rows but found {}", stmt.hashCode(), ex.getRows(), s.getRowCount());
                msg.append("{" + stmtNumber + " " + String.format(template, stmt.hashCode(), ex.getRows(), s.getRowCount()) + "}");
                s.setStatus(ResultSummary.FAILED);
            }
            else {
                log.debug("{}: Expectation Passed. Number of Rows {} found", stmt.hashCode(), ex.getRows());
            }
        }

        if (!s.getStatus()) {
            s.setFailureReason(msg.toString());
        }

    }

    /**
     * Returns the JsonTest.
     * @return
     */
    public JsonTest getTest() {
        return this.test;
    }

    public void pause(int duration, int stmtNum) {
        // Sleep for the desired amount of time
        if (duration > 0) {
            try {
                log.debug("STMT({}) Sleeping for {} seconds.", stmtNum, duration);
                Thread.sleep(TimeUnit.SECONDS.toMillis(duration));
            } catch (InterruptedException ie) {
                log.error("STMT{}: Failed during Execute. \n Trace: {}", stmtNum, ExceptionUtilities.stacktraceToString(ie));
            }
        }
    }

    /**
     * Sets the Output type for the test.
     * @param device OutputDevice
     * @param format OutputFormat
     */
    public void setOutputManager(OutputDevice device, OutputFormat format) {
        outputManager.setDevice(device);
        outputManager.setFormat(format);
    }

    /**
     * Sets the output file for the test.
     * @param filepath String
     * @param filename String
     */
    public void setOutputManagerFile(String filepath, String filename) {
        outputManager.setFilepath(filepath);
        outputManager.setFilename(filename);
    }
}
