#!/bin/bash

pushd event-sourcing-python >/dev/null 2>&1
	make lint || exit 1
	make test || exit 1
popd >/dev/null 2>&1
