package com.ca.rtp.core;

import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.CallableStatement;

/**
 * Created by bergr05 on 3/17/2016.
 * Copyright (c) 3/17/2016 CA Technologies. All rights reserved.
 */
public class RTPExecutor {

    // Get a logger
    private static final Logger log = LogManager.getLogger(RTPExecutor.class);

    private String user;
    private String ssid;
    private String sql;
    private SelectDriver driver;

    /**
     *  Create a basic RTP test case executor.
     * @param user The user id.
     * @param ssid The subsystem id.
     * @param sql The SQL statement to execute.
     */
    public RTPExecutor(String user, String ssid, String sql) {
        this.user = user;
        this.ssid = ssid;
        this.sql = sql;
    }

    /**
     * The execute method creates a database connection and executes the query.
     * @return The executed statement.
     */
    public CallableStatement execute() throws RtpException {

        // Open Database Connection and Execute the SQL
        driver = new SelectDriver(user, Subsystems.getConnectionInfo(ssid));
        driver.setOutputManager(OutputDevice.CONSOLE, OutputFormat.CSV);
        driver.getConnection();

        return driver.execute(sql);

    }

    /**
     * The close method closes the passed in stmt and the database connection.
     * @param stmt The active statement.
     */
    public void closeStmt(CallableStatement stmt) {

        // Close Statement
        driver.closeStmt(stmt);
    }

    /**
     * The close method closes the passed in stmt and the database connection.
     */
    public void close() {
        // Close Database Connection
        driver.closeConnection();
    }


    /**
     *  This method validates that the user and ssid are not null or blank.
     * @param user The active userid
     * @param ssid The target database subsystem.
     * @return boolean
     */
    public boolean validateUserAndSSID(String user, String ssid) {
        if(user == null) {
            log.warn("Skipping test. Missing USERID.");
            return false;
        } else if (user.equals("")) {
            log.warn("Skipping test. Userid is blank.");
            return false;
        } else if (ssid == null) {
            log.warn("Skipping test. Missing SSID.");
            return false;
        } else if (ssid.equals("")) {
            log.warn("Skipping test. SSID is blank.");
            return false;
        }

        return true;
    }
}
