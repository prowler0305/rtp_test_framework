package com.ca.rtp.core.json;

import java.util.ArrayList;

/**
 * The Statement class maps a RTP Database statement to execute.
 *
 * Created by bergr05 on 3/23/2016.
 * Copyright (c) 3/23/2016 CA Technologies. All rights reserved.
 */
public class Statement {

    private final ArrayList<Parameter> parameterList;
    private String text;
    private final String type;
    private final String subType;
    private final int repeat;
    private final int batches;
    public final int sleep;
    private final Expectations expectations;

    public Statement(String text, String type, String subType, int repeat, Expectations expectations, ArrayList<Parameter> parameterList, int sleep, int batches) {

        this.text = text;
        this.type = type;
        this.subType = subType;
        this.repeat = repeat;
        this.expectations = expectations;
        this.parameterList = parameterList;
        this.sleep = sleep;
        this.batches = batches;
    }

    /**
     * Get the statement text.
     * @return String
     */
    public String getText() {
        return this.text;
    }

    /**
     * Get the statement type
     * @return String
     */
    public String getType() {
        return this.type;
    }

    /**
     * Get the statement subType.
     * @return String
     */
    public String getSubType() {
        return this.subType;
    }

    /**
     * Get the statement repeat value.
     * @return int
     */
    public int getRepeat() {
        return this.repeat;
    }

    /**
     * Get the statement repeat value.
     * @return int
     */
    public int getBatches() {
        return this.batches;
    }

    /**
     * Get the statement expect value.
     * @return Expectations
     */
    public Expectations getExpectations() {
        return this.expectations;
    }

    /**
     * Get the statement parameterList
     * @return ArrayList<Parameter>
     */
    public ArrayList<Parameter> getParameterList() {
        return this.parameterList;
    }

    public void setText(String text) {
        this.text = text;
    }

    /**
     * Clones the current statement object.
     * @return Statement
     */
    @Override
    public Statement clone() {
        ArrayList<Parameter> parmList = new ArrayList<>();

        for(Parameter parm : this.parameterList) {
            parmList.add(parm.clone());
        }

        return new Statement(this.text, this.type, this.subType, this.repeat, this.expectations.clone(), parmList, this.sleep, this.batches);

    }

}
