package com.ca.rtp.core.json;

/**
 * Created by bergr05 on 4/14/2016.
 * Copyright (c) 4/14/2016 CA Technologies. All rights reserved.
 *
 * The ArgumentTypes ENUM describes all the available RTP Test JSON arguments.
 *
 * VALUE       - The static value of a parameter.
 * DATATYPE    - The parameter datatype.
 * TYPE        - The parameter type. I.E Static, Generated
 * LENGTH      - The parameter length.
 * PRECISION   - A numeric parameter's precision.
 * SCALE       - A numeric parameter's scale.
 * SEED        - A seed value used with Generated parameters.
 * KEY         - A value used as an identifier for replacing literals.
 * MAX         - A value used to determine the maximum number a literal parameter should be incremented to before
 *               starting back at the initial value.
 * DESCRIPTION - An optional text string used to better document a given parameter.
 *
 */
public enum ArgumentTypes {

    VALUE("VALUE"),
    DATATYPE("DATATYPE"),
    TYPE("TYPE"),
    SUBTYPE("SUBTYPE"),
    LENGTH("LENGTH"),
    PRECISION("PRECISION"),
    SCALE("SCALE"),
    SEED("SEED"),
    KEY("KEY"),
    MAX("MAX"),
    RANDOMIZE("RANDOMIZE"),
    DESCRIPTION("DESCRIPTION"),
    NONE("NONE");

    private final String value;

    ArgumentTypes(final String value){
        this.value = value;
    }

    @Override
    public String toString() {
        return this.value;
    }

}
