package com.ca.rtp.core;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.CallableStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;

/**
 * Created by bergr05 on 2/23/2016.
 */
public class ResultSetManager {

    // Get a logger
    private static final Logger log = LogManager.getLogger(ResultSetManager.class);

    private CallableStatement stmt;
    private ArrayList<String> columns;

    public ResultSetManager(CallableStatement stmt){
        this.columns = new ArrayList<>();
        this.stmt = stmt;
    }

    /**
     * Get the next row of the result set.
     * @return ArrayList<String>
     */
    public ArrayList<String> getNextRow() {
        ArrayList<String> row = null;
        try {
            ResultSet rs = stmt.getResultSet();
            if(rs.next()) {
                row = new ArrayList<>();
                int colCount = stmt.getMetaData().getColumnCount();
                for (int i = 0; i < colCount; i++) {
                    row.add(rs.getString(i + 1));
                }
            }
        } catch (SQLException e) {
            log.error("Error retrieving next row. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            return null;
        }

        return row;
    }

    /**
     * Get the result set columns.
     * @return ArrayList<String>
     */
    public ArrayList<String> getColumns() {
        ArrayList<String> columns = new ArrayList<>();
        try {
            ResultSetMetaData metadata = stmt.getMetaData();
            int colCount = metadata.getColumnCount();

            for (int i = 0; i < colCount; i++) {
                columns.add(metadata.getColumnName(i + 1));
            }
        } catch (SQLException e) {
            log.error("Error getting stmt metadata. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            return null;
        }
        return columns;
    }

    /**
     * Reset the cursor to the first row.
     */
    public void reset() {
        try {
            this.stmt.getResultSet().beforeFirst();
        } catch (SQLException e) {
            log.error("Error resetting the result set cursor. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
        }
    }
}
