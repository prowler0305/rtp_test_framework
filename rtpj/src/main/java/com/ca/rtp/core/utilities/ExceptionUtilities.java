package com.ca.rtp.core.utilities;

import java.io.PrintWriter;
import java.io.StringWriter;

/**
 * Created by bergr05 on 4/28/2016.
 * Copyright (c) 4/28/2016 CA Technologies. All rights reserved.
 */
public class ExceptionUtilities {

    private ExceptionUtilities() {}

    /**
     * Convert an exception stack trace to a string.
     * @param e Exception
     * @return String
     */
    public static String stacktraceToString(Exception e) {
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        e.printStackTrace(pw);
        return sw.toString();
    }
}
