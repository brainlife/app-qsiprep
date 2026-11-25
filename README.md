<h1 align="center">QSIPrep preprocessing</h1>

<p align="center">
  Preprocessed diffusion MRI in T1w space, a preprocessed T1w image, brain mask, tissue segmentation and an HTML QC report, from a T1w image and one or two DWI runs.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.246"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.246-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> **This branch, `0.15.3`, is the brainlife.io App QSIPrep - Preprocessing workflow** ([doi:10.25663/brainlife.app.246](https://doi.org/10.25663/brainlife.app.246)).

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Preprocesses DWI with QSIPrep 0.15.3 (denoising, head motion and eddy correction, susceptibility distortion correction, coregistration to the T1w) and outputs the preprocessed DWI, T1w, brain mask, tissue segmentation and HTML report.**

Converts the inputs to BIDS and runs the QSIPrep preprocessing workflow only (no reconstruction), with denoising, unringing and head-motion transform as chosen, resampling the DWI to the requested isotropic resolution in T1w (ACPC) space. Use it as a complete diffusion preprocessing pipeline when you have a T1w image and one or two DWI runs; a second DWI must have the opposite phase-encoding direction, and fieldmaps are used when provided. Needs a FreeSurfer license (used by QSIPrep).

| | |
|---|---|
| **Inputs** | `neuro/anat/t1w` · `neuro/dwi` · `neuro/fmap` (optional) |
| **Outputs** | `neuro/dwi` · `neuro/anat/t1w` · `neuro/parcellation/volume` · `neuro/mask` · `report/html` · `neuro/regressors` · `raw` |
| **Container** | `pennbbl/qsiprep:0.15.3` |
| **Requires** | `FREESURFER_LICENSE` |
| **Run it** | [doi.org/10.25663/brainlife.app.246](https://doi.org/10.25663/brainlife.app.246) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `t1` | `neuro/anat/t1w` (!qsiprep) | yes | T1 anatomical image. |
| `dwi` | `neuro/dwi` (!qsiprep, !preprocessed) | yes | DWI volume(s). If you input a second DWI, be sure that it has an opposite Phase Encoding Direction than the first DWI. At the moment, no more than 2 DWIs can be selected. |
| `fmap` | `neuro/fmap` | no | fieldmap |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output_dwi` | `neuro/dwi` | Preprocessed DWI in T1w space with bvals and bvecs (FSL-style unless xflip is set). |
| `output_anat_preproc` | `neuro/anat/t1w` | Preprocessed T1w image (in MNI152NLin2009cAsym space if selected). |
| `output_dseg` | `neuro/parcellation/volume` | QSIPrep tissue segmentation (dseg) as a volume parcellation. |
| `output_brainmask` | `neuro/mask` | Brain mask from the anatomical workflow. |
| `output_report` | `report/html` | QSIPrep HTML report with figures. |
| `regressors` | `neuro/regressors` | Per-volume confounds table (regressors.tsv) from QSIPrep. |
| `dwiqc` | `raw` | raw directory containing dwi QC reports in dwiqc.json |

<details>
<summary><b>Parameters</b> (11)</summary>

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

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.246](https://doi.org/10.25663/brainlife.app.246), choose a T1-weighted image, one or two DWI runs and, optionally, a fieldmap, set the options and press **Execute**.

The App runs [QSIPrep](https://github.com/pennbbl/qsiprep) 0.15.3. QSIPrep configures pipelines for diffusion-weighted MRI; this App implements only the preprocessing pipelines, not the reconstruction pipelines. The preprocessing pipeline is built from the available BIDS inputs, so fieldmaps are handled correctly, and performs head motion correction, susceptibility distortion correction, denoising, coregistration to the T1w image, spatial normalisation with ANTs and tissue segmentation.

Inputs:

- a T1w image and at least one DWI run. If you add a second DWI, it must have the opposite phase-encoding direction to the first; no more than two DWIs can be selected at the moment;
- optionally, a `neuro/fmap` fieldmap, used when provided.

Main options:

- `output_resolution` (default 1.2): isotropic voxel size in mm for the preprocessed DWI (only the DWI is resampled);
- `output_space`: `T1w` (default; the preprocessed T1w defines the space, not the native T1) or `MNI152NLin2009cAsym` for the anatomical outputs;
- `denoise_method` (`dwidenoise`, `patch2self` or `none`), `unringing_method` (`none` or `mrdegibbs`) and `hmc_transform` (`Affine` or `Rigid`);
- `distortion_group_merge` for two DWI runs (only `none` can be run at the moment);
- `syn_sdc` (experimental fieldmap-free distortion correction), `infant`, `skipbidsvalidation`;
- `xflip`: save bvecs in MRtrix style; by default they are FSL style, compatible with DIPY and DSI Studio.

### Locally

`main` relies on brainlife.io's `bl2bids` to convert the inputs to BIDS, so outside brainlife.io it is usually simpler to run QSIPrep directly; see the [QSIPrep usage documentation](https://qsiprep.readthedocs.io/en/latest/usage.html). To run `main` itself you need [Singularity/Apptainer](https://apptainer.org/), [`jq`](https://jqlang.github.io/jq/), `bl2bids` and a [FreeSurfer license](https://surfer.nmr.mgh.harvard.edu/registration.html) (QSIPrep uses it), and a `config.json` like [`config.json.sample`](config.json.sample), with the input paths, the options above and the `_inputs` metadata brainlife.io writes. Check out the branch brainlife.io runs (`git checkout 0.15.3`) and run `./main`.

## Outputs

```text
output_dwi/            dwi.nii.gz, dwi.bvals, dwi.bvecs: preprocessed DWI in T1w space
output_anat_preproc/   t1.nii.gz: preprocessed T1w (in MNI152NLin2009cAsym if selected)
output_dseg/           parc.nii.gz: tissue segmentation
output_brainmask/      mask.nii.gz: brain mask
output_report/html/    QSIPrep HTML report with figures
regressors/            regressors.tsv: per-volume confounds
dwiqc/                 dwiqc.json: DWI QC metrics
```

## Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Cieslak M, Cook PA, He X, Yeh F-C, Dhollander T, Adebimpe A, Aguirre GK, Bassett DS, Betzel RF, Bourque J, Cabral LM, Davatzikos C, Detre J, Earl E, Elliott MA, Fadnavis S, Fair DA, Foran W, Fotiadis P, Garyfallidis E, Giesbrecht B, Gur RC, Gur RE, Kelz M, Keshavan A, Larsen BS, Luna B, Mackey AP, Milham M, Oathes DJ, Perrone A, Pines AR, Roalf DR, Richie-Halford A, Rokem A, Sydnor VJ, Tapera TM, Tooley UA, Vettel JM, Yeatman JD, Grafton ST, Satterthwaite TD. QSIPrep: an integrative platform for preprocessing and reconstructing diffusion MRI. *Nature Methods* (2021). [Article](https://www.nature.com/articles/s41592-021-01185-5); preprint [doi:10.1101/2020.09.04.282269](https://doi.org/10.1101/2020.09.04.282269)
- QSIPrep - Preprocessing workflow. brainlife.io App. [doi:10.25663/brainlife.app.246](https://doi.org/10.25663/brainlife.app.246)
- Avesani P. et al. The open diffusion data derivatives. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Tournier et al. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. *NeuroImage* 202:116137 (2019). [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137)
- Cieslak et al. QSIPrep: an integrative platform for preprocessing and reconstructing diffusion MRI data. *Nature Methods* 18:775-778 (2021). [doi:10.1038/s41592-021-01185-5](https://doi.org/10.1038/s41592-021-01185-5)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)

## Authors

- Franco Pestilli (project director)
- Giulia Bertò ([@giulia-berto](https://github.com/giulia-berto))
- Soichi Hayashi ([@soichih](https://github.com/soichih))

**Contributors:** Brad Caron, Ashley Stewart, Sangmin Yi, Anibal Sólon, Steven Meisler

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

This material is based upon work supported by the National Science Foundation Graduate Research Fellowship under Grant No. 1342962. Any opinion, findings, and conclusions or recommendations expressed in this material are those of the authors(s) and do not necessarily reflect the views of the National Science Foundation.

## License

[MIT](LICENSE). QSIPrep itself is distributed under its own license.
