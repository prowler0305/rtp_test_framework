package com.ca.rtp.core.json;

import java.util.Random;

/**
 * The Arguments class contains a set of parameters that represent
 * an input parameter from a JSON RTP test.
 *
 * Created by bergr05 on 4/15/2016.
 * Copyright (c) 4/15/2016 CA Technologies. All rights reserved.
 */
public class Arguments {

    private int length;
    private Long seed;
    private Object value;
    private String subType;
    private Random random;
    private String key;
    private int max;
    private boolean randomize;

    public Arguments(){
        length = 0;
        seed = 0L;
        value = "";
        subType = "";
        key = "";
        max = 0;
        randomize = false;
        random = null;
    }

    public void setValue(Object value) {
        this.value = value;
    }

    public void setLength(int length) {
        this.length = length;
    }

    public void setSubtype(String subType) {
        this.subType = subType;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public void setMax(int max) {
        this.max = max;
    }

    public void setRandom(Random random) {
        this.random = random;
    }


    /**
     * Set the random seed value.
     * Set the current Random object with the modified seed value.
     * @param seed
     */
    public void setSeed(long seed) {
        this.seed = seed;
    }

    public void setRandomize(boolean randomize) {
        this.randomize = randomize;
    }

    public Random getRandom(){
        if (this.random == null) {
            if (this.seed == 0) {
                this.random = new Random(System.nanoTime() + Thread.currentThread().getId());
            } else {
                this.random = new Random();
            }
        }
        return this.random;
    }

    public boolean getRandomize(){
        return this.randomize;
    }

    public Object getValue() {
        return this.value;
    }

    public int getLength() {
        return this.length;
    }

    public String getSubType() {
        return this.subType;
    }

    public String getKey() {
        return this.key;
    }

    public long getSeed() {
        return this.seed;
    }

    public int getMax() {
        return this.max;
    }

    /**
     * Clones the current Arguments object.
     * @return Arguments
     */
    @Override
    public Arguments clone() {
        Arguments arg = new Arguments();
        arg.setValue(this.value);
        arg.setLength(this.length);
        arg.setSubtype(this.subType);
        arg.setSeed(this.seed);
        arg.setKey(this.key);
        arg.setMax(this.max);
        arg.setRandomize(this.randomize);
        arg.setRandom(this.random);

        return arg;
    }

}
