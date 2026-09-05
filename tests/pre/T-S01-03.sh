#!/bin/bash
# Design: paleta + tema aplicados (design.md -> res/)
grep -q "accent" app/res/values/colors.xml && grep -q "AppTheme" app/res/values/styles.xml \
  && echo "T-S01-03 PASS: paleta+tema" || { echo "T-S01-03 FAIL"; exit 1; }
