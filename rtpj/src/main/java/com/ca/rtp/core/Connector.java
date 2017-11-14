package com.ca.rtp.core;
/**
 * Class Connect
 *
 * This class provides a connection API to DB2 for z/OS.
 *
 * Helpful notes:
 * Get the CCSID for the DB2 subsystem:
 * SELECT
 * GETVARIABLE('SYSIBM.APPLICATION_ENCODING_SCHEME') AS CCSID
 * FROM SYSIBM.SYSDUMMY1
 *
 * Get the CCSID for a DB2 Database
 * SELECT SBCS_CCSID, MIXED_CCSID, DBCS_CCSID
 * FROM SYSIBM.SYSDATABASE
 * WHERE NAME = 'database-name'
 *
 * Get the CCSID for a DB2 Tablespace
 * SELECT SBCS_CCSID, MIXED_CCSID, DBCS_CCSID
 * FROM SYSIBM.TABLESPACE
 * WHERE NAME = 'tablespace-name'
 *
 * Get the CCSID for a DB2 Table
 * SELECT ENCODING_SCHEME
 * FROM SYSIBM.SYSTABLES
 * WHERE NAME = 'table-name'
 *
 * Get teh CCSID for a DB2 Table Column
 * SELECT FOREIGNKEY, CCSID
 * FROM SYSIBM.SYSCOLUMNS
 * WHERE NAME = 'column-name'
 *
 */

import com.ca.rtp.auth.Credentials;
import com.ibm.db2.jcc.am.SqlInvalidAuthorizationSpecException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.util.Properties;

public class Connector {

    // Get a logger
    private static final Logger log = LogManager.getLogger(Connector.class);

    /**
     * Connect Constructor
     */
    private Connector() {
    }

    /**
     * Create a connection to DB2.
     *
     * @return 0 on success, -1 on failure
     */
    public static Connection connect(ConnectionInfo cInfo, Credentials creds, Properties clientProps) throws RtpException {
        Connection conn;

        /**
         * Load the IBM JDBC Driver.
         */
        try {
            Class.forName("com.ibm.db2.jcc.DB2Driver").newInstance();
        } catch (Exception e) {
            throw new RtpException("Failed loading class com.ibm.db2.jcc.DB2Driver", e);
        }

        /**
         * Setup the database connection.
         */
        try {
            Properties properties = new Properties();
            properties.put("user", creds.getUserid());
            properties.put("password", creds.getPassword(cInfo.getHost(), creds.getUserid()));
            properties.put("retreiveMessagesFromServerOnGetMessage", "true");
            properties.put("sendCharInputsUTF8", "1");
            properties.put("autocommit", "true");

            if (clientProps == null) {
                clientProps = new Properties();
                clientProps.put("ApplicationName", "com.ca.rtp.core.Connector.connect()");
            }

            conn = DriverManager.getConnection(cInfo.getUrl(), properties); /* Get Connection */
            conn.setClientInfo(clientProps); /* Set the client specific properties */
            log.debug("IBM DB2 Database Connected");
            return conn;

        } catch (SqlInvalidAuthorizationSpecException sia) {

            if(cInfo.getRetries() > 0) {

                log.error("The password appears to be incorrect or expired.  Please enter the correct password.");
                creds.resetPassword(cInfo.getHost(), creds.getUserid());
                creds.setPassword(cInfo.getHost(), creds.getUserid());
                cInfo.decrementRetries();
                log.info("Attempting to connect again...");
                try {
                    conn = Connector.connect(cInfo, creds, clientProps);
                    return conn;
                } catch (Exception e) {
                    throw new RtpException("DB2 Connection has failed.", e);
                }
            } else {
                throw new RtpException("Connection retry attempts have been exhausted.", sia);
            }
        } catch (Exception e) {
            log.error("DB2 Database connection has Failed");
            throw new RtpException("DB2 Connection has failed.", e);
        }
    }

    /**
     * Get a Statement for a given connection and input.
     * This can be invoked to execute any dynamic sql.
     * @param conn Connection
     * @return Statement
     */
    public static Statement createStatement(Connection conn) throws RtpException{
        Statement p;
        try {
            p = conn.createStatement();
        } catch (Exception e) {
            throw new RtpException("Error getting the statement.", e);
        }

        return p;
    }

    /**
     * Get a PreparedStatement for a given connection and input.
     * This can be invoked to execute any prepared sql.
     * @param conn Connection
     * @param input String
     * @return PreparedStatement
     */
    public static PreparedStatement createPreparedStatement(Connection conn, String input) throws RtpException {
        PreparedStatement p;
        try {
            p = conn.prepareStatement(input);
        } catch (Exception e) {
            throw new RtpException("Error getting the prepared statement.", e);
        }

        return p;
    }

    /**
     * Get a CallableStatement for a given connection and input.
     * This can be used to invoke stored procedures.
     * @param conn CallableStatement
     * @param input String
     * @return CallableStatement
     */
    public static CallableStatement createCallableStatement(Connection conn, String input) throws RtpException {
        CallableStatement c;
        try {
            c = conn.prepareCall(input);
        } catch (Exception e) {
            throw new RtpException("Error getting the callable statement.", e);
        }

        return c;
    }

    /**
     * Close the DB2 Database Connection
     *
     * @return 0 on success, -1 on failure
     */
    public static int close(Connection conn) {
        try {
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
            return -1;
        }
        return 0;
    }
}