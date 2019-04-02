#!/bin/bash

# stop on error
set -e

# glowdrop path
glowdrop="python3 ../GlowDrop/GlowDrop.py"

echo "Check your config.yaml file"
$glowdrop --make_conf

if  [ $# -lt 1 ]; then
    echo "No argument specified"
    exit 0
fi

DIRECTORY="pip"
PACKAGE="$1"
PACKDIR="$DIRECTORY/$PACKAGE"

echo "Creating $PACKDIR dir"
mkdir -p $PACKDIR

python3 -m pip download $PACKAGE -d $PACKDIR

FILE=`ls ${PACKDIR}/*.whl`
echo "Converting .whl to .txt..."
for f in ${PACKDIR}/*whl; do mv "$f" ${PACKDIR}/"$(basename "$f" .whl)".txt; done
echo "Zipping: ${PACKDIR}"
zip -r ${DIRECTORY}/${PACKAGE}.zip ${PACKDIR}
echo "Sending with glowdrop: ${PACKAGE}.zip"
$glowdrop -s ${DIRECTORY}/${PACKAGE}.zip -e -c config.yaml
echo "RemotePIP completed!"