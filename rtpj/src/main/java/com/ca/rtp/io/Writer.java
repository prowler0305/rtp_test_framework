package com.ca.rtp.io;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by bergr05 on 12/22/2015.
 */
public class Writer {

    // Get a logger
    private static final Logger log = LogManager.getLogger(Writer.class);

    private Writer() {
    }

    public static BufferedWriter getWriter(String path)
    {
        Path p = Paths.get(path);
        BufferedWriter writer = null;

        try {
            Charset charset = Charset.forName("UTF-8");
            writer = Files.newBufferedWriter(p, charset);
        }
        catch(IOException ioe) {
            log.error("Error writing to file {}. \n Trace: {}", path, ExceptionUtilities.stacktraceToString(ioe));
        }

        return writer;
    }
}
