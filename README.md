# BOLD Quality Control (beta)
BOLDQC is an automated quality control pipeline for functional MRI scans. BOLDQC
is built on top of the excellent
[`dcm2niix`](https://github.com/rordenlab/dcm2niix), 
[`FreeSurfer`](https://surfer.nmr.mgh.harvard.edu/),
and
[`FSL`](https://fsl.fmrib.ox.ac.uk/fsl)
software packages.

For the latest documentation please head over to [boldqc.readthedocs.io](https://boldqc.readthedocs.io).

# BU BOLDQC Modifications

This repo contains modifications to the BOLDQC routine, including:

1. Modification of the tagging process to be in line with that of ANATQC.

By default, BOLDQC looks for the term BOLD within the notes field of XNAT scans. ANATQC, by contrast, looks for the term "#T1w_###" where ### is a zero padded identifier for the first, second, and so on T1w scan in this scan session. The changes made to the BOLDQC routine change the tags that it searches for to match this zero padding convention -- i.e., it looks for #BOLD_001, #BOLD_002, etc. in the notes field.