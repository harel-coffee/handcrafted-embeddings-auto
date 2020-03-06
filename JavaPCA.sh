#!/bin/bash

# generating jar
mvn -f ./JavaPCA/ clean compile assembly:single &> JavaPCA.log

# generating pca
mN=1000
mDataRoot="/scratch/rabin/data/code2vec/pca/t${mN}"
jDataTypes=("java-large")
jDataCats=("training")
jDataTars=("nonTarget" "equals" "setUp" "toString")
for jType in "${jDataTypes[@]}"; do
    for jCat in "${jDataCats[@]}"; do
        for jTar in "${jDataTars[@]}"; do
            echo "${jType}/${jCat}/${jTar}"
            inputPath=${mDataRoot}/${jTar}/${jType}/${jCat}
            outputPath="data/pca"/${jType}/${jCat}/"count"
            java -jar JavaPCA/target/jar/JavaPCA.jar ${inputPath} ${outputPath}
        done
    done
done
