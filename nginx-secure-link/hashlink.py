#!/usr/bin/env python3
"""
	Python implementation to generate hashed urls for nginx' secure_link module.
"""

import hashlib

prefix = "http://localhost:9005/p"
link = "trade-secrets.txt"
secret = "secret"

link_hash = hashlib.md5("{}{}".format(link, secret).encode()).hexdigest()
print("{}/{}/{}".format(prefix, link_hash, link))
