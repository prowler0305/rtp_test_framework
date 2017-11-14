package com.ca.rtp.examples;

import com.ca.rtp.auth.Credentials;
import com.ca.rtp.auth.CredentialsCache;
import com.ca.rtp.core.*;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;

/**
 * Example Database Driver.
 *
 * This program creates a DB2 Database connection, then issues a simple select and retrieves all available rows.
 *
 *  DB0G Host: usilca11.ca.com port: 5130
 *  D11D Host: usilca11.ca.com port: 5258
 *  DD0G Host: usilca11.ca.com port: 5052
 *
 * Created by bergr05 on 12/16/2015.
 */

public class DatabaseDriver {

    // Get a logger
    private static final Logger log = LogManager.getLogger(DatabaseDriver.class);

    public static void main(String args[]) {

        String userid = System.getProperty("user.name");
        String ssid = "DB0G";
        String numberOfRows = "100";

        /* Create a Connection Info Object */
        ConnectionInfo cInfo;
        try {
            cInfo = Subsystems.getConnectionInfo(ssid);
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }

        /* Create the Credentials */
        Credentials credentials = CredentialsCache.get(userid);

        /* Create a query */
        String query = "Select NAME from SYSIBM.SYSTABLES FETCH FIRST % ROWS ONLY;";

        /* Create an output manager */
        OutputManager output = new OutputManager(OutputFormat.CSV, OutputDevice.CONSOLE);

        /* Create the database connection */
        Connection conn;
        try {
            conn = Connector.connect(cInfo, credentials, null);
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }
        CallableStatement stmt;
        try {
             stmt = Connector.createCallableStatement(conn, String.format(query, numberOfRows));
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        } finally {
            try {
                conn.close();
            } catch (SQLException sqle) {
                log.error("Error closing connection. \n Trace: {}", ExceptionUtilities.stacktraceToString(sqle));
            }
        }

        if (stmt != null) {
            try {
                stmt.execute();
               //ResultWriter.writeResult(stmt, output, stmt.getResultSet());
                stmt.close();
                int rc = Connector.close(conn);
                if (rc != -1) {
                    log.info("Database Connection Closed.");
                }

            } catch (Exception e) {
                log.error("Error preparing/executing the statement. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            }
        }
    }
}