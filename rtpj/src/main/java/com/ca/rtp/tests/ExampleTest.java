package com.ca.rtp.tests;

import com.ca.rtp.core.RtpTest;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Set;

/**
 * Created by bergr05 on 2/25/2016.
 */
public class ExampleTest implements RtpTest {

    public boolean invoke(HashMap<String, String> parms) {
        System.out.println("I am a Example test that was invoked via the TestRunner.");
        System.out.println("I was passed the following parameters:");
        Set<String> keys = parms.keySet();
        System.out.println("Parameters:");

        for (String key : keys) {
            System.out.println(key + " : " + parms.get(key));
        }

        return true;
    }
}
