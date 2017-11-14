package com.ca.rtp.core.utilities;

import com.ca.rtp.core.RtpException;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.core.config.Configurator;

/**
 * The RtpLogger performs and required programmatic log4j2 changes.
 * Created by bergr05 on 4/28/2016.
 * Copyright (c) 4/28/2016 CA Technologies. All rights reserved.
 */
public class RtpLogger {

    private RtpLogger() throws RtpException{
        throw new RtpException("Cannot instantiate class RtpLogger");
    }

    public static void init() {
        System.setProperty("Log4jContextSelector", "org.apache.logging.log4j.core.async.AsyncLoggerContextSelector");
    }

    public static void changeLevel(String level) {
        Configurator.setRootLevel(Level.valueOf(level));
    }
}
