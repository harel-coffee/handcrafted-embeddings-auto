DATA_TYPE=("java-large")
DATA_CATEGORY=("training" "validation" "test")
TOP_METHODS=("equals" "main" "setUp" "onCreate" "toString" "run" "hashCode" "init" "execute" "get" "close")

for i in "${DATA_TYPE[@]}"; do
    for j in "${DATA_CATEGORY[@]}"; do
        for k in "${TOP_METHODS[@]}"; do
            echo $i/$j/$k:; find Methods/$i/$j -type f -name "*_${k}.java" | wc -l
        done
        echo $i/$j:; find Methods/$i/$j -type f -name "*.java" | wc -l
    done
    echo $i:; find Methods/$i -type f -name "*.java" | wc -l
done
