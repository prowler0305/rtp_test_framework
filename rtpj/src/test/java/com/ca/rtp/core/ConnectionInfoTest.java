package com.ca.rtp.core;

/**
 * Created by bergr05 on 3/15/2016.
 */

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class ConnectionInfoTest {

    private String URL = "jdbc:db2://CA11:5045/D10APTIB:emulateParameterMetaDataForZCalls=1;";
    private String host = "CA11";
    private String ssid = "D10A";
    private String port = "5045";
    private ConnectionInfo ci;

    @Before
    public void setup(){
        ci = new ConnectionInfo(ssid, host, port);
    }

    @Test
    public void validateConnectionInfo(){
        assertEquals(ci.getHost(), host);
        assertEquals(ci.getPort(), port);
        assertEquals(ci.getSSID(), ssid);
        assertEquals(ci.getUrl(), URL);
    }

    @After
    public void destroy(){
        ci = null;
    }
}
