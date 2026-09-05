#!/bin/bash
# RNF-01: dois layouts reais definidos
N=$(ls app/res/layout/*.xml 2>/dev/null | wc -l)
[ "$N" -ge 2 ] && echo "T-S01-02 PASS: $N layouts" || { echo "T-S01-02 FAIL: $N layouts"; exit 1; }
