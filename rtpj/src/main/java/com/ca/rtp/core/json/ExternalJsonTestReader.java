package com.ca.rtp.core.json;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.SearchLibrary;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.net.URL;

/**
 * The ExternalJsonTestReader reads a Json file or test suite from an external location.
 * Created by bergr05 on 4/19/2016.
 * Copyright (c) 4/19/2016 CA Technologies. All rights reserved.
 */
public class ExternalJsonTestReader extends JsonTestReader {

    private String path;

    public ExternalJsonTestReader(String filename, String path) {
        super(filename);
        this.path = path;
    }

    /**
     * Reads a Json test from an external library.
     * @return The root JsonNode
     * @throws RtpException
     */
    public JsonNode read() throws RtpException{

        if (!path.endsWith("\\")) {
            if (System.getProperty("os.name").contains("Windows")) {
                this.path = path + "\\";
            } else {
                this.path = path + "/";
            }
        }

        ObjectMapper objectMapper = new ObjectMapper();
        URL testFile = SearchLibrary.search(path, filename);

        // Parse the JSON file into object map
        JsonNode root;
        try {
            root = objectMapper.readTree(testFile);
        } catch (IOException ioe) {
            throw new RtpException("Error parsing file: " + testFile, ioe);
        } catch (NullPointerException npe) {
            throw new RtpException("Error reading file: " + this.filename, npe);
        }

        return root;
    }

}
