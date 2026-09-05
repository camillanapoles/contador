#!/bin/bash
# UC-02/GWT estrutura: Given manifest do app / When declara telas / Then MainActivity E AboutActivity existem
grep -q "MainActivity" app/AndroidManifest.xml && grep -q "AboutActivity" app/AndroidManifest.xml \
  && echo "T-S01-01 PASS: 2 activities declaradas" || { echo "T-S01-01 FAIL"; exit 1; }
