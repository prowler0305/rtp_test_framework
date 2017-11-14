package com.ca.rtp.auth;

/**
 * The Decryptor unseals a sealed XOR string using the passed in key.
 * Created by bergr05 on 2/19/2016.
 */
public class Decryptor {

    public static String unseal(String sealed, String key) {
        char temp;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < sealed.length(); i++) {
            temp = (char) (key.charAt(i) ^ sealed.charAt(i));
            sb.append(temp);
        }

        return sb.toString();
    }
}
