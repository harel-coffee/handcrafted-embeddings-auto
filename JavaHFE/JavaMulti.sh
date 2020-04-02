#!/bin/bash

mTopN="top11"
mDataRoot="/scratch/rabin/data/code2vec/handcrafted"
jType="java-large"

inputPath=${mDataRoot}/${mTopN}/"Methods"/${jType}
outputPath="../data/handcrafted"/${jType}/${mTopN}/"count"
java -jar target/jar/JavaHFE.jar ${inputPath} ${outputPath} true
