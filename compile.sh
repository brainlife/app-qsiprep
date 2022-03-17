#!/bin/bash
mkdir -p compiled
cat > build.m <<END
addpath(genpath(pwd))
addpath(genpath('/N/u/brlife/git/jsonlab'))
mcc -m -R -nodisplay -d compiled main
exit
END
matlab -nodisplay -nosplash -r build
