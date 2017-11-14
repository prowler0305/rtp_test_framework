package com.ca.rtp.core.json;

/**
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
enum ParameterType {
    GENERATED("GENERATED"),
    STATIC("STATIC"),
    INCREMENTED("INCREMENTED"),
    NONE("NONE");

    private final String value;

    ParameterType(final String value){
        this.value = value;
    }

    public String toString() {
        return this.value;
    }
}
