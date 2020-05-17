#!/bin/sh
mkdir -p "../tools/svm_light/"
cd "../tools/svm_light/"
wget http://download.joachims.org/svm_light/current/svm_light.tar.gz
gunzip -c svm_light.tar.gz | tar xvf -
make all
