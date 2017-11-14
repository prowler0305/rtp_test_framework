package com.ca.rtp.auth;

import java.util.concurrent.ConcurrentHashMap;

/**
 * The CredentialsCache holds the credentials for each user connecting to DB2.
 * This cache is kept in memory for the life of the JVM.
 *
 * Created by bergr05 on 4/20/2016.
 * Copyright (c) 4/20/2016 CA Technologies. All rights reserved.
 */
public class CredentialsCache {

    public static final ConcurrentHashMap<String, Credentials> cache = new ConcurrentHashMap();

    /**
     * Get the user credentials from the cache.
     * If the credentials are not found a new credential object is created and returned.
     * This object is automatically added to the cache and then returned.
     * @param user String
     * @return Credentials
     */
    public static synchronized Credentials get(String user) {

        if (cache.containsKey(user)) {
            return cache.get(user);
        } else {
            Credentials creds = new Credentials(user);
            cache.put(user, creds);
            return cache.get(user);
        }
    }

    /**
     * Add a user and credentials to the cache.
     * @param user
     * @param creds
     */
    public static synchronized void put(String user, Credentials creds) {
        cache.put(user, creds);
    }

    /**
     * Remove a user and credentials from the cache.
     * @param user
     */
    public static synchronized void remove(String user) {
        cache.remove(user);
    }
}

