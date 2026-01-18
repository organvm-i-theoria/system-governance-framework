#!/bin/bash
# verify_input_validation.sh

# Setup
TEST_DIR=$(mktemp -d)
# Copy script to test dir
cp scripts/install-framework.sh "$TEST_DIR/"
cd "$TEST_DIR" || exit 1
git init > /dev/null

EXIT_CODE=0

# Test Case 1: Malicious Version with newlines (Injection)
echo "Testing malicious input..."
PAYLOAD="v3.0.0
      with:
        injected: true"

OUTPUT=$(echo "Y" | bash ./install-framework.sh "$PAYLOAD" 2>&1)

if echo "$OUTPUT" | grep -q "Installation Complete"; then
    echo "❌ VULNERABLE: Script accepted malicious input."
    echo "Output snippet:"
    echo "$OUTPUT" | grep "Version:" -A 5
    EXIT_CODE=1
else
    echo "✅ SECURE: Script rejected malicious input."
fi

# Test Case 2: Valid Input
echo "Testing valid input..."
# Note: It might fail to download config if valid version doesn't exist on remote,
# but it should proceed past validation.
# We'll use a dummy version but valid format.
VALID_VERSION="v3.0.0"

OUTPUT_VALID=$(echo "Y" | bash ./install-framework.sh "$VALID_VERSION" 2>&1)

if echo "$OUTPUT_VALID" | grep -q "Installation Complete"; then
    echo "✅ SUCCESS: Script accepted valid input."
else
    echo "❌ FAILURE: Script rejected valid input or failed unexpectedly."
    echo "Output snippet:"
    echo "$OUTPUT_VALID" | head -n 20
    EXIT_CODE=1
fi

# Cleanup
cd ..
rm -rf "$TEST_DIR"

exit $EXIT_CODE
