package com.ca.rtp.examples;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.SelectDriver;
import com.ca.rtp.core.SelectExecutor;
import com.ca.rtp.core.Subsystems;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Example for executing a query over multiple threads.
 * Created by bergr05 on 2/18/2016.
 */
public class ExampleMultiThreadedSelect {

    public static void main(String args[]) {

        String username = System.getProperty("user.name");
        String ssid = "D11D";
        int count = 10;

        String query = "Select NAME, CREATOR from SYSIBM.SYSTABLES, SYSIBM.SYSTABLESPACE FETCH FIRST %s ROWS ONLY;";

        for(int i = 0; i < count; i++) {
            SelectDriver driver;
            try {
                driver = new SelectDriver(username, Subsystems.getConnectionInfo(ssid));
            } catch (RtpException rtpe) {
                rtpe.print();
                return;
            }

            SelectExecutor se = new SelectExecutor(driver, String.format(query, i+1));
            (new Thread(se)).start();
        }
    }
}
