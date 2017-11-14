package com.ca.rtp.auth;

import com.ca.rtp.core.RtpException;

/**
 * This exception is thrown when a user's password cannot be retrieved.
 * Created by bergr05 on 4/21/2016.
 * Copyright (c) 4/21/2016 CA Technologies. All rights reserved.
 */
public class CredentialsException extends RtpException{

    public CredentialsException() {
        super();
    }

    public CredentialsException(String message) {
        super(message);
    }

    public CredentialsException(String message, Throwable cause) {
        super(message, cause);
    }
}
