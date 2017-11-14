package com.ca.rtp.core.json;

/**
 * Created by schke19 on 5/16/2016.
 * Copyright (c) 5/16/2016 CA Technologies. All rights reserved.
 */
public class Expectations {

    private Integer sqlerror;
    private Integer rows;
    private Integer columns;
    public final boolean ignore;

    public Expectations(){
        sqlerror = 0;
        rows = -1;
        columns = -1;
        ignore = false;

    }

    public Expectations(Integer sqlerror, Integer rows, Integer columns, boolean ignore){
        this.sqlerror = sqlerror;
        this.rows = rows;
        this.columns = columns;
        this.ignore = ignore;
    }

    public Integer getSqlerror() {
        return sqlerror;
    }

    public void setSqlerror(Integer sqlerror) {
        this.sqlerror = sqlerror;
    }

    public Integer getRows() {
        return rows;
    }

    public void setRows(Integer rows) {
        this.rows = rows;
    }

    public Integer getColumns() {
        return columns;
    }

    public void setColumns(Integer columns) {
        this.columns = columns;
    }

    /**
     * Creates a clone of the current Expectations object.
     * @return Expectations
     */
    @Override
    public Expectations clone() {
        return new Expectations(new Integer(sqlerror.intValue()), new Integer(rows.intValue()), new Integer(columns.intValue()), ignore);
    }
}
