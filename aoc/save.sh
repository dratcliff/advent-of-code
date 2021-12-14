#!/bin/bash
if [ -z "$1" ]
  then
    echo "No argument supplied. The argument should be the day to saved."
    exit 1
fi

mkdir $1
mv a.py $1
mv a.txt $1
mv b.txt $1

cp template/* .
