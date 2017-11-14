package com.ca.rtp.io;

/**
 * Created by bergr05 on 12/22/2015.
 */
public enum OutputFormat {
    CSV("1"),
    TABLE("2"),
    NONE("3");

    private final String value;

    OutputFormat(final String value){
        this.value = value;
    }
}
