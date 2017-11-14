package com.ca.rtp.io;

import com.ca.rtp.io.OutputDevice;
import com.ca.rtp.io.OutputFormat;

/**
 * Created by bergr05 on 1/6/2016.
 */
public class OutputManager {

    private OutputFormat format;
    private OutputDevice device;
    private String filepath;
    private String filename;

    /**
     * OutputManager constructor
     * @param format Output format
     * @param device Output device
     */
    public OutputManager(OutputFormat format, OutputDevice device){
        this.format = format;
        this.device = device;
        this.filepath = System.getProperty("user.dir");
        setFilename("RTP_Result");
    }

    /**
     * Getters
     */
    public OutputFormat getFormat() {
        return this.format;
    }

    public OutputDevice getDevice() {
        return this.device;
    }

    public String getFilepath() {
        return this.filepath;
    }

    public String getFilename() {
        return this.filename;
    }

    /**
     * Returns the output file.  If the output file is null, the default file path is returned.
     * "user.dir\rtpResult"
     * @return String
     */
    public String getFile() {
        String ext;
        if (this.format == OutputFormat.CSV) {
            ext = ".csv";
        } else {
            ext = ".txt";
        }

        return this.filepath + "\\" + this.filename + ext;
    }

    /**
     * Setters
     */
    public void setFormat(OutputFormat format) {
        this.format = format;
    }

    public void setDevice(OutputDevice device) {
        this.device = device;
    }

    public void setFilepath(String filepath) {
        this.filepath = filepath;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }
}
