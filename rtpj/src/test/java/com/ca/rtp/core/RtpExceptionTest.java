package com.ca.rtp.core;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertTrue;

/**
 * Created by bergr05 on 4/19/2016.
 * Copyright (c) 4/19/2016 CA Technologies. All rights reserved.
 */
public class RtpExceptionTest {

    // Test Global Variables
    private Object a = null;
    @Before
    public void setup(){
        // Add test setup here
    }

    @Test
    public void test(){
        // test logic here
        try {
           System.out.println(a.toString());
        } catch(NullPointerException npe) {
            RtpException rtpe = new RtpException("RtpException JUNIT Test.", npe);
            try {
                rtpe.print();
                assertTrue(true);
            } catch(Exception e) {
                assertTrue(false);
            }
        }
    }

    @After
    public void destroy(){
        // Add cleanup code here
    }
}
