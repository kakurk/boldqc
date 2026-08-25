# Developer Guide

## Dependencies
BOLDQC is built upon [FSL][], [dcm2niix][], and a custom Python-based NIfTI
quality assessment library. The [container][Container] is based on Rocky Linux.

| Package        | Version        | Download                             |
|----------------|----------------|--------------------------------------|
| [Rocky Linux][]| `8`            | [:material-download:][Rocky Linux DL]|
| [FSL][]        | `6.0.4`        | [:material-download:][FSL DL]        |
| [dcm2niix][]   | `v1.0.20260724`| [:material-download:][dcm2niix DL]   |

## Pipeline overview
The BOLDQC pipeline consists of two main processing tasks: `niftiqa_wrapper` 
and `stackcheck_ext`. Together, these tasks produce signal quality metrics, 
motion estimates, and snapshot images for a single BOLD fMRI run.

### niftiqa_wrapper
The `niftiqa_wrapper.py` script is a Python-based quality assessment tool that
computes voxel-wise statistics from a 4D BOLD NIfTI image. It produces derived
3D volumes (mean, standard deviation, SNR, slope, and mask) and generates 
mosaic thumbnail images using FSL's `slicer` command.

#### `niftiqa.py`
The core `niftiqa.py` script loads the 4D NIfTI image, discards an initial 
number of volumes (skip), applies an intensity-based mask, and computes the 
following derived volumes:

- **Mean** — temporal mean of the time series
- **StDev** — temporal standard deviation (ddof=1)
- **SNR** — voxel-wise signal-to-noise ratio (mean / stdev)
- **Slope** — linear regression slope across time points per voxel
- **Mask** — binary volume based on mean intensity threshold

It also generates a per-slice mean intensity report and a mean slice intensity
plot.

```bash
niftiqa.py --skip 4 --mask-threshold ${MASK_THRESHOLD} --mean-slice-plot-format png --all --output-dir ${OUTPUT_DIR} ${NIFTI}
```

#### `slicer`
After `niftiqa.py` completes, mosaic thumbnail images are generated for each 
derived 3D volume using FSL's `slicer` command

```bash
slicer ${INPUT_NIFTI} -u -S ${NTH_VOX} ${X_WIDTH} ${OUTPUT_PNG}
```

### stackcheck_ext
The `stackcheck_ext.sh` script performs orientation correction, signal quality
analysis, and motion estimation on a BOLD fMRI NIfTI image. It depends heavily
on FSL tools.

#### `fslorient`
Checks and enforces image orientation. If the image is in NEUROLOGICAL 
orientation, it is flipped to RADIOLOGICAL

```bash
fslorient -getorient ${NIFTI}
fslorient -swaporient ${NIFTI}
```

#### `fslswapdim`
Enforces LPI (Left-Posterior-Inferior) voxel dimensions on the input image

```bash
fslswapdim ${NIFTI} RL PA IS ${NIFTI}
```

#### `stackcheck_nifti`
Runs the core signal quality analysis, computing mean, mask, standard deviation,
and SNR volumes, along with a per-slice report

```bash
stackcheck_nifti --threshold ${THRESH} --skip ${SKIP} --report --mean --mask --stdev --snr --plot --input ${NIFTI} --output-basename ${OUTDIR}/${BASE}
```

#### `mcflirt`
Performs motion correction using FSL's `mcflirt`. Outputs rotation and 
translation parameters, transformation matrices, and RMS displacement files
(both relative and absolute)

```bash
mcflirt -in ${NIFTI} -report -plots -mats -rmsrel -rmsabs -refvol 0 -out ${OUTDIR}/moco
```

#### Motion parameter extraction
After `mcflirt` completes, motion parameters are extracted from the `.par` file
and reformatted into three data files:

| File        | Description                                              |
|-------------|----------------------------------------------------------|
| `${BASE}.dat`  | Absolute displacement (reordered columns from moco.par)  |
| `${BASE}.rdat` | Mean-centered displacement                               |
| `${BASE}.ddat` | Frame-to-frame relative displacement                     |

These data files are then used to compute summary motion statistics (mean, 
standard deviation, maximum) for translations and rotations in each axis, as
well as counts of movements exceeding 0.1mm and 0.5mm thresholds.

#### `fslmeants`
Calculates mean masked signal values for the derived volumes using FSL's 
`fslmeants`

```bash
fslmeants -i ${OUTDIR}/${BASE}_snr.nii -m ${OUTDIR}/${BASE}_mask.nii
fslmeants -i ${OUTDIR}/${BASE}_stdev.nii -m ${OUTDIR}/${BASE}_mask.nii
fslmeants -i ${OUTDIR}/${BASE}_mean.nii -m ${OUTDIR}/${BASE}_mask.nii
fslmeants -i ${OUTDIR}/${BASE}_slope.nii -m ${OUTDIR}/${BASE}_mask.nii
```

#### Motion and mean slice plots
Motion parameters and mean slice intensity data are plotted using matplotlib

```bash
# Motion plot: rotations (pitch, roll, yaw) and translations (x, y, z)
${OUTDIR}/${BASE}_motion.png

# Mean slice intensity plot
${OUTDIR}/${BASE}_meanSlice.png
```

#### Auto report
A comprehensive text report (`${BASE}_autoReport.txt`) is generated containing
all computed QC metrics, motion statistics, and processing provenance.

## Mask threshold
The mask threshold is automatically determined based on the DICOM metadata
fields `BitsStored` and `ReceiveCoilName`:

| Bits Stored | Receive Coil         | Threshold |
|-------------|----------------------|-----------|
| any         | `HeadNeck_20`        | 3000.0    |
| 12          | any                  | 150.0     |
| 16          | `Head_32`            | 1500.0    |
| 16          | `Head_64`/`HeadNeck_64` | 3000.0 |


[FSL]: https://fsl.fmrib.ox.ac.uk/fsl/docs/
[FSL DL]: https://fsl.fmrib.ox.ac.uk/fsldownloads/
[dcm2niix]: https://github.com/rordenlab/dcm2niix
[dcm2niix DL]: https://github.com/rordenlab/dcm2niix/releases/tag/v1.0.20260724
[Rocky Linux]: https://rockylinux.org/
[Rocky Linux DL]: https://hub.docker.com/layers/library/rockylinux/8
[Container]: ../admin/#downloading-the-container
