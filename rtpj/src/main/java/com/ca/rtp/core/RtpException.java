package com.ca.rtp.core;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.PrintWriter;
import java.io.StringWriter;

/**
 * Created by bergr05 on 4/18/2016.
 * Copyright (c) 4/18/2016 CA Technologies. All rights reserved.
 */
public class RtpException extends Exception {

    // Get a logger
    private static final Logger log = LogManager.getLogger(RtpException.class);


    public RtpException() {
        super();
    }

    public RtpException(String message) {
        super(message);
    }

    public RtpException(String message, Throwable cause) {
        super(message, cause);
    }

    /**
     * Print out diagnostic information about the RtpException.
     * @return
     */
    public void print() {

        String template = "\nRTPException Details: \n Message: %s \n Cause: %s \n StackTrace:\n %s";

        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        this.printStackTrace(pw);

        String trace = sw.toString();
        template = String.format(template, this.getMessage(), this.getCause(), trace);

        log.error(template);

    }

}
