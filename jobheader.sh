#!/bin/bash

##figure out amount of wall time we really need by parsing config.json with jq
if [[ $(jq -r .dwi config.json) == *","* ]]; then
    walltime=12:00:00
else
    walltime=06:00:00
fi

echo "#PBS -l nodes=1:ppn=8,vmem=40gb"
echo "#PBS -l walltime=$walltime"
