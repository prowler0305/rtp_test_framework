package com.ca.rtp.auth;

import com.ca.rtp.core.utilities.RandomString;

/**
 * The Encryptor seals a string using XOR encryption.
 * Created by bergr05 on 2/19/2016.
 */
public class Encryptor {

    private StringBuilder sealed;
    private String key = "";

    public void seal(String input) {
        sealed = new StringBuilder();
        key = RandomString.generate(input.length());
        char temp;

        for (int i = 0; i < input.length(); i++) {
            temp = (char) (key.charAt(i) ^ input.charAt(i));
            sealed.append(temp);
        }
    }

    public String getSealed(){return this.sealed.toString();}

    public String getKey(){return this.key;}

    public void destroy() {
        sealed = null;
        key = null;
    }
}
