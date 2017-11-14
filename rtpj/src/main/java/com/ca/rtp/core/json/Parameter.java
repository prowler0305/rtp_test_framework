package com.ca.rtp.core.json;

import java.util.ArrayList;

/**
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
public interface Parameter {

    /**
     * Gets the parameter's datatype.
     * @return String
     */
    String getDataType();

    /**
     * Gets the parameters type.
     * @return String
     */
    String getType();

    String getSubType();

    Object getValue();

    Arguments getArguments();

    void resetOriginalValue();

    Parameter clone();
}
