XNAT user documentation
=======================
.. _XNAT: https://doi.org/10.1385/NI:5:1:11
.. _command.json: https://github.com/harvard-nrg/anatqc/blob/xnat-1.7.6/command.json
.. _BOLD: https://tinyurl.com/dxs6zj2z

Tagging your scans
------------------
For BOLDQC to discover `BOLD`_ scans to process, you need to set the scan *type* in `XNAT`_

========= ========================
Type      Example series              
========= ========================
BOLD      ``ABCD_fMRI_rest_noPMU``
========= ========================

The image below displays an MR Session report page with populated types 

.. image:: images/xnat-scan-types.png

Running the pipeline
--------------------
To run the BOLDQC pipeline, use the ``Run Containers > boldqc-session`` button located within the ``Actions`` box on the MR Session report page

.. note::
   If you don't see the ``Run Containers`` menu, please refer to `Setting up the container <developers.html#setting-up-the-container>`_.

.. image:: images/xnat-run-button.png


This should bring up a small form with any configurable settings. Continue reading for a description of each setting

.. image:: images/xnat-container-form.png

run
^^^
.. note::
   The ``run`` number is *not* the scan number. If scan ``17`` was the first 
   BOLD scan within the MR session, the ``run`` number would be ``1``, the 
   second BOLD scan would be run ``2``, and so on.

This should be set to the integer value of the BOLD scan you want to process. 

Understanding the report page
-----------------------------
The following section will break down each section of the BOLDQC report page.

.. image:: images/xnat-eqc-home.png

Left pane
^^^^^^^^^
The left pane is broken up into several distinct sections. Each section will be described below.

Summary
"""""""
The ``Summary`` pane orients the user to what MR Session they're currently looking at and various processing details

.. image:: images/xnat-eqc-left-summary.png

============== ===================
Key            Description
============== ===================
MR Session     MR Session label
Processed      Processing date
BOLD scan      Processed BOLD scan
============== ===================

Parameters
""""""""""
The ``Parameters`` pane displays fine-grained scan information

.. image:: images/xnat-eqc-left-parameters.png

============== =========================================
Key            Description
============== =========================================
Num Volumes    Number of time points
Num Voxels     Number of voxels included in the analysis
Mask Threshold Masking threshold
Skip           Number of initial time points discarded
============== =========================================

QC Metrics
""""""""""
The ``QC Metrics`` pane displays quality control metrics computed *over the entire volume*

.. image:: images/xnat-eqc-left-qcmetrics.png

================= ============================================
Metric            Description                              
================= ============================================
Mean              Mean signal intensity
StDev             Mean voxel Standard deviation
Slice SNR         Mean slice-based SNR (sensitive to motion)
Voxel SNR         Mean voxel SNR
Mean Rel Motion   Mean relative translations in 3D (mm)
Max Rel Motion    Maximum relative motion (mm)
Mean Abs Motion   Mean absolute motion in 3D (mm)
Max Abs Motion    Maximum absolute motion in 3D (mm)
Movements (>.1mm) Number of relative translations in 3D > .1mm
Movements (>.5mm) Number of relative translations in 3D > .5mm
================= ============================================

Files
"""""
The ``Files`` pane contains the most commonly requested files. Clicking on any of these files will display that file in the browser

.. image:: images/xnat-eqc-left-files.png

======================= ===========================================
File                    Description
======================= ===========================================
SNR Image               BOLD signal SNR image, axiale
Mean Image              BOLD signal mean image, axial
StDev Image             BOLD signal standard deviation image, axial
Mask Image              Masked image
Mean Slice Image        BOLD signal mean slice intensity plot
Motion Data             Motion (translations and rotations) plot
Slope Image             BOLD signal slope image, axial
Auto QC Report          Automated QC report
Slice Report            Individual slice QC report
======================= ===========================================

Tabs
^^^^
To the right of the `left pane <#left-pane>`_ left pane you’ll find a tab container. 

Images
""""""
The ``Images`` tab displays a zoomed out view of the SNR, Mean, Standard 
Deviation, Slope, MEan Slice Intensity, Motion, and Mask images

.. image:: images/xnat-eqc-images-tab.png

Clicking on any of these images will display a larger version of the image

.. image:: images/xnat-eqc-zoom.png

Automated QC
""""""""""""
The ``Automated QC`` tab displays a complete list of BOLDQC metrics.

.. image:: images/xnat-eqc-autoqc-tab.png

Manual QC
"""""""""
The ``Manual QC`` tab contains a form allowing a quality control 
technician to record additional observations, comments, and assign 
a final ``PASS``, ``WARN``, or ``FAIL`` grade to the scan

.. image:: images/xnat-eqc-manualqc-tab.png

All Stored Files
""""""""""""""""
The ``All Stored Files`` tab contains a list of *every file* stored by BOLDQC

.. image:: images/xnat-eqc-files-tab.png

.. note::
   Clicking on a file within the ``All Stored Files`` tab will download the file.

============================= ==========================================
File                          Description
============================= ==========================================
``*_EQC_auto_report.txt``     Automated QC report
``*_EQC_mask_thumbnail.png``  Mask snapshot image
``*_EQC_mask.nii.gz``         Mask NIFTI
``*_EQC_mean_thumbnail.png``  Mean snapshot image
``*_EQC_mean.nii.gz``         Mean NIFTI
``*_EQC_mean_slice.txt``      Mean slice intensity data
``*_EQC_mean_slice.png``      Mean slice intensity plot
``*_EQC_motion.png``          Motion plot
``*_EQC_slice_report.txt``    Slice report
``*_EQC_slope_thumbnail.png`` Slope snapshot image
``*_EQC_slope.nii.gz``        Slope NIFTI
``*_EQC_snr_thumbnail.png``   SNR snapshot image
``*_EQC_snr.nii.gz``          SNR NIFTI
``*_EQC_stdev_thumbnail.png`` Standard deviation snapshot image
``*_EQC_stdev.nii.gz``        Standard deviation image
============================= ==========================================

