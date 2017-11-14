package com.ca.rtp.io;

/**
 * Created by bergr05 on 12/22/2015.
 */
public enum OutputDevice {
    CONSOLE("1"),
    FILE("2"),
    NONE("3");

    private final String value;

    OutputDevice(final String value){
        this.value = value;
    }
}

