package com.ca.rtp.core.json;

/**
 * Created by bergr05 on 4/18/2016.
 * Copyright (c) 4/18/2016 CA Technologies. All rights reserved.
 */
public enum StatementTypes {

    TEXT("VALUE"),
    TYPE("TYPE"),
    SUBTYPE("SUBTYPE"),
    ARGS("ARGS"),
    REPEAT("REPEAT"),
    EXPECT("EXPECT"),
    SLEEP("SLEEP"),
    BATCHES("BATCHES"),
    DESCRIPTION("DESCRIPTION"),
    NONE("NONE");

    private final String value;

    StatementTypes(final String value){
        this.value = value;
    }

    @Override
    public String toString() {
        return this.value;
    }

}

