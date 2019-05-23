import numpy as np
import pandas as pd
import os.path as op
import nibabel as nib
from nilearn import image
from nilearn.datasets import fetch_atlas_harvard_oxford
from nilearn import masking
from tqdm import tqdm

vbm = nib.load('../bids/derivatives/vbm/stats/GM_mod_merg_s3_cut.nii.gz').get_data()

rois = ['OFC', 'IPL', 'Hippocampus', 'MTL']

df_cov = pd.read_csv('../privacy_sensitive_data/PREDICTORS.tsv', sep='\t', index_col=0)
df = pd.DataFrame()
for roi in tqdm(rois, desc='Looping across ROIs'):

    for ext in ['bin']:#['bin', 'prob']:
        roi_path = f'../rois/{roi}_{ext}.nii.gz'
        mask = nib.load(roi_path).get_data()
        if ext == 'bin':
            vals = vbm[mask.astype(bool), :].mean(axis=0)
        else:
            vals = (vbm * mask[..., np.newaxis]).mean(axis=(0, 1, 2))
        df[roi] = vals
        #df[f'{roi}_{ext}'] = vals

df.index = df_cov.index
df_all = pd.concat((df_cov, df), axis=1)
df_all['subject'] = np.random.permutation(df_all.index)  # shuffle sub-ids!
df_all = df_all.set_index('subject').reset_index()
df_all = df_all.sort_values(by='subject')
df_all.to_csv('../ReligiosityVBM_AllData.csv', index=False)
