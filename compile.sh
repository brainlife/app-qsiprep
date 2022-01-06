#!/bin/bash
mkdir -p compiled
cat > build.m <<END
addpath(genpath(pwd))
mcc -m -R -nodisplay -d compiled main
exit
END
matlab -nodisplay -nosplash -r build