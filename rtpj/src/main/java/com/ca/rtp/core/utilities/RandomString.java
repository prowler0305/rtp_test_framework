package com.ca.rtp.core.utilities;

import java.util.Random;

/**
 * Created by bergr05 on 2/19/2016.
 */
public class RandomString {

    /**
     * Generates a random string using printable characters.
     * @param len - the desired length of the string.
     * @return String
     */
    public static String generateAlpha(int len) {
        StringBuilder str = new StringBuilder();
        Random rnd = new Random();
        final String chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        for (int i = 0; i < len; i++) {
            str.append(chars.charAt(rnd.nextInt(1000)%chars.length()));
        }
        return str.toString();
    }

    /**
     * Generates a random string using printable characters.
     * @param len - the desired length of the string.
     * @param rnd - the Random object to use.
     * @return String
     */
    public static String generateAlpha(int len, Random rnd) {
        StringBuilder str = new StringBuilder();
        final String chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

        for (int i = 0; i < len; i++) {
            str.append(chars.charAt(rnd.nextInt(1000)%chars.length()));
        }
        return str.toString();
    }


    /**
     * Generates a random string using ALL characters.
     * @param len - the desired length of the string.
     * @return String
     */
    public static String generate(int len) {
        StringBuilder str = new StringBuilder();
        Random rnd = new Random();
        for (int i = 0; i < len; i++) {
            int next = rnd.nextInt(255);
            if (next > 0) {
                str.append((char)(next));
            } else {
                i--;
            }
        }
        return str.toString();
    }

    /**
     * Generates a random string using ALL characters.
     * @param len - the desired length of the string.
     * @param rnd - the Random object to use.
     * @return String
     */
    public static String generate(int len, Random rnd) {
        StringBuilder str = new StringBuilder();
        for (int i = 0; i < len; i++) {
            int next = rnd.nextInt(255);
            if (next > 0) {
                str.append((char)(next));
            } else {
                i--;
            }
        }
        return str.toString();
    }
}
