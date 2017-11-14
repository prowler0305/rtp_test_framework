package com.ca.rtp.core.json;

/**
 * Created by bergr05 on 4/19/2016.
 * Copyright (c) 4/19/2016 CA Technologies. All rights reserved.
 */
public class ThreadingInfo {

    public final int threads;
    public final boolean parallel;
    public final int sleep;

    public ThreadingInfo(int threads, boolean parallel, int sleep) {
        this.threads = threads;
        this.parallel = parallel;
        this.sleep = sleep;
    }
}
