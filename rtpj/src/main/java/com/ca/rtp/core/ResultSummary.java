package com.ca.rtp.core;

import com.ca.rtp.core.json.*;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.sql.Statement;
import java.util.ArrayList;

/**
 * Holds a Result from the execution of a DB2 JDBC query.
 * Created by schke19 on 5/18/2016.
 */
public class ResultSummary {

    // Get a logger
    private static final Logger log = LogManager.getLogger(ResultSummary.class);

    // Counters
    private int columnCount = 0;
    private int rowCount = 0;
    private String reason;
    private boolean status;
    private ArrayList<String> warnings;

    // Status
    public static final boolean PASSED = true;
    public static final boolean FAILED = false;

    // DB2 result objects
    private ResultSet resultSet;
    private ResultSetMetaData metadata;


    public ResultSummary() {
        this.status = PASSED;
        this.reason = "";
        this.warnings = new ArrayList<>();
    }

    public ResultSet getResultSet() {
        return this.resultSet;
    }

    public ResultSetMetaData getMetadata() {
        return this.metadata;
    }

    public boolean getStatus() {
        return this.status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public void setFailureReason(String reason) {
        this.reason = reason;
    }

    public String getFailureReason() {
        return this.reason;
    }

    public void setColumnCount(int columnCount) {
        this.columnCount = columnCount;
    }

    public void setRowCount(int rowCount) {
        this.rowCount = rowCount;
    }

    public int getColumnCount() {
        return columnCount;
    }

    public int getRowCount() {
        return rowCount;
    }

    public ArrayList<String> getWarnings() {
        return this.warnings;
    }

    /**
     * Process a DB2 result set.
     * @param stmt DB2 executed statement
     * @param outputManager Output object
     */
    public void processResult(Statement stmt, OutputManager outputManager, int stmtNumber) throws SQLException {

        SQLWarning warning = stmt.getWarnings();
        do {
            if (warning != null) {
                String w = warning.toString();
                this.warnings.add(w);
                warning = warning.getNextWarning();
                log.warn(w);
            }

        } while (warning != null);

        resultSet = stmt.getResultSet();
        metadata = resultSet.getMetaData();
        int colCount = metadata.getColumnCount();
        this.setColumnCount(colCount);

        if((outputManager.getDevice() == OutputDevice.CONSOLE
            || outputManager.getDevice() == OutputDevice.NONE)
            && !log.isDebugEnabled()) {
            this.setRowCount(getRowCount(resultSet));
        } else {
            ResultWriter.writeResult(stmt, outputManager, this);
        }
    }

    /**
     * Get the row count.
     * @param rs The result set.
     * @return int
     */
    public int getRowCount(ResultSet rs) {

        int i = 0;
        try {
            while (rs.next()) {
                i++;
            }
        } catch (SQLException e) {
            this.reason = e.getMessage();
            this.setStatus(ResultSummary.FAILED);
            return -1;
        }

        return i;
    }
}
