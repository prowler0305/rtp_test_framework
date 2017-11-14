package com.ca.rtp.examples;

import com.ca.rtp.auth.CredentialsCache;
import com.ca.rtp.core.*;
import com.ca.rtp.auth.Credentials;
import com.ca.rtp.core.utilities.RandomString;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;

import java.sql.*;
import java.util.Random;

/**
 * Example Database Driver.
 *
 * This program shows examples of executing the following:
 *
 * 1.) A simple select statement.
 * 2.) A stored procedure.
 * 3.) A batch insert.
 *
 *  DB0G Host: usilca11.ca.com port: 5130
 *  D11D Host: usilca11.ca.com port: 5258
 *  DD0G Host: usilca11.ca.com port: 5052
 * Created by bergr05 on 12/16/2015.
 */

public class ExampleDatabaseDriver {

    public static void main(String args[]){

        String userid = System.getProperty("user.name");
        String ssid = "D11D";
        String numberOfRows = "100";

        /* Create the connection info object. */
        ConnectionInfo cInfo;
        try {
            cInfo = Subsystems.getConnectionInfo(ssid);
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }

        /* Create the credentials */
        Credentials credentials = CredentialsCache.get(userid);

        /* Create the output object */
        OutputManager output = new OutputManager(OutputFormat.CSV, OutputDevice.CONSOLE);

        /* Connect to the database. */
        Connection conn;
        try {
            conn = Connector.connect(cInfo, credentials, null);
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }

        /* Execute a basic query */
        String query = "Select NAME from SYSIBM.SYSTABLES FETCH FIRST %s ROWS ONLY;";
        exampleSQLQuery(conn, query, output, numberOfRows);

        /* Execute a batch insert */
        String insert = "INSERT INTO BERGR05.GBTBL2 VALUES(?,?)";
        exampleSQLInsert(conn,insert);

        Connector.close(conn);

        /* Execute a stored procedure */
        //exampleStoredProcedure(conn, output);

    }

    /**
     * Execute an basic query without using the SelectDriver.
     * @param conn Connection
     * @param query String
     * @param output OutputManager
     * @param numberOfRows String
     * @return int
     */
    public static int exampleSQLQuery(Connection conn, String query, OutputManager output, String numberOfRows){
        int repeat = 1; /* Repeat the statement this number of times */
        boolean rc;

        try {
            for(int i = 0; i < repeat; i++) {
                if (!numberOfRows.equals("0")) {
                    System.out.println("Query: " + String.format(query, numberOfRows));
                    query = String.format(query, numberOfRows);
                } else {
                    System.out.println("Query: " + query);
                }

                CallableStatement cs;
                try {
                    cs = conn.prepareCall(query);
                    rc = cs.execute();
                    if(rc) {
                        //ResultWriter.writeResult(cs, output, summary);

                    } else {
                        System.out.println("Row not found for fetch");
                        return -1;
                    }
                } catch(SQLException e) {
                  System.out.println("Error executing the statmenet.");
                  return -1;
                }
            }
        } catch (Exception e) {
            System.out.println("SEVERE ERROR...Terminating Program Execution.");
            e.printStackTrace();
            System.exit(-1);
        }

        return 0;
    }

    public static void exampleSQLInsert(Connection conn, String insert){
        int nRows = 100; /* Repeat the statement this number of times */

        try {
            PreparedStatement pstmt = conn.prepareStatement(insert);
            Random rnd = new Random();

            for(int i = 0; i < nRows; i++){
                pstmt.setInt(1, rnd.nextInt(10));
                pstmt.setString(2, RandomString.generateAlpha(20));
                pstmt.addBatch(); // Add the data
            }

            System.out.println("Inserting: " + nRows + " Rows");
            conn.commit();
            pstmt.close();
            System.out.println("Operation successful.");
        } catch (Exception e) {
            System.out.println("ERROR...Terminating Program Execution.");
            e.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Execute a sample stored procedure
     *
     * Available stored procedures:
     * RTP.GREGLSQL - Large SQL result set.
     * RTP.GREGSSQL - Small SQL result set (100 Rows).
     *
     * @param conn Connection
     * @param output OutputManager
     */
    public static void exampleStoredProcedure(Connection conn, OutputManager output){
        int repeat = 1; /* Repeat the statement this number of times */
        CallableStatement stmt;

        try {
            for(int i = 0; i < repeat; i++) {

                stmt = conn.prepareCall("CALL RTP.GREGLSQL()");
                stmt.setQueryTimeout(3600);

                stmt.executeQuery();
                stmt.close();
            }
        } catch (Exception e) {
            System.out.println("SEVERE ERROR...Terminating Program Execution.");
            e.printStackTrace();
            System.exit(-1);
        } finally { // Always close the connection.
            try {
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException e) {
                System.out.println("Error closing Database connection.");
                e.printStackTrace();
            }
        }
    }
}
