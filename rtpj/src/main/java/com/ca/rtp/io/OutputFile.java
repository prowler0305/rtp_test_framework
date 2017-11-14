package com.ca.rtp.io;

/**
 * Created by bergr05 on 2/22/2016.
 */
public class OutputFile {

    String filepath;
    String filename;

    public OutputFile(String filepath, String filename) {
        this.filepath = filepath;
        this.filename = filename;
    }

    String getFilepath() {
        return this.filepath;
    }

    String getFilename() {
        return this.filename;
    }

    void setFilepath(String filepath) {
        this.filepath = filepath;
    }

    void setFilename(String filename) {
        this.filename = filename;
    }
}
