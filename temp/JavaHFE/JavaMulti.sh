#!/bin/bash

mTopN="top11"
mDataRoot="/scratch/rabin/data/code2vec/handcrafted"
jType="java-large"

<<<<<<< HEAD
inputPath=${mDataRoot}/${mTopN}/"Methods"/${jType}
outputPath="../data/handcrafted"/${jType}/${mTopN}/"multi"/"count"
java -jar target/jar/JavaHFE.jar ${inputPath} ${outputPath} true
=======
inputPath=${RAW_DATA_ROOT}/${DATASET_NAME}
outputPath="../data/handcrafted"/${DATASET_NAME}/"complexity/multi/count"
java -jar JavaComplexity.jar ${inputPath} ${outputPath} true
>>>>>>> 2189d7f... Separate ComplexityPCA and MethodPCA
