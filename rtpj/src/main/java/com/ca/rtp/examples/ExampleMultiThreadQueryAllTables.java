package com.ca.rtp.examples;

import com.ca.rtp.core.*;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;

import java.sql.CallableStatement;
import java.util.ArrayList;

/**
 * This class is an example of multithreaded queries against all the catalog tables.
 * Created by bergr05 on 2/23/2016.
 */
public class ExampleMultiThreadQueryAllTables {

    public static void main(String args[]) {

        String username = System.getProperty("user.name");
        String ssid = "DB0G";
        String count = "400";
        String query = "Select CREATOR, NAME from SYSIBM.SYSTABLES WHERE TYPE='T' NAME NOT LIKE 'SYS%' FETCH FIRST &rowcount ROWS ONLY";
        String tableQuery = "SELECT * FROM %s FETCH FIRST 1 ROWS ONLY";

        SelectDriver driver;
        try {
            driver = new SelectDriver(username, Subsystems.getConnectionInfo(ssid));
            driver.setOutputManager(OutputDevice.NONE, OutputFormat.NONE);
            driver.getConnection();
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }

        CallableStatement stmt;
        try {
            stmt = driver.execute(query.replace("&rowcount", count));
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        } finally {
            driver.closeConnection();
        }

        ResultSetManager rsm = new ResultSetManager(stmt);
        ArrayList<String> row;

        int j = 1;
        do {
            row = rsm.getNextRow();
            if(row != null) {
                String table = row.get(0).trim() + "." + row.get(1).trim();
                String nextQuery = String.format(tableQuery, table);
                SelectDriver driver2;
                try {
                    driver2 = new SelectDriver(username, Subsystems.getConnectionInfo(ssid));
                } catch (RtpException rtpe) {
                    rtpe.print();
                    return;
                }

                driver2.setOutputManager(OutputDevice.NONE, OutputFormat.NONE);
                System.out.println("Executing Query: " + nextQuery);
                SelectExecutor se = new SelectExecutor(driver2, nextQuery);
                (new Thread(se)).start();
                j++;
            }

        } while (row != null);

        try {
            Thread.sleep(1000);
        } catch (Exception e) {
            System.out.println("Error sleeping.");
        }

        System.out.println("Connections Opened:" + SelectExecutor.getOpened());
        System.out.println("Connections Closed:" + SelectExecutor.getClosed());

        driver.closeStmt(stmt);
        driver.closeConnection();
    }
}
