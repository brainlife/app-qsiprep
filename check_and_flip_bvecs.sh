#!/bin/bash

set -e

# detect.py script is taken from https://github.com/brainlife/app-testflip/blob/1.3/detect.py
# with small changes, since here dwi, bvals, and bvecs filenames are in a list
SINGULARITYENV_PYTHONNOUSERSITE=true singularity exec -e docker://brainlife/dipy:1.1.1 ./detect.py

msg=$(jq -r '.brainlife[].msg' product.json)
bvecs=$(jq -r '.bvecs[0]' config.json)
sub=$(jq -r '._inputs[0].meta.subject' config.json)
ses=$(jq -r '._inputs[] | select(.id == "dwi") | .meta.session' config.json)
ses=($ses)

if [[ "$msg" =~ "bvecs directions look good!" ]]; then
	echo "No bvecs flip is needed!"

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
	echo "Flipping done."

	#overwrite bvecs
	outsub="bids/sub-${sub}"
	outfile="sub-${sub}"

	# if a session tag exists, append to outsub and outfile
	[ "$ses" != "null" ] && outsub=$outsub/ses-${ses[0]}
	[ "$ses" != "null" ] && outfile=${outfile}_ses-${ses[0]}

	bvecs_path=$outsub/dwi/${outfile}_dwi.bvec
	mv -f dwi.bvecs $bvecs_path

	rm config.json 
	mv config_original.json config.json #restore original config.json

	##remove bvecs from config.json
	#tmp=$(mktemp)
	#jq '._inputs[1].meta.bvecs = ""' config.json > "$tmp" && mv "$tmp" config.json
fi

