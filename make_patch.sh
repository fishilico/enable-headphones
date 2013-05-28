#!/bin/sh
# Make HDA analyzer patch

UPSTREAM=alsa/hda-analyzer
CURRENT=hda_analyzer

cd $(dirname $0)
if ! [ -d "$UPSTREAM" ] ; then
    echo >&2 "Missing upstream directory"
    exit 1
elif ! [ -d "$CURRENT" ] ; then
    echo >&2 "Missing current directory"
    exit 1
fi

if ! (mkdir a && cp $UPSTREAM/*.py a) ; then
    echo >&2 "Unable to copy upstream version"
    exit 1
elif ! (mkdir b && cp $CURRENT/*.py b) ; then
    echo >&2 "Unable to copy current version"
    exit 1
fi

diff -Naur a b
rm -rf a b
