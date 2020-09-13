#!/bin/bash

RAW_DATA_ROOT="/scratch/rabin/data/code2vec/handcrafted"
DATASET_NAME="top10/deduplication/java-large"
PARTITION_NAMES=("training"  "validation" "test")

# Run for ("false" "true")/("HC33" "HC33X"): $source HandcraftedExtractor.sh
add_complexity="false" # ("false" "true")
hfe_type="HC33" # ("HC33" "HC33X")

for partition in "${PARTITION_NAMES[@]}"; do
  inputPath=${RAW_DATA_ROOT}/${DATASET_NAME}/${partition}/
  echo "${inputPath}"
  outputPath="../data/handcrafted"/${DATASET_NAME}/"all"/${hfe_type}
  mkdir -p ${outputPath}
  java -jar HandcraftedExtractor.jar "${inputPath}" "${add_complexity}" &> "${outputPath}/${partition}.csv"
  echo "${outputPath}/${partition}.csv"
  echo
done
