package com.ca.rtp.core.json;

import java.util.Random;

/**
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
class ParameterFactory {

    static Parameter buildParameter(String type, String datatype, Arguments arguments) {
        Parameter parm = null;
        ParameterType t = ParameterType.valueOf(type.toUpperCase());
        switch (t) {
            case GENERATED:
                parm = new GeneratedParameter(type, datatype, arguments);
                break;
            case STATIC:
                parm = new StaticParameter(type, datatype, arguments);
                break;
            case INCREMENTED:
                parm = new IncrementedParameter(type, datatype, arguments);
                break;
            default:
                break;
        }

        return parm;
    }

}
