import nibabel as nib
import numpy as np
from nilearn.datasets import load_mni152_template

affine = load_mni152_template().affine

ofc = nib.load('../rois/OFC_prob.nii.gz').get_data()
ofc = (ofc > 0).astype(int)
nib.Nifti1Image(ofc, affine=affine).to_filename('../rois/OFC_bin.nii.gz')

ang_gyrus = nib.load('../rois/AngularGyrus.nii.gz').get_data()
smg_ant = nib.load('../rois/SMG_ant.nii.gz').get_data()
smg_post = nib.load('../rois/SMG_post.nii.gz').get_data()
ipl = ang_gyrus + smg_ant + smg_post
ipl[ipl > 100] = 100
nib.Nifti1Image(ipl / 100, affine=affine).to_filename('../rois/IPL_prob.nii.gz')
nib.Nifti1Image((ipl > 0).astype(int), affine=affine).to_filename('../rois/IPL_bin.nii.gz')

mtl_ant = nib.load('../rois/MTL_right_ant.nii.gz').get_data()
mtl_post = nib.load('../rois/MTL_right_post.nii.gz').get_data()
mtl = mtl_ant + mtl_post
mtl[mtl > 100] = 100
nib.Nifti1Image(mtl / 100, affine=affine).to_filename('../rois/MTL_prob.nii.gz')
nib.Nifti1Image((mtl > 0).astype(int), affine=affine).to_filename('../rois/MTL_bin.nii.gz')

hipp_left = nib.load('../rois/Hippocampus_left.nii.gz').get_data()
hipp_right = nib.load('../rois/Hippocampus_right.nii.gz').get_data()
hipp = hipp_left + hipp_right
hipp[hipp > 100] = 100
nib.Nifti1Image(hipp / 100, affine=affine).to_filename('../rois/Hippocampus_prob.nii.gz')
nib.Nifti1Image((hipp > 0).astype(int), affine=affine).to_filename('../rois/Hippocampus_bin.nii.gz')
