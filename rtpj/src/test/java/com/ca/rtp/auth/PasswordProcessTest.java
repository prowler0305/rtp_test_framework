//package com.ca.rtp.auth;
//
//import com.ca.rtp.auth.PasswordProcess;
//import org.junit.After;
//import org.junit.Before;
//import org.junit.Test;
//
//import static org.junit.Assert.assertEquals;
//import static org.junit.Assert.assertTrue;
//
///**
// * Created by bergr05 on 4/15/2016.
// * Copyright (c) 4/15/2016 CA Technologies. All rights reserved.
// */
//public class PasswordProcessTest {
//
//    // Test Global Variables
//    private String output;
//    private final static String PASSWORD = "thepassword";
//
//    @Before
//    public void setup(){
//        // Add test setup here
//    }
//
//    @Test
//    public void testOnlyPassword(){
//        // Add test logic here
//        output = "\r\nthepassword\r\n";
//        assertEquals(PASSWORD, PasswordProcess.parsePassword(output.trim()));
//    }
//
//    @Test
//    public void testOnlyPassword2(){
//        // Add test logic here
//        output = "\r\nthepassword";
//        assertEquals(PASSWORD, PasswordProcess.parsePassword(output.trim()));
//    }
//
//    @Test
//    public void testOnlyPassword3(){
//        // Add test logic here
//        output = "thepassword\r\n";
//        assertEquals(PASSWORD, PasswordProcess.parsePassword(output.trim()));
//    }
//
//    @Test
//    public void testWithMessages(){
//        // Add test logic here
//        output = "\r\nthis is a message\r\nand another message\r\nthepassword\r\n";
//        assertEquals(PASSWORD, PasswordProcess.parsePassword(output.trim()));
//    }
//
//    @Test
//    public void testWithMessages2(){
//        // Add test logic here
//        output = "this is a message\r\nand another message\r\nthepassword\r\n";
//        assertEquals(PASSWORD, PasswordProcess.parsePassword(output.trim()));
//    }
//
//    @After
//    public void destroy(){
//        // Add cleanup code here
//    }
//}
//
