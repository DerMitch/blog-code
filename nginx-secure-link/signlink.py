#!/usr/bin/env python3
"""
	Python implementation to generate signed urls for nginx' secure_link module.

	Signing code based on:
	https://gist.github.com/bftanase/cbae1f9fc69bb4f9cb86
"""

import time
import base64
import hashlib
from urllib.parse import urlencode

# Achtung: Im Gegensatz zu den hashlink.* Beispielen ist der gesamte Link
#          Teil des zu signierenden Payloads, nicht nur der Dateiname am Ende.
prefix = "http://localhost:9005"
link = "/s/trade-secrets.txt"
secret = "secret"

# Lokale Zeit + 1 Tag
expires = int(time.time() + 86400)

# Abgleichen mit secure_link_md5
url_hash = "{}{} {}".format(expires, link, secret,)

url_hash = hashlib.md5(url_hash.encode()).digest()
url_hash = base64.b64encode(url_hash).decode()
url_hash = url_hash.replace("+", "-")
url_hash = url_hash.replace("/", "_")
url_hash = url_hash.replace("=", "")

final_url = "{}{}?{}".format(prefix, link, urlencode({
	'md5': url_hash,
	'expires': expires,
}))

print(final_url)
