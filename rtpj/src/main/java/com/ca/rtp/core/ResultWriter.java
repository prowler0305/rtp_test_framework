package com.ca.rtp.core;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.io.OutputManager;
import com.ca.rtp.io.Writer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.nio.charset.UnmappableCharacterException;
import java.sql.*;
import java.io.BufferedWriter;

/**
 * Created by bergr05 on 12/22/2015.
 *
 * This class prints the sql result as a csv file.
 * The output can be sent to:
 *   1.) The console.
 *   2.) ?
 */
public class ResultWriter {

    // Get a logger
    private static final Logger log = LogManager.getLogger(ResultWriter.class);

    private ResultWriter() {

    }

    /**
     * Write the result output to the console as a .csv or a tabular format.
     * @param stmt Statement
     */
    public static void writeResult(Statement stmt, OutputManager output, ResultSummary summary) throws SQLException {
        BufferedWriter writer = null;

        if (output.getDevice() == OutputDevice.FILE) {
            writer = Writer.getWriter(output.getFile());
        }

        //try {

            ResultSetMetaData metadata = summary.getMetadata();
            ResultSet rs = summary.getResultSet();
            int colCount = metadata.getColumnCount();

            String columns = "";
            int totalSize = 0;

            for (int j = 0; j < colCount; j++) {
                String name = metadata.getColumnName(j + 1);

                switch(output.getFormat()) {
                    case CSV:
                        if (j == (colCount - 1)) {
                            columns = columns + name;
                        } else {
                            columns = columns + name + ",";
                        }
                        break;
                    case TABLE:
                        int colSize = metadata.getColumnDisplaySize(j + 1);
                        int diff = colSize - name.length();
                        String pad = "";
                        if (diff > 0) {
                            pad = copies(diff + 1, " ");
                        }
                        columns = columns + name + pad;
                        totalSize += colSize;
                        break;
                    case NONE:
                        break;
                    default:
                        break;
                }
            }

            write(writer, "Results", output.getDevice());
            write(writer, columns, output.getDevice());

            if(output.getFormat() == OutputFormat.TABLE) {
                final String dashLine = copies(totalSize, "-");
                write(writer, dashLine, output.getDevice());
            }

            int totalRowCount = 0;
            int partialRowCount;
            boolean more = true;

            while(more) {
                partialRowCount = writePartialResult(rs, metadata, output, writer);

                if (partialRowCount != -1) {
                    totalRowCount += partialRowCount;
                } else {
                    log.error("Error writing part of the result set.");
                }

                if(!stmt.getMoreResults()){
                    more = false;
                } else {
                    log.info("*************GETTING MORE RESULTS FROM SERVER.***********************");
                }
            }

            summary.setRowCount(totalRowCount); // Set the total row count.

            if(output.getFormat() == OutputFormat.CSV) {
                write(writer, "Rows Fetched," + totalRowCount, output.getDevice());
            } else if(output.getFormat() == OutputFormat.TABLE) {
                write(writer, "Rows Fetched:" + totalRowCount, output.getDevice());
            } else {
                write(writer, "Rows Fetched:" + totalRowCount, OutputDevice.CONSOLE);
            }

            if(output.getDevice() == OutputDevice.FILE) {
                try {
                    if (writer != null) {
                        writer.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    return;
                }
            }

//        } catch(SQLDataException sde) {
//            log.error("A data exception has occurred. \n Trace {}", ExceptionUtilities.stacktraceToString(sde));
//            summary.setStatus(ResultSummary.FAILED);
//            summary.setFailureReason(sde.getMessage());
//            return;
//        } catch(SQLException se) {
//            log.error("Error printing the result. \n Trace {}", ExceptionUtilities.stacktraceToString(se));
//            summary.setStatus(ResultSummary.FAILED);
//            summary.setFailureReason(se.getMessage());
//            return;
//        } catch(Exception e){
//            log.error("Error printing the result. \n Trace {}", ExceptionUtilities.stacktraceToString(e));
//            summary.setStatus(ResultSummary.FAILED);
//            summary.setFailureReason(e.getMessage() + e.getCause().getMessage());
//            return;
//        }
    }

    /**
     * Process a partial result set.
     * @param rs Result set
     * @param metadata Result metadata
     * @param output output of request
     * @return On Success: total rows fetched, On Error: -1
     */
    private static int writePartialResult(ResultSet rs,
                                          ResultSetMetaData metadata,
                                          OutputManager output,
                                          BufferedWriter writer) throws SQLException
    {
        int rowCount = 0;

        int colCount = metadata.getColumnCount();
        while (rs.next()) {
            String row = "";
            for (int j = 0; j < colCount; j++) {
                String value = rs.getString(j + 1);
                if (value == null) // If we found a NULL in the column
                    value = "NULL"; // Set the string to something we can display

                switch (output.getFormat()) {
                    case CSV:
                        if (j == (colCount - 1)) {
                            row = row + value;
                        } else {
                            row = row + value + ",";
                        }
                        break;
                    case TABLE:
                        int colSize = metadata.getColumnDisplaySize(j + 1);
                        int diff = colSize - value.length();
                        String pad = "";
                        if (diff > 0) {
                            pad = copies(diff + 1, " ");
                        }
                        row = row + value + pad;
                        break;
                    case NONE:
                        break;
                    default:
                        break;
                }
            }

            if (writer != null) {
                write(writer, row, output.getDevice());
            } else {
                write(row, output.getDevice());
            }

            rowCount++;
        }

        return rowCount;
    }

    /**
     * Returns a string with a value repeated x number of times.
     * @param x - The number of copies of the string.
     * @param value - The string to be repeated.
     * @return String
     */
    private static String copies(int x, String value) {
       return new String(new char[value.length()*x]).replace("\0", value);
    }

    /**
     * Writes a line to the open file writer.
     * @param writer BufferedWriter
     * @param line String
     * @return 0 for success, -1 for failure.
     */
    private static int writeToFile(BufferedWriter writer, String line) {
        try{
            writer.write(line +"\n");
        } catch(UnmappableCharacterException uce) {
            log.error("Error writing to file. \n Trace: {}", ExceptionUtilities.stacktraceToString(uce));
            return 0;
        }catch(IOException ioe) {
            log.error("Error writing to file. \n Trace: {}", ExceptionUtilities.stacktraceToString(ioe));
            return -1;
        }catch(Exception e){
            log.error("Error writing to file. \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
            return -1;
        }
        return 0;
    }

    /**
     * Writes the output to the desired device.
     * @param writer BufferedWriter
     * @param line String
     * @param device OutputDevice
     * @return int
     */
    private static int write(BufferedWriter writer, String line, OutputDevice device) {
        int rc = 0;

        switch(device){
            case NONE:
                break;
            case FILE:
                rc = writeToFile(writer,line);
                break;
            case CONSOLE:
                log.trace(line);
                break;
                //Default behavior.
            default:
                log.trace(line);
                break;
        }

        return rc;
    }

    /**
     * Writes the output to the desired device.
     * @param line String
     * @param device OutputDevice
     * @return int
     */
    private static int write(String line, OutputDevice device) {
        int rc = 0;

        switch(device){
            case NONE:
                break;
            case CONSOLE:
                log.trace(line);
                break;
            default:
                log.trace(line);
                break;
        }

        return rc;
    }
}
