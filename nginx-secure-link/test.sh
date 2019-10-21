#!/bin/bash

#
# URLs with hashes
#

EXPECTED_URL='http://localhost:9005/p/67606be31ce34020cafea3fc1464434b/trade-secrets.txt'

for file in hashlink.pl hashlink.py hashlink.sh; do
	OUTPUT=$(./$file)
	if [[ $? -ne 0 ]]; then
		echo "❗️ FAIL: ${file} crashed"
		continue
	fi

	if [[ ! "${EXPECTED_URL}" = "$OUTPUT" ]]; then
		echo "❗️ FAIL: ${file} output mismatch"
		echo "❗️   Expected: '${EXPECTED_URL}'"
		echo "❗️   Output:   '${OUTPUT}'"
		continue
	fi

	echo "☑️  ${file} passed!"
done

if curl http://localhost:9005 >/dev/null 2>&1; then
	echo "🌍 Running nginx tests"

	OUTPUT=$(curl "${EXPECTED_URL}" 2>/dev/null)
	if [[ $? -ne 0 ]]; then
		echo "❗️ FAIL: Could not download ${EXPECTED_URL}"
		exit 1
	fi
	echo "☑️  Download test passed"

	EXPECTED_SECRET=$(cat secret-files/trade-secrets.txt)
	if [[ ! "${EXPECTED_SECRET}" = "$OUTPUT" ]]; then
		echo "❗️ FAIL: ${EXPECTED_URL} output mismatch"
		echo "❗️   Expected: '${EXPECTED_SECRET}'"
		echo "❗️   Output:   '${OUTPUT}'"
		exit 1
	fi
else
	echo "❗️ nginx is not running on port 9005, not running tests"
fi
