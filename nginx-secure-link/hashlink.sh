#!/bin/sh

set -e
set -o pipefail

#
# Bash implementation to generate hashed urls for nginx' secure_link module.
#

LINK="trade-secrets.txt"
SECRET="secret"

# We don't use echo -n as it only seems to work in bash
LINK_HASH=$(printf "${LINK}${SECRET}" | openssl md5 -hex)

echo "http://localhost:9005/p/${LINK_HASH}/${LINK}"
