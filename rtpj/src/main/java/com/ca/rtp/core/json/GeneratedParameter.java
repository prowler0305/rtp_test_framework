package com.ca.rtp.core.json;

import com.ca.rtp.core.utilities.RandomString;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by bergr05 on 3/22/2016.
 * Copyright (c) 3/22/2016 CA Technologies. All rights reserved.
 */
public class GeneratedParameter implements Parameter {

    // Get a logger
    private static final Logger log = LogManager.getLogger(GeneratedParameter.class);

    private final String type;
    private final String dataType;
    private final Arguments arguments;
    private final Object originalValue;

    GeneratedParameter(String type, String dataType, Arguments arguments) {
        this.type = type;
        this.dataType = dataType;
        this.arguments = arguments;
        this.originalValue = arguments.getValue();
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

    /**
     * Reset the arguments value to the original value.
     */
    public void resetOriginalValue() {
        this.arguments.setValue(this.originalValue);
    }

    public Object getValue() {
        //Possibly make two child classes; one for incrementing

        // Call appropriate getter based on datatype
        switch (dataType) {
            case "BIGINT":
                return (long) Math.abs(arguments.getRandom().nextInt());
            case "BOOLEAN":
                return arguments.getRandom().nextBoolean();
            case "CHAR":
                return getString(arguments.getLength());
            case "DOUBLE":
                return arguments.getRandom().nextDouble(); // 0.0 and 1.0 (probably should be multiplied out)
            case "FLOAT":
                return Math.abs(arguments.getRandom().nextFloat()); // Same thing as Double (make sure you take precision into account)
            case "INTEGER":
                return Math.abs(arguments.getRandom().nextInt());
            case "SMALLINT":
                return (short) Math.abs(arguments.getRandom().nextInt());
            case "TINYINT":
                return (byte) Math.abs(arguments.getRandom().nextInt());
            case "VARCHAR":
                return getString(arguments.getLength());
            case "DATE":
                // Create a new Date object.
                GregorianCalendar cal = new GregorianCalendar();

                // Randomize the Date, starting with the year (present-100) : present), then the month (0:11), then the day (1 : days in month).
                cal.set(GregorianCalendar.YEAR,
                        ThreadLocalRandom.current().nextInt(Calendar.getInstance().get(Calendar.YEAR) - 100, Calendar.getInstance().get(Calendar.YEAR)));
                cal.set(GregorianCalendar.MONTH,
                        ThreadLocalRandom.current().nextInt(cal.getActualMinimum(Calendar.MONTH), cal.getActualMaximum(Calendar.MONTH)));
                cal.set(GregorianCalendar.DAY_OF_MONTH,
                        ThreadLocalRandom.current().nextInt(cal.getActualMinimum(Calendar.DAY_OF_MONTH), cal.getActualMaximum(Calendar.DAY_OF_MONTH)));

                // Convert the Date to a SQL Date.
                java.sql.Date date = new java.sql.Date(cal.getTimeInMillis());
                return date;
            default:
                log.error("Generation of datatype {} is not supported yet." , dataType);
                return null;
        }
    }

    private String getString(int length) {
        return RandomString.generateAlpha(length, arguments.getRandom());
    }

    /**
     * Clones the current GeneratedParameter object.
     * @return GeneratedParameter
     */
    @Override
    public Parameter clone() {
        return new GeneratedParameter(this.type, this.dataType, this.arguments.clone());
    }

}
