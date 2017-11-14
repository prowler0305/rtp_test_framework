package com.ca.rtp.core.json;

import com.ca.rtp.core.RtpException;
import com.ca.rtp.core.SearchLibrary;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.net.URL;

/**
 * Created by bergr05 on 4/19/2016.
 * Copyright (c) 4/19/2016 CA Technologies. All rights reserved.
 */
public class JsonTestReader {

    protected String filename;

    public JsonTestReader(String filename) {
        this.filename = filename;
    }

    public JsonNode read() throws RtpException {

        // Search the library for the target file.
        URL testURL = SearchLibrary.search(filename);

        ObjectMapper objectMapper = new ObjectMapper();

        // Parse the JSON file into object map
        JsonNode root;
        try {
            root = objectMapper.readTree(testURL);
        } catch (IOException ioe) {
            throw new RtpException("Error parsing file: " + testURL, ioe);
        } catch (NullPointerException npe) {
            throw new RtpException("Error reading file: " + filename, npe);
        }

        return root;
    }

}
