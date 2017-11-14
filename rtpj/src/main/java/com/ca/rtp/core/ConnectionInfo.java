package com.ca.rtp.core;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Created by bergr05 on 2/18/2016.
 *
 * This class wraps all the required connection information used on the database connection.
 */
public class ConnectionInfo {

    // Get a logger
    private static final Logger log = LogManager.getLogger(ConnectionInfo.class);

    private String URL;
    private final String host;
    private final String ssid;
    private final String port;
    private int retries;

    /**
     * Connect Constructor
     * @param ssid Subsystem id.
     * @param host Subsystem Host DNS name or ip address.
     * @param port Subsystem TCP/IP port.
     */
    public ConnectionInfo(String ssid,
                          String host,
                          String port) {
        this.retries = 1;
        this.ssid = ssid;
        this.host = host;
        this.port = port;
        this.URL = "jdbc:db2://%s:%s/%sPTIB:emulateParameterMetaDataForZCalls=1;";
        updateUrl();
    }

//    /**
//     * Sets the Host variable
//     */
//    public void setHost(String host){
//        this.host = host;
//    }
//
//    /**
//     * Sets the port variable
//     */
//    public void setPort(String port){
//        this.port = port;
//    }
//
//    /**
//     * Sets the database variable
//     */
//    public void setSSID(String ssid){
//        this.ssid = ssid;
//    }

    /**
     * Decrement the retries value by 1 and return the original value.
     * @return int
     */
    public int decrementRetries(){
        int t = retries;
        this.retries--;
        return t;
    }

    /**
     * Increment the retries value by 1 and return the original value.
     * @return int
     */
    public int incrementRetries(){
        int t = retries;
        this.retries++;
        return t;
    }

    /**
     * Gets the Host variable
     * @return String
     */
    public String getHost(){
        return this.host;
    }

    /**
     * Gets the database variable
     * @return String
     */
    public String getSSID(){
        return this.ssid;
    }

    /**
     * Gets the port variable
     * @return String
     */
    public String getPort(){
        return this.port;
    }

    /**
     * Gets the URL variable
     * @return String
     */
    public String getUrl(){
        return this.URL;
    }

    /**
     * Gets the retries value.
     * @return int
     */
    public int getRetries(){
        return this.retries;
    }

    /**
     * Format the connection URL using the current ssid, host, port.
     */
    public void updateUrl() {
        String copy = "";
        try {
            copy = this.URL;
            this.URL = String.format(this.URL, this.host, this.port, this.ssid);
        } catch (Exception e) {
            log.error("Failed to format the Database connection URL. \n Trace: {}" + ExceptionUtilities.stacktraceToString(e));
            this.URL = copy; /* Reset to original string */
        }
    }

    /**
     * Clones the current ConnectionInfo object with the exception of the retries class variable.
     * @return ConnectionInfo
     */
    @Override
    public ConnectionInfo clone() {
        return new ConnectionInfo(this.ssid, this.host, this.port);
    }
}
