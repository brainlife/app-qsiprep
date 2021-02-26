(This is under development. Please do not use)

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.246-blue.svg)](https://doi.org/10.25663/brainlife.app.246)

# app-qsiprep

This app runs [QSIPrep](https://github.com/pennbbl/qsiprep) on the [brainlife.io](https://brainlife.io/) interface. QSIPrep configures pipelines for processing diffusion-weighted MRI (dMRI) data. This App implements only the preprocessing piplines (and not the reconstruction pipelines). The preprocessing pipelines are built based on the available BIDS inputs, ensuring that fieldmaps are handled correctly. The preprocessing workflow performs head motion correction, susceptibility distortion correction, MP-PCA denoising, coregistration to T1w images, spatial normalization using ANTs and tissue segmentation.

#### References and resources to consider
* QSIPrep bioRxiv paper: https://www.biorxiv.org/content/10.1101/2020.09.04.282269v1
* QSIPrep documentation: https://qsiprep.readthedocs.io
* QSIPrep full list of citations: https://qsiprep.readthedocs.io/en/latest/citing.html 

### Authors
- Giulia Bertò ([@giulia-berto](https://github.com/giulia-berto))
- Soichi Hayashi ([@soichih](https://github.com/soichih))

### Project director
- Franco Pestilli ([@francopestilli](https://github.com/francopestilli))

### Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your code and publications. Copy and past the following lines into your repository when using this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations
We ask that you the following articles when publishing papers that used data, code or other resources created by the brainlife.io community.

1. Matthew Cieslak, Philip A. Cook, Xiaosong He, Fang-Cheng Yeh, Thijs Dhollander, Azeez Adebimpe, Geoffrey K. Aguirre, Danielle S. Bassett, Richard F. Betzel, Josiane Bourque, Laura M. Cabral, Christos Davatzikos, John Detre, Eric Earl, Mark A. Elliott, Shreyas Fadnavis, Damien A. Fair, Will Foran, Panagiotis Fotiadis, Eleftherios Garyfallidis, Barry Giesbrecht, Ruben C. Gur, Raquel E. Gur, Max Kelz, Anisha Keshavan, Bart S. Larsen, Beatriz Luna, Allyson P. Mackey, Michael Milham, Desmond J. Oathes, Anders Perrone, Adam R. Pines, David R. Roalf, Adam Richie-Halford, Ariel Rokem, Valerie J. Sydnor, Tinashe M. Tapera, Ursula A. Tooley, Jean M. Vettel, Jason D. Yeatman, Scott T. Grafton, Theodore D. Satterthwaite. QSIPrep: An integrative platform for preprocessing and reconstructing diffusion MRI.
bioRxiv 2020.09.04.282269; doi: https://doi.org/10.1101/2020.09.04.282269

2. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Running the App 

### On Brainlife.io

Check out the brainlife app [here](https://doi.org/10.25663/brainlife.app.246)

### Running Locally

Information on how to run QSIPrep locally can be found here: https://qsiprep.readthedocs.io/en/latest/usage.html#
  
### Outputs
  
1) DWI preprocessed;
2) T1w preprocessed;
3) volumetric parcellation;
4) brain mask;
5) html report for QA.
  
### Dependencies

This App requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install following dependencies. It also requires [jq](https://stedolan.github.io/jq/).

---

#### MIT Copyright (c) brainlife.io

<sub> This material is based upon work supported by the National Science Foundation Graduate Research Fellowship under Grant No. 1342962. Any opinion, findings, and conclusions or recommendations expressed in this material are those of the authors(s) and do not necessarily reflect the views of the National Science Foundation. </sub>
