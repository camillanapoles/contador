#!/bin/bash
# RF-01/02 pós-build: bytecode das 2 activities compilado
N=$(find build/classes -name '*.class' 2>/dev/null | wc -l)
[ "$N" -ge 3 ] && echo "T-S02-02 PASS: $N classes compiladas" || { echo "T-S02-02 FAIL: $N classes"; exit 1; }
