package com.ca.rtp.io;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by bergr05 on 2/19/2016.
 */
public class Reader {

    // Get a logger
    private static final Logger log = LogManager.getLogger(Reader.class);

    private Reader(){}

    public static BufferedReader getReader(String path) {
        Path p = Paths.get(path);
        BufferedReader reader = null;

        try {
            InputStream in = Files.newInputStream(p);

            reader = new BufferedReader(new InputStreamReader(in));
        }
        catch(IOException ioe) {
            log.error("Error reading from file {}. \n Trace: {}", path, ExceptionUtilities.stacktraceToString(ioe));
        }

        return reader;
    }
}

