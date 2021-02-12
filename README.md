(This is under development. Please do not use)

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.246-blue.svg)](https://doi.org/10.25663/brainlife.app.246)

# app-qsiprep

This app runs [QSIPrep](https://github.com/pennbbl/qsiprep) on the [brainlife.io](https://brainlife.io/) interface. QSIPrep configures pipelines for processing diffusion-weighted MRI (dMRI) data. This App implements only the preprocessing piplines (and not the reconstruction pipelines). The preprocessing pipelines are built based on the available BIDS inputs, ensuring that fieldmaps are handled correctly. The preprocessing workflow performs head motion correction, susceptibility distortion correction, MP-PCA denoising, coregistration to T1w images, spatial normalization using ANTs and tissue segmentation.


#### citiations and resources to consider
* QSIPrep bioRxiv paper: https://www.biorxiv.org/content/10.1101/2020.09.04.282269v1
* QSIPrep documentation: https://qsiprep.readthedocs.io
* QSIPrep full list of citations: https://qsiprep.readthedocs.io/en/latest/citing.html 


### Authors
- Giulia Bertò ([@giulia-berto](https://github.com/giulia-berto))
- Soichi Hayashi ([@soichih](https://github.com/soichih))

### Project director
- Franco Pestilli ([@francopestilli](https://github.com/francopestilli))

### Funding 

[![NSF-GRFP-1342962](https://img.shields.io/badge/NSF_GRFP-1342962-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1342962)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-1342962](https://img.shields.io/badge/NSF_DGE-1342962-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1342962)

## Running the App 

### On Brainlife.io

Check out the brainlife app [here](https://doi.org/10.25663/brainlife.app.160)

### Running Locally

A)
  1) git clone this repo.
  2) Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

  ```json
  {
    "t1": "./t1.nii.gz",
    "dwi": "./dwi.nii.gz",
    "bvals": "./dwi.bvals",
    "bvecs": "./dwi.bvecs"
  }
  ```

  3. Launch the App by executing `main`

  ```bash
  ./main
  ```
  
  ## Output
  
  todo
  
  ### Dependencies

This App requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install following dependencies. It also requires [jq](https://stedolan.github.io/jq/).

---

#### MIT Copyright (c) brainlife.io

<sub> This material is based upon work supported by the National Science Foundation Graduate Research Fellowship under Grant No. 1342962. Any opinion, findings, and conclusions or recommendations expressed in this material are those of the authors(s) and do not necessarily reflect the views of the National Science Foundation. </sub>
