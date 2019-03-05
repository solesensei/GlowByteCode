#!/bin/bash

# stop on error
set -e


# change dir
cd /mnt/c/prj/GlowByteCode/RemotePIP/

# glowdrop path
glowdrop='python3 /mnt/c/prj/GlowByteCode/GlowDrop/GlowDrop.py'

if  [ $# -eq 1 ]; then
    package=$1
else
    echo "No argument specified"
    exit 0
fi

DIRECTORY="pip"

if [ ! -d "$DIRECTORY" ]; then
    echo "Creating $DIRECTORY dir"
    mkdir $DIRECTORY
fi

cd $DIRECTORY
python3 -m pip download $package

FILE=`ls ${package}*.whl`
echo "Converting to txt"
ls ${package}*.whl
mv $FILE ${FILE}.txt
ls ${package}*.txt
echo "Sending with glowdrop: ${FILE}.txt"
$glowdrop -s ${FILE}.txt -e -c ~/config.yaml
echo "Rename back"
mv ${FILE}.txt $FILE