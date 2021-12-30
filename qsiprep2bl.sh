#!/bin/bash

#####################################################################################
# reogranize qsiprep outputs for brainlife 
#####################################################################################

set -x
set -e

outdir=output

# get basename for output
sub=$(jq -r '._inputs[0].meta.subject' config.json)
oDir=$outdir/fmriprep/sub-$sub

#organize output
mkdir -p output_anat_preproc
mkdir -p output_dseg
mkdir -p output_brainmask

SRCDIR=$outdir/qsiprep/sub-${sub}/anat

if [ $space == "T1w" ]; then
    cp $SRCDIR/sub-${sub}_desc-preproc_T1w.nii.gz output_anat_preproc/t1.nii.gz;
    cp $SRCDIR/sub-${sub}_dseg.nii.gz output_dseg/parc.nii.gz;
    cp $SRCDIR/sub-${sub}_desc-brain_mask.nii.gz output_brainmask/mask.nii.gz;
elif [ $space == "template" ]; then
    cp $SRCDIR/sub-${sub}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz output_anat_preproc/t1.nii.gz;     
    cp $SRCDIR/sub-${sub}_space-MNI152NLin2009cAsym_dseg.nii.gz output_dseg/parc.nii.gz;
    cp $SRCDIR/sub-${sub}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz output_brainmask/mask.nii.gz;
fi

mkdir -p output_dwi
cp $outdir/qsiprep/sub-*/dwi/sub-*_space-T1w_desc-preproc_dwi.nii.gz output_dwi/dwi.nii.gz
cp $outdir/qsiprep/sub-*/dwi/sub-*_space-T1w_desc-preproc_dwi.bvec output_dwi/dwi.bvecs
cp $outdir/qsiprep/sub-*/dwi/sub-*_space-T1w_desc-preproc_dwi.bval output_dwi/dwi.bvals

#report
mkdir -p output_report

for html in $(cd $outdir && find -name "*.html"); do
    mkdir -p output_report/$(dirname $html)
    cp $outdir/$html output_report/$html
done

for dir in $(cd $outdir && find ./ -name figures); do
    mkdir -p output_report/$(dirname $dir)
    cp -r $outdir/$dir output_report/$(dirname $dir)
done

#rename the parent directory to confirm to brainlife html output
mv output_report/qsiprep output_report/html 