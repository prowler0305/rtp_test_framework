package com.ca.rtp.core.json;

/**
 * This class represents a Static Parameter value.
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
public class StaticParameter implements Parameter{

    private final String type;
    private final String dataType;
    private final Arguments arguments;

    StaticParameter(String type, String dataType, Arguments arguments) {
        this.type = type;
        this.dataType = dataType;
        this.arguments = arguments;
    }

    public Object getValue() {
        return arguments.getValue();
    }

    public String getType() {
        return this.type;
    }

    public void resetOriginalValue() {
        // Does nothing, the value never changes for a StaticParameter.
    }

    public String getSubType() {
        return arguments.getSubType();
    }

    public String getDataType() {
        return this.dataType;
    }

    public Arguments getArguments() {
        return this.arguments;
    }

    public Parameter clone() {
        return new StaticParameter(this.type, this.dataType, this.arguments.clone());
    }
}

