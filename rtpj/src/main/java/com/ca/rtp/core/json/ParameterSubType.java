package com.ca.rtp.core.json;

/**
 * Created by schke19 on 4/18/2016.
 * Copyright (c) 4/18/2016 CA Technologies. All rights reserved.
 */
enum ParameterSubType {
    OUT("OUT"),
    INOUT("INOUT");

    private final String value;

    ParameterSubType(final String value){
        this.value = value;
    }

    public String toString() {
        return this.value;
    }
}
