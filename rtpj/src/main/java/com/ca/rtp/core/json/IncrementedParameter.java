package com.ca.rtp.core.json;

/**
 * This class represents a Static Parameter value.
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
public class IncrementedParameter implements Parameter{

    private final String type;
    private final String dataType;
    private final Arguments arguments;
    private final Object originalValue;
    private int randomStart;

    IncrementedParameter(String type, String dataType, Arguments arguments) {
        this.type = type;
        this.dataType = dataType;
        this.arguments = arguments;
        this.originalValue = arguments.getValue();
        this.randomStart = -1;
    }

    public Object getValue() {

        // Check if an integer starting place is to be randomized within a range.
        if (dataType.equals("INTEGER")) {
            if (arguments.getRandomize()) {
                randomizeStart();
            }
        }

        return arguments.getValue();
    }

    public void resetOriginalValue() {
        this.arguments.setValue(originalValue);
    }

    public String getType() {
        return this.type;
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

    public void increment() {
        if (dataType.equals("INTEGER"))

            arguments.setValue((int) arguments.getValue() + 1);

            // Check if we have gone past the max
            if ((int)arguments.getValue() == arguments.getMax()+1) {
                arguments.setValue(this.originalValue);  // If so, reset to the original value.
            }
    }

    public void randomizeStart() {
        if (randomStart == -1 || ((int) arguments.getValue()) == randomStart) {
            // Start the random location
            this.randomStart = arguments.getRandom().nextInt(arguments.getMax() - (int) this.originalValue + 1) + (int) this.originalValue;
            arguments.setValue(randomStart);
        }
    }


    @Override
    public Parameter clone() {
        return new IncrementedParameter(this.type, this.dataType, this.arguments.clone());
    }
}

