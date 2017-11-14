package com.ca.rtp.examples;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.Subsystems;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;
import com.ca.rtp.core.SelectDriver;

import java.sql.CallableStatement;

/**
 * This class is an example of using the SelectDriver class.
 * Created by bergr05 on 2/22/2016.
 */
public class ExampleSelectDriver {

    /**
     * Example for executing a simple SELECT statement.
     * @param args
     *
     *  DB0G Host: usilca11.ca.com port: 5130
     *  D11D Host: usilca11.ca.com port: 5258
     *  DD0G Host: usilca11.ca.com port: 5052
     */
    public static void main(String args[]) {

        String user = System.getProperty("user.name");
        String ssid = "DB0G";

        String query = "Select CREATOR, NAME from SYSIBM.SYSTABLES FETCH FIRST 100 ROWS ONLY";
        SelectDriver driver;

        try {
            driver = new SelectDriver(user, Subsystems.getConnectionInfo(ssid));
            driver.setOutputManager(OutputDevice.CONSOLE, OutputFormat.CSV);
            driver.getConnection();
        } catch (RtpException rtpe) {
            rtpe.print();
            return;
        }

        try {
            CallableStatement stmt = driver.execute(query);
            driver.closeStmt(stmt);
        } catch (RtpException rtpe) {
            rtpe.print();
        } finally {
            driver.closeConnection();
        }
    }
}
