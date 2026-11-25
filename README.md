[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.246-blue.svg)](https://doi.org/10.25663/brainlife.app.246)

# app-qsiprep

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

**Preprocesses DWI with QSIPrep 0.15.3 (denoising, head motion and eddy correction, susceptibility distortion correction, coregistration to the T1w) and outputs the preprocessed DWI, T1w, brain mask, tissue segmentation and HTML report.**

Converts the inputs to BIDS and runs the QSIPrep preprocessing workflow only (no reconstruction), with denoising, unringing and head-motion transform as chosen, resampling the DWI to the requested isotropic resolution in T1w (ACPC) space. Use it as a complete diffusion preprocessing pipeline when you have a T1w image and one or two DWI runs; a second DWI must have the opposite phase-encoding direction, and fieldmaps are used when provided. Needs a FreeSurfer license (used by QSIPrep).

Run it on brainlife.io: [https://doi.org/10.25663/brainlife.app.246](https://doi.org/10.25663/brainlife.app.246)

| Input | Datatype | Required | Description |
|---|---|---|---|
| `t1` | `neuro/anat/t1w` (!qsiprep) | yes | T1 anatomical image. |
| `dwi` | `neuro/dwi` (!qsiprep, !preprocessed) | yes | DWI volume(s). If you input a second DWI, be sure that it has an opposite Phase Encoding Direction than the first DWI. At the moment, no more than 2 DWIs can be selected. |
| `fmap` | `neuro/fmap` | no | fieldmap |

| Output | Datatype | Description |
|---|---|---|
| `output_dwi` | `neuro/dwi` | Preprocessed DWI in T1w space with bvals and bvecs (FSL-style unless xflip is set). |
| `output_anat_preproc` | `neuro/anat/t1w` | Preprocessed T1w image (in MNI152NLin2009cAsym space if selected). |
| `output_dseg` | `neuro/parcellation/volume` | QSIPrep tissue segmentation (dseg) as a volume parcellation. |
| `output_brainmask` | `neuro/mask` | Brain mask from the anatomical workflow. |
| `output_report` | `report/html` | QSIPrep HTML report with figures. |
| `regressors` | `neuro/regressors` | Per-volume confounds table (regressors.tsv) from QSIPrep. |
| `dwiqc` | `raw` | raw directory containing dwi QC reports in dwiqc.json |

| Parameter | Type | Default | Description |
|---|---|---|---|
| `output_resolution` | number | `1.2` | The isotropic voxel size in mm the data will be resampled to after preprocessing. NOTE: only dwi data will be resampled. |
| `output_space` | enum | `T1w` | Volume and surface spaces to resample dwis into. NOTE: If selecting T1w, the preprocessed T1w image defines the T1w space, not the native T1. Reconstructed surfaces will be registered to the T1w space (ACPC), and not to the input images. WARNING: If selecting template, dwis will be still resampled to the T1w space (and not to the template). Options: `T1w`, `MNI152NLin2009cAsym`. |
| `skipbidsvalidation` | boolean | `false` | Skip the BIDS validation of input data. Try this option if your data is not BIDS compatible but you'd like to go ahead and process it through qsiprep anyway. |
| `denoise_method` | enum | `dwidenoise` | Image-based denoising method. Options: `dwidenoise`, `patch2self`, `none`. |
| `distortion_group_merge` | enum | `none` | How to combine images across distorted groups (only in case of multi dwi inputs). (at the moment only 'none' can be run). Options: `none`, `average`, `concat`. |
| `unringing_method` | enum | `none` | Method for Gibbs-ringing removal. Options: `none`, `mrdegibbs`. |
| `hmc_transform` | enum | `Affine` | Transformation to be optimized during head motion correction. Options: `Affine`, `Rigid`. |
| `infant` | boolean | `false` | Configure pipelines to process infant brains. |
| `syn_sdc` | boolean | `false` | EXPERIMENTAL: Use fieldmap-free distortion correction. |
| `force_syn` | boolean | `false` | EXPERIMENTAL/TEMPORARY: Use SyN correction in addition to fieldmap correction, if available. |
| `xflip` | boolean | `false` | Save output bvecs in MRtrix-style. If false (default), bvecs will be saved in FSL-style and will be compatible with DIPY and DSI Studio. |

Runtime: container `pennbbl/qsiprep:0.15.3`; needs `FREESURFER_LICENSE`.

Please cite:
- Cieslak M. et al. QSIPrep: An integrative platform for preprocessing and reconstructing diffusion MRI. bioRxiv 2020.09.04.282269. [doi:10.1101/2020.09.04.282269](https://doi.org/10.1101/2020.09.04.282269)
- Avesani P. et al. The open diffusion data derivatives. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

<!-- brainlife-app:end -->

This App runs [QSIPrep](https://github.com/pennbbl/qsiprep) on the [brainlife.io](https://brainlife.io/) interface. QSIPrep configures pipelines for processing diffusion-weighted MRI (dMRI) data. This App implements only the preprocessing piplines (and not the reconstruction pipelines). The preprocessing pipelines are built based on the available BIDS inputs, ensuring that fieldmaps are handled correctly. The preprocessing workflow performs head motion correction, susceptibility distortion correction, MP-PCA denoising, coregistration to T1w images, spatial normalization using ANTs and tissue segmentation.

#### References and resources to consider
* QSIPrep paper: https://www.nature.com/articles/s41592-021-01185-5
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
We ask that you cite the following articles when publishing papers that used data, code or other resources created by the brainlife.io community.

1. Matthew Cieslak, Philip A. Cook, Xiaosong He, Fang-Cheng Yeh, Thijs Dhollander, Azeez Adebimpe, Geoffrey K. Aguirre, Danielle S. Bassett, Richard F. Betzel, Josiane Bourque, Laura M. Cabral, Christos Davatzikos, John Detre, Eric Earl, Mark A. Elliott, Shreyas Fadnavis, Damien A. Fair, Will Foran, Panagiotis Fotiadis, Eleftherios Garyfallidis, Barry Giesbrecht, Ruben C. Gur, Raquel E. Gur, Max Kelz, Anisha Keshavan, Bart S. Larsen, Beatriz Luna, Allyson P. Mackey, Michael Milham, Desmond J. Oathes, Anders Perrone, Adam R. Pines, David R. Roalf, Adam Richie-Halford, Ariel Rokem, Valerie J. Sydnor, Tinashe M. Tapera, Ursula A. Tooley, Jean M. Vettel, Jason D. Yeatman, Scott T. Grafton, Theodore D. Satterthwaite. QSIPrep: An integrative platform for preprocessing and reconstructing diffusion MRI.
bioRxiv 2020.09.04.282269; doi: https://doi.org/10.1101/2020.09.04.282269

2. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Running the App 

### On Brainlife.io

Check out the brainlife app [here](https://doi.org/10.25663/brainlife.app.246)

### Running Locally

Information on how to run QSIPrep locally can be found here: https://qsiprep.readthedocs.io/en/latest/usage.html#

### Inputs

You would need a T1w image and (at least) one DWI volume. If you input a second DWI, be sure that it has an opposite Phase Encoding Direction than the first DWI. At the moment, no more than 2 DWIs can be selected.
  
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
