#!/bin/bash

set -e

# detect.py script is taken from https://github.com/brainlife/app-testflip/blob/1.3/detect.py
# with small changes, since here dwi, bvals, and bvecs filenames are in a list
SINGULARITYENV_PYTHONNOUSERSITE=true singularity exec -e docker://brainlife/dipy:1.1.1 ./detect.py

msg=$(jq -r '.brainlife[].msg' product.json)
bvecs=$(jq -r '.bvecs[0]' config.json)

if [[ "$msg" =~ "bvecs directions look good!" ]]; then
	echo "No bvecs flip is needed!"
	cp $bvecs ./dwi_new.bvecs

else
	mv config.json config_original.json #backup config.json

	if [[ "$msg" =~ "bvecs-x seems to be flipped." ]]; then
		echo "Flipping bvecs-x..."
		echo "{\"bvecs_out\": \"$bvecs\", \"xflip\": \"true\"}" > config.json
	elif [[ "$msg" =~ "bvecs-y seems to be flipped." ]]; then
		echo "Flipping bvecs-y..."
		echo "{\"bvecs_out\": \"$bvecs\", \"yflip\": \"true\"}" > config.json
	elif [[ "$msg" =~ "bvecs-z seems to be flipped." ]]; then
		echo "Flipping bvecs-z..."
		echo "{\"bvecs_out\": \"$bvecs\", \"zflip\": \"true\"}" > config.json
	fi

    singularity exec -e docker://brainlife/mcr:neurodebian1604-r2017a ./compiled/main
    cp dwi.bvecs ./dwi_new.bvecs #flipped bvecs
	rm config.json 
	mv config_original.json config.json #restore original config.json
fi


