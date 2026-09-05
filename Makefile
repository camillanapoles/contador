SDK ?= $(ANDROID_HOME)
BT ?= $(lastword $(sort $(wildcard $(SDK)/build-tools/*)))
PLATFORM ?= $(lastword $(sort $(wildcard $(SDK)/platforms/android-*/android.jar)))
SRC := $(shell find src -name '*.java' 2>/dev/null)

.PHONY: test verify apk _apk gov
test:
	@for t in tests/pre/T-*.sh; do [ -e "$$t" ] || continue; bash "$$t" || exit 1; done
verify:
	@for t in tests/post/T-*.sh; do [ -e "$$t" ] || continue; bash "$$t" || exit 1; done
apk:
	@if [ -z "$(SRC)" ]; then echo "sem src/ — build adiado (etapas iniciais)"; else $(MAKE) _apk; fi
_apk:
	rm -rf build && mkdir -p build/classes build/dex build/gen
	$(BT)/aapt2 compile --dir app/res -o build/res.zip
	$(BT)/aapt2 link -o build/unsigned.apk -I $(PLATFORM) \
		--manifest app/AndroidManifest.xml --java build/gen \
		--min-sdk-version 24 --target-sdk-version 34 build/res.zip
	javac -source 17 -target 17 -Xlint:-options -classpath $(PLATFORM) \
		-d build/classes $(SRC) $$(find build/gen -name '*.java')
	$(BT)/d8 --release --lib $(PLATFORM) --min-api 24 \
		--output build/dex $$(find build/classes -name '*.class')
	cd build/dex && zip -q ../unsigned.apk classes.dex
gov:
	cd gov && python3 -m uvicorn api:app --host 127.0.0.1 --port 8791
