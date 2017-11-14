package com.ca.rtp.tests;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.RtpTest;
import com.ca.rtp.core.SelectDriver;
import com.ca.rtp.core.Subsystems;
import com.ca.rtp.core.utilities.RtpLogger;
import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;

import java.sql.CallableStatement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

/**
 * This is a RTP Test program that can be executed via the TestRunner.
 * Created by bergr05 on 2/25/2016.
 */
public class SelectDriverTest implements RtpTest {

    public boolean invoke(HashMap<String,String> parms) {

        String user = parms.get("USERID");
        String ssid = parms.get("SSID");
        String lvl = parms.get("LOG");
        RtpLogger.changeLevel(lvl);

        if(user == null) {
            System.out.println("Skipping test. Missing USERID.");
            return false;
        } else if(ssid == null) {
            System.out.println("Skipping test. Missing SSID.");
            return false;
        }

        Random rand = new Random(System.nanoTime());


        for (int i = 0; i < 1000; i++) {

            SelectDriver driver;
            try {
                driver = new SelectDriver(user, Subsystems.getConnectionInfo(ssid));
                driver.setOutputManager(OutputDevice.NONE, OutputFormat.NONE);
                driver.getConnection();
            } catch (RtpException rtpe) {
                rtpe.print();
                return false;
            }

            String query = "Select COLCOUNT from SYSIBM.SYSTABLES WHERE COLCOUNT < %s FETCH FIRST 1 ROWS ONLY";
            int j = rand.nextInt();
            query = String.format(query, j);

            try {
                CallableStatement stmt = driver.execute(query);
                driver.closeStmt(stmt);
            } catch (Exception e) {
                System.out.println("Error executing statement.");
                e.printStackTrace();
                driver.closeConnection();
                return false;
            } finally {
                driver.closeConnection();
            }
        }

        return true;
    }

}
