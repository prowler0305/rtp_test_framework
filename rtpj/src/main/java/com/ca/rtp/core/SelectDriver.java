package com.ca.rtp.core;

import com.ca.rtp.auth.Credentials;
import com.ca.rtp.auth.CredentialsCache;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.CallableStatement;
import java.sql.Connection;

/**
 * The SelectDriver is intened to provide a quick interface for executing SELECT statements.
 *
 * Executing a SELECT statement using the SelectDriver can be done following these steps.
 *   ---------------------------------------------------------------------------------------------------------
 *   | Description                       | Code                                                              |
 *   ---------------------------------------------------------------------------------------------------------
 *   1.) Create the SelectDriver.        | SelectDriver driver = new SelectDriver(username, ssid, host, port);
 *   2.) Set the output format and type. | driver.setOutputManager(OutputDevice.FILE, OutputFormat.CSV);
 *   3.) Connect to the database.        | driver.getConnection();
 *   4.) Execute a SELECT statement.     | CallableStatement stmt = driver.execute(query);
 *   5.) Close the statement.            | driver.closeStmt(stmt);
 *   6.) Close the connection.           | driver.closeConnection();
 *
 * Created by bergr05 on 2/22/2016.
 */
public class SelectDriver {

    // Get a logger
    private static final Logger log = LogManager.getLogger(SelectDriver.class);

    private ConnectionInfo cInfo;
    private Connection conn = null;
    private OutputManager outputManager;
    private Credentials credentials;

    public SelectDriver(String userid, ConnectionInfo cInfo) {
        this.cInfo = cInfo;
        credentials = CredentialsCache.get(userid);
        outputManager = new OutputManager(OutputFormat.CSV, OutputDevice.CONSOLE);
    }

    /**
     * Get a database connection.
     */
    public void getConnection() throws RtpException {
        /* Create the database connection */
        try {
            conn = Connector.connect(cInfo, credentials, null);
        } catch (RtpException rtpe) {
            throw rtpe;
        } catch (Exception e) {
            throw new RtpException("Database Connection has failed for:" + cInfo.toString(), e);
        }

        log.info("Database Connected Successfully. ID: {}", conn.toString());
    }

    /**
     * Close the database connection.
     */
    public void closeConnection() {
        try {
            String token = conn.toString();
            conn.close();
            log.info("Database Connection Closed. ID: {} ", token);
        } catch (Exception e) {
            log.error("Error closing the database connection. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
        }
    }

    /**
     * Close the statement connection.
     */
    public void closeStmt(CallableStatement stmt) {
        try {
            stmt.close();
        } catch (Exception e) {
            log.error("Error closing the statement. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
        }
    }

    /**
     * Executes a SELECT statement.
     * By default this method will print the output to the console as a CSV.
     * The output manager can be set explicitly by using the setOutputManager method.
     *
     * If the query is successful a CallableStatement is returned.
     * Otherwise null is returned.
     *
     * @param query String
     * @return CallableStatement
     */
    public CallableStatement execute(String query) throws RtpException {

        /* Create a Callable statement. */
        CallableStatement stmt = Connector.createCallableStatement(conn, query);

        /* Execute the statement */
        if (stmt != null) {
            try {
                boolean check = stmt.execute();
                if (check) {
                    if(outputManager.getFormat() != OutputFormat.NONE || outputManager.getDevice() != OutputDevice.NONE) {
                       // ResultWriter.writeResult(stmt, outputManager, stmt.getResultSet());
                    }
                } else {
                    log.error("Error executing the statement");
                }
            } catch (Exception e) {
                throw new RtpException("Error preparing/executing the statement: " + query, e);
            }
        }
        return stmt;
    }

    /**
     * Sets the Output type for the query.
     * @param device OutputDevice
     * @param format OutputFormat
     */
    public void setOutputManager(OutputDevice device, OutputFormat format) {
        outputManager.setDevice(device);
        outputManager.setFormat(format);
    }

    public void setOutputManagerFile(String filepath, String filename) {
        outputManager.setFilepath(filepath);
        outputManager.setFilename(filename);
    }
}
