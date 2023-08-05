#!/bin/sh

if ! hash poetry 2>/dev/null; then
	echo "Install poetry to initialize a poetry project"
	exit 0
fi

(cd "$2" && poetry init)
