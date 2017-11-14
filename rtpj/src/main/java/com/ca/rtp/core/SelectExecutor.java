package com.ca.rtp.core;

import com.ca.rtp.core.SelectDriver;
import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.CallableStatement;
import java.sql.SQLException;

/**
 * This class is used to execute a select statement on its own thread.
 * Created by bergr05 on 2/22/2016.
 */
public class SelectExecutor implements Runnable {

    // Get a logger
    private static final Logger log = LogManager.getLogger(SelectExecutor.class);

    private SelectDriver driver;
    private String query;
    private static int closed = 0;
    private static int opened = 0;
    private static final Object lock = new Object();

    public SelectExecutor(SelectDriver driver, String query) {
        this.driver = driver;
        this.query = query;
    }

    public void run() {
        try {
            driver.getConnection();
        } catch(RtpException rtpe) {
            rtpe.print();
            return;
        }

        incrementOpened();
        try {
            CallableStatement stmt = driver.execute(query);
            driver.closeStmt(stmt);
        } catch (Exception e) {
            log.error("***** Unknown Exception ***** \n Trace: {}", ExceptionUtilities.stacktraceToString(e));
        } finally {
            driver.closeConnection();
            incrementClosed();
        }
    }

    private static void incrementClosed() {
        synchronized(lock) {
            closed++;
        }
    }

    private static void incrementOpened() {
        synchronized(lock) {
            opened++;
        }
    }

    public static int getClosed() {
        return closed;
    }

    public static int getOpened() {
        return opened;
    }
}
