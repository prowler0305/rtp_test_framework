package com.ca.rtp.core;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.io.IOException;
import java.net.*;
import java.util.Enumeration;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

/**
 * The SearchLibrary class implements utility methods for locating tests within
 * the library.
 * Created by bergr05 on 6/22/2016.
 * Copyright (c) 6/22/2016 CA Technologies. All rights reserved.
 */
public class SearchLibrary {

    // Get a logger
    private static final Logger log = LogManager.getLogger(SearchLibrary.class);
    public final static String LIBRARY = "test_library";
    public static final String FSLASH = "/";

    /**
     * Search the entire test library looking for the "target" file name.
     * @param target The filename to locate.
     * @return The relative path in the test library.
     * @throws RtpException
     */
    public static URL search(String target) throws RtpException {
        URL library = SearchLibrary.class.getResource(FSLASH + LIBRARY);
        log.debug("Internal Library location: " + library);
        log.debug("Searching internal library for test: " + target);
        log.debug("Lib:" + library.toString());

        if(library.toString().startsWith("jar:")) { // Reading from jar file.
            try {
                String jarPath = library.getPath().substring(5, library.getPath().indexOf("!"));
                final JarFile jar = new JarFile(URLDecoder.decode(jarPath, "UTF-8"));
                final Enumeration<JarEntry> entries = jar.entries();
                while (entries.hasMoreElements()) {
                    final String name = entries.nextElement().getName();
                    if (name.startsWith(LIBRARY)) {
                        if(name.substring(name.lastIndexOf(FSLASH)+1, name.length()).equals(target)) {
                            log.debug("Found test library: " + name);
                            URL test = SearchLibrary.class.getResource(FSLASH + name);
                            log.debug("Jar Test URL: " + test);
                            return test;
                        }
                    }
                }
            } catch (IOException ioe) {
                throw new RtpException("Error searching jar file for test library.", ioe);
            }
        } else {  // Reading from source.

            File test = new File("");

            try {
                File root = new File(library.toURI());
                if (root.isDirectory()) {
                    test = searchDir(root, target);
                }
            } catch (URISyntaxException e) {
                throw new RtpException("Error converting test library URL to URI", e);
            }

            if (!test.getName().equals("")) {
                return getRelativeTestPath(test);
            } else {
                throw new RtpException("The test: " + target + " could not be found within the internal test library.");
            }
        }

        throw new RtpException("The test: " + target + " could not be found within the internal test library.");
    }

    public static URL search(String path, String target) throws RtpException {
        File test = new File("");

        try {
            File root = new File(path);
            if (root.isDirectory()) {
                test = searchDir(root, target);
            }
        } catch (Exception e) {
            throw new RtpException("Error converting test library URL to URI", e);
        }

        if (!test.getName().equals("")) {
            return getRelativeTestPath(test);
        } else {
            throw new RtpException("The test: " + target + " could not be found within the internal test library.");
        }
    }

    /**
     * Searches the current directory and all sub-directories for the target.
     * @param directory starting directory
     * @param target target file name
     * @return
     */
    public static File searchDir(File directory, String target) {
        File[] files = directory.listFiles();
        File found = new File("");

        for (File file: files) {
            if (file.isDirectory()) {
                log.debug("Now Searching Directory: " + file.getName());
                found = searchDir(file, target);
                if(found.getName().equals(target)) {
                    return found;
                }
            } else {
                if (file.getName().equals(target)) {
                    log.debug("Found the test file at location: " + file.getAbsolutePath());
                    return file;
                }
            }
        }

        if (found.getName().equals(target)) {
            return found;
        } else {
            return new File("");
        }
    }

    /***
     * Converts the absolute test path into the relative library path.
     * @param test The test File.
     * @return String containing the relative library path
     */
    public static URL getRelativeTestPath(File test) throws RtpException {
        URL url;
        try {
            url = test.toURI().toURL();
        } catch (MalformedURLException e) {
            throw new RtpException("Error converting test library path name from URI to URL.", e);
        }

        return url;
    }
}
