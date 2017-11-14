package com.ca.rtp.core;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.HashMap;

/**
 * Created by bergr05 on 2/23/2016.
 * Map of DB2 Connection information taken from SYSPROG.PRODUCTS($DOCDB2)
 */
public class Subsystems {

    // Get a logger
    private static final Logger log = LogManager.getLogger(Subsystems.class);

    public static final String CA11 = "usilca11.ca.com";
    public static final String CA31 = "usilca31.ca.com";
    public static final String CA32 = "usilca32.ca.com";
    public static final String DE24 = "mvsde24.ca.com";

    private static HashMap<String, ConnectionInfo> subsystems = new HashMap<>();

    static {

        subsystems.put("D11D", new ConnectionInfo("D11D", CA11, "5258"));

        subsystems.put("D10A", new ConnectionInfo("D10A", CA31, "5166"));
        subsystems.put("D11A", new ConnectionInfo("D11A", CA31, "5252"));
        subsystems.put("D10B", new ConnectionInfo("D10B", CA11, "5169"));
        subsystems.put("D11B", new ConnectionInfo("D11B", CA11, "5274"));

        subsystems.put("D81A", new ConnectionInfo("D81A", CA31, "5141"));

        subsystems.put("D81B", new ConnectionInfo("D81B", CA11, "5143"));
        subsystems.put("D81D", new ConnectionInfo("D81D", CA11, "5149"));
        subsystems.put("D81E", new ConnectionInfo("D81E", CA11, "5064"));
        subsystems.put("Q81A", new ConnectionInfo("Q81A", CA31, "5147"));
        subsystems.put("M81A", new ConnectionInfo("M81A", CA31, "5151"));

        subsystems.put("D91A", new ConnectionInfo("D91A", CA31, "5058"));
        subsystems.put("D91B", new ConnectionInfo("D91B", CA11, "5182"));
        subsystems.put("D91E", new ConnectionInfo("D91E", CA11, "5160"));
        subsystems.put("M91A", new ConnectionInfo("M91A", CA31, "5197"));
        subsystems.put("Q91A", new ConnectionInfo("Q91A", CA31, "5187"));

        subsystems.put("Q91B", new ConnectionInfo("Q91B", CA11, "5190"));
        subsystems.put("Q91C", new ConnectionInfo("Q91C", CA31, "5194"));

        subsystems.put("D10C", new ConnectionInfo("D10C", CA11, "5200"));
        subsystems.put("D10E", new ConnectionInfo("D10E", CA11, "5203"));
        subsystems.put("Q10A", new ConnectionInfo("Q10A", CA31, "5206"));
        subsystems.put("Q10B", new ConnectionInfo("Q10B", CA11, "5209"));

        subsystems.put("Q10C", new ConnectionInfo("Q10C", CA31, "5212"));
        subsystems.put("Q10D", new ConnectionInfo("Q10D", CA11, "5287"));
        subsystems.put("F108", new ConnectionInfo("F108", CA11, "5003"));
        subsystems.put("F109", new ConnectionInfo("F109", CA11, "5006"));
        subsystems.put("T10A", new ConnectionInfo("T10A", CA31, "5249"));

        subsystems.put("D11C", new ConnectionInfo("D11C", CA11, "5255"));
        subsystems.put("D11E", new ConnectionInfo("D11E", CA11, "5277"));
        subsystems.put("D11F", new ConnectionInfo("D11F", CA11, "5271"));

        subsystems.put("Q11A", new ConnectionInfo("Q11A", CA31, "5283"));
        subsystems.put("Q11B", new ConnectionInfo("Q11B", CA11, "5290"));
        subsystems.put("Q12A", new ConnectionInfo("Q12A", CA31, "5315"));

        subsystems.put("D12A", new ConnectionInfo("D12A", CA31, "5304"));

        subsystems.put("DBN1", new ConnectionInfo("DBN1", CA31, "5295"));
        subsystems.put("DBN2", new ConnectionInfo("DBN2", CA11, "5298"));
        subsystems.put("DBN3", new ConnectionInfo("DBN3", CA11, "5301"));

        subsystems.put("DA0G", new ConnectionInfo("DA0G", CA31, "5122"));
        subsystems.put("DA1G", new ConnectionInfo("DA0G", CA11, "5122"));
        subsystems.put("DA2G", new ConnectionInfo("DA0G", CA11, "5122"));
        subsystems.put("DA3G", new ConnectionInfo("DA0G", CA32, "5122"));

        subsystems.put("DB0G", new ConnectionInfo("DB0G", CA11, "5130"));
        subsystems.put("DB1G", new ConnectionInfo("DB0G", CA11, "5130"));
        subsystems.put("DB2G", new ConnectionInfo("DB0G", CA31, "5130"));
        subsystems.put("DB3G", new ConnectionInfo("DB0G", CA32, "5130"));
        subsystems.put("DB4G", new ConnectionInfo("DB0G", CA32, "5130"));

        subsystems.put("DC0G", new ConnectionInfo("DC0G", CA11, "5224"));
        subsystems.put("DC1G", new ConnectionInfo("DC0G", CA31, "5224"));
        subsystems.put("DC2G", new ConnectionInfo("DC0G", CA11, "5224"));
        subsystems.put("DC3G", new ConnectionInfo("DC0G", CA31, "5224"));

        subsystems.put("DH0G", new ConnectionInfo("DH0G", CA11, "5261"));
        subsystems.put("DH1G", new ConnectionInfo("DH0G", CA32, "5261"));
        subsystems.put("DH2G", new ConnectionInfo("DH0G", CA11, "5261"));
        subsystems.put("DH3G", new ConnectionInfo("DH0G", CA31, "5261"));

        subsystems.put("DD0G", new ConnectionInfo("DD0G", CA11, "5052"));
        subsystems.put("DD1G", new ConnectionInfo("DD0G", CA11, "5052"));
        subsystems.put("DD2G", new ConnectionInfo("DD0G", CA31, "5052"));
        subsystems.put("DD3G", new ConnectionInfo("DD0G", CA32, "5052"));

        subsystems.put("DR1G", new ConnectionInfo("DR0G", CA11, "5074"));
        subsystems.put("DR2G", new ConnectionInfo("DR0G", CA11, "5074"));
        subsystems.put("DR3G", new ConnectionInfo("DR0G", CA31, "5074"));

        subsystems.put("DT11", new ConnectionInfo("DTG", CA11, "5307"));
        subsystems.put("DT31", new ConnectionInfo("DTG", CA31, "5307"));
        subsystems.put("DT32", new ConnectionInfo("DTG", CA32, "5307"));

        // For DB2s on the mini DE24.
        subsystems.put("MC24", new ConnectionInfo("MCDB", DE24,"5261"));

    }

    private Subsystems(){}

    /**
     * Get a connection information object for the requested subsystem.
     * @param ssid String
     * @return ConnectionInfo
     * @throws RtpException
     */
    public static ConnectionInfo getConnectionInfo(String ssid) throws RtpException{
        ConnectionInfo ci = subsystems.get(ssid.toUpperCase());
        if(ci != null) {
            return new ConnectionInfo(ci.getSSID(), ci.getHost(), ci.getPort());
        } else {
            throw new RtpException("The requested subsystem " + ssid + " could not be located.");

        }
    }
}
