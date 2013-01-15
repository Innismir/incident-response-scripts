#!/bin/bash
/usr/bin/python hostomatic.py -g -i $1 -o /tmp/chartomatic.out
/usr/bin/R --no-save -q -f chartomatic.r

NOW=$(date +"%N")
FILE_USA="chartomatic.output.$NOW.usa.png"
FILE_WORLD="chartomatic.output.$NOW.world.png"
FILE_DATA="chartomatic.output.$NOW.hosts.txt"

mv /tmp/chartomatic.out.usa.png $FILE_USA
mv /tmp/chartomatic.out.world.png $FILE_WORLD
mv /tmp/chartomatic.out $FILE_DATA

echo Hostomatic output in $FILE_DATA
echo USA map in $FILE_USA
echo World map in $FILE_WORLD

