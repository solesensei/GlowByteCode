#!/bin/sh

if  [ $# -eq 1 ]; then
    package=$1
else
    echo "No argument specified"
    exit 0
fi

shopt -s expand_aliases
source ~/.bashrc

cd ~
DIRECTORY="./pip"

if [ ! -d "$DIRECTORY" ]; then
    echo "Creating pip dir"
    mkdir pip
fi

cd pip
python3 -m pip download $package

FILE=`ls ${package}*.whl`
echo "Converting to txt"
ls ${package}*.whl
mv $FILE ${FILE}.txt
ls ${package}*.txt
echo "Sending with glowdrop: ${FILE}.txt"
glowdrop -s ${FILE}.txt -e -c ~/config.yaml
echo "Rename back"
mv ${FILE}.txt $FILE