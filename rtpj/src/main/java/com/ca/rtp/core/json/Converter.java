package com.ca.rtp.core.json;

import com.ca.rtp.core.utilities.ExceptionUtilities;
import com.fasterxml.jackson.databind.JsonNode;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.sql.*;

/**
 * Created by schke19 on 4/5/2016.
 */
public class Converter {

    private static final Logger log = LogManager.getLogger(Converter.class);

    public static String[] sqlTypesStrings = {
            "ARRAY",
            "BIGINT",
            "BINARY",
            "BIT",
            "BLOB",
            "BOOLEAN",
            "CHAR",
            "CLOB",
            "DATALINK",
            "DATE",
            "DECIMAL",
            "DISTINCT",
            "DOUBLE",
            "FLOAT",
            "INTEGER",
            "JAVA_OBJECT",
            "LONGNVARCHAR",
            "LONGVARBINARY",
            "LONGVARCHAR",
            "NCHAR",
            "NCLOB",
            "NULL",
            "NUMERIC",
            "NVARCHAR",
            "OTHER",
            "REAL",
            "REF",
            "ROWID",
            "SMALLINT",
            "SQLXML",
            "STRUCT",
            "TIME",
            "TIMESTAMP",
            "TINYINT",
            "VARBINARY",
            "VARCHAR"
    };

    /**
     * Convert a parameter value to a specific datatype.
     * @param valueNode JsonNode
     * @param datatype String
     * @return Object
     */
    public static Object parameterValueToObject(JsonNode valueNode, String datatype) {
        // Extract value for STATIC type parameters based on the datatype
        // datatype should correspond to values defined in java.sql.Types
        switch (datatype) {
            case "ARRAY":
                Converter.notSupported(datatype);
                return null;
            case "BIGINT":
                return valueNode.asLong();
            case "BINARY":
                try {
                    return valueNode.binaryValue();
                } catch (IOException e) {
                    Converter.datatypeConversionException(datatype, e);
                    return null;
                }
            case "BIT":
                return valueNode.booleanValue();
            case "BLOB":
                try {
                    return valueNode.binaryValue();
                } catch (IOException e) {
                    Converter.datatypeConversionException(datatype, e);
                    return null;
                }
            case "BOOLEAN":
                return valueNode.booleanValue();
            case "CHAR":
                return valueNode.asText("");
            case "CLOB":
                return valueNode.asText("");
            case "DATALINK":
                Converter.notSupported(datatype);
                return null;
            case "DATE":
                return new Date(valueNode.asLong());
            case "DECIMAL":
                return valueNode.decimalValue();
            case "DISTINCT":
                Converter.notSupported(datatype);
                return null;
            case "DOUBLE":
                return valueNode.asDouble();
            case "FLOAT":
                return (float) valueNode.asDouble();
            case "INTEGER":
                return valueNode.asInt();
            case "JAVA_OBJECT":
                Converter.notSupported(datatype);
                return null;
            case "LONGNVARCHAR":
                Converter.notSupported(datatype);
                return null;
            case "LONGVARBINARY":
                try {
                    return valueNode.binaryValue();
                } catch (IOException e) {
                    Converter.datatypeConversionException(datatype, e);
                    return null;
                }
            case "LONGVARCHAR":
                return valueNode.asText("");
            case "NCHAR":
                Converter.notSupported(datatype);
                return null;
            case "NCLOB":
                Converter.notSupported(datatype);
                return null;
            case "NULL":
                return null;
            case "NUMERIC":
                return valueNode.decimalValue();
            case "NVARCHAR":
                Converter.notSupported(datatype);
                return null;
            case "OTHER":
                Converter.notSupported(datatype);
                return null;
            case "REAL":
                return (float) valueNode.asDouble();
            case "REF":
                Converter.notSupported(datatype);
                return null;
            case "ROWID":
                try {
                    return valueNode.binaryValue();
                } catch (IOException e) {
                    Converter.datatypeConversionException(datatype, e);
                    return null;
                }
            case "SMALLINT":
                return (short) valueNode.asInt();
            case "SQLXML":
                return valueNode.toString();
            case "STRUCT":
                Converter.notSupported(datatype);
                return null;
            case "TIME":
                return new Time(valueNode.asLong());
            case "TIMESTAMP":
                return new Timestamp(valueNode.asLong());
            case "TINYINT":
                return (byte) valueNode.asInt();
            case "VARBINARY":
                try {
                    return valueNode.binaryValue();
                } catch (IOException e) {
                    Converter.datatypeConversionException(datatype, e);
                    return null;
                }
            case "VARCHAR":
                return valueNode.asText("");
            default:
                Converter.notSupported(datatype);
        }
        return null;
    }

    /**
     * Standard log error message for a unsupported datatype.
     * @param datatype String
     */
    private static void notSupported(String datatype) {
        log.error("Error: Datatype: {} not supported yet.", datatype);
    }

    /**
     * Standard log error message for an exception when converting an object to its specified datatype.
     * @param datatype String
     * @param e Exception
     */
    private static void datatypeConversionException(String datatype, Exception e) {
        log.error("{} conversion failed. \n Trace: {}", datatype, ExceptionUtilities.stacktraceToString(e));
    }

    public static int getSqlType(String type) {
        switch (type) {
            case "ARRAY":
                return Types.ARRAY;
            case "BIGINT":
                return Types.BIGINT;
            case "BINARY":
                return Types.BINARY;
            case "BIT":
                return Types.BIT;
            case "BLOB":
                return Types.BLOB;
            case "BOOLEAN":
                return Types.BOOLEAN;
            case "CHAR":
                return Types.CHAR;
            case "CLOB":
                return Types.CLOB;
            case "DATALINK":
                return Types.DATALINK;
            case "DATE":
                return Types.DATE;
            case "DECIMAL":
                return Types.DECIMAL;
            case "DISTINCT":
                return Types.DISTINCT;
            case "DOUBLE":
                return Types.DOUBLE;
            case "FLOAT":
                return Types.FLOAT;
            case "INTEGER":
                return Types.INTEGER;
            case "JAVA_OBJECT":
                return Types.JAVA_OBJECT;
            case "LONGNVARCHAR":
                return Types.LONGNVARCHAR;
            case "LONGVARBINARY":
                return Types.LONGVARBINARY;
            case "LONGVARCHAR":
                return Types.LONGVARCHAR;
            case "NCHAR":
                return Types.NCHAR;
            case "NCLOB":
                return Types.NCLOB;
            case "NULL":
                return Types.NULL;
            case "NUMERIC":
                return Types.NUMERIC;
            case "NVARCHAR":
                return Types.NVARCHAR;
            case "OTHER":
                return Types.OTHER;
            case "REAL":
                return Types.REAL;
            case "REF":
                return Types.REF;
            case "ROWID":
                return Types.ROWID;
            case "SMALLINT":
                return Types.SMALLINT;
            case "SQLXML":
                return Types.SQLXML;
            case "STRUCT":
                return Types.STRUCT;
            case "TIME":
                return Types.TIME;
            case "TIMESTAMP":
                return Types.TIMESTAMP;
            case "TINYINT":
                return Types.TINYINT;
            case "VARBINARY":
                return Types.VARBINARY;
            case "VARCHAR":
                return Types.VARCHAR;
            default:
                return -1;
        }
    }
}
