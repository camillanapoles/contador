#!/bin/bash
# UC-01 pós-build: APK contém recursos compilados + dex
unzip -l build/unsigned.apk | grep -q resources.arsc && unzip -l build/unsigned.apk | grep -q classes.dex \
  && echo "T-S02-01 PASS: resources.arsc+classes.dex no APK" || { echo "T-S02-01 FAIL"; exit 1; }
