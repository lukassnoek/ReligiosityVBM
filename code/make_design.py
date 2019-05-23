import os.path as op
import pandas as pd
import nibabel as nib
import numpy as np
from glob import glob
from tqdm import tqdm

demogr_file = '../privacy_sensitive_data/DEMOGRAPHICS.tsv'
df = pd.read_csv(demogr_file, sep='\t', index_col=0)
df = df.loc[:, ['age', 'gender', 'raven_score']]
df = df.dropna(how='any')
print("N subjects with complete demographic data: %i" % df.shape[0])

#for col in ['age', 'raven_score']:
#    df.loc[:, col + '_zscore'] = (df.loc[:, col] - df.loc[:, col].mean()) / df.loc[:, col].std()

df.loc[:, 'gender'] = df.loc[:, 'gender'].map({1: 'Male', 2: 'Female'})
df = pd.concat((df, pd.get_dummies(df.loc[:, 'gender'])), axis=1)#.drop('gender', axis=1)

reli_file = '../privacy_sensitive_data/RELIGIOSITY.csv'
df_r = pd.read_csv(reli_file)
df_r['nummer'] = ['sub-' + str(s).zfill(4) for s in df_r['nummer']]
df_r = df_r.set_index('nummer')
df_r = df_r.rename(columns={'RELIGIOSITY_KEY': 'religious belief', 'MYSTICAL_EXP_KEY': 'mystical experience', 'raven_score': 'intelligence'})
df_r = df_r.drop(['RELI5', 'RELI6'], axis=1)  # open questions

df = pd.concat((df, df_r), sort=True, axis=1).dropna(how='any')#.loc[:, ['religiosity', 'mystical_exp', 'religiosity_zscore', 'mystical_exp_zscore']]), sort=True, axis=1).dropna(how='any')
print("N subjects with both demographic and reli data: %i" % len(df))

vbm_4D_file = '../bids/derivatives/vbm/stats/GM_mod_merg_s3.nii.gz'
vbm_4D_img = nib.load(vbm_4D_file)
gm_files = sorted(glob('../bids/derivatives/fmriprep/sub*/anat/*T1w_class-GM_probtissue.nii.gz'))
print("N subjects with complete MRI data: %i" % len(gm_files))


to_keep = np.ones(len(gm_files)).astype(bool)
for i, gm_file in tqdm(enumerate(gm_files)):
    sub_id = op.basename(gm_file).split('_')[0]
    img = nib.load(gm_file).get_data()
    nonzero_vox = (img > 0).sum()

    if sub_id in df.index:
        df.loc[sub_id, 'brain_size'] = nonzero_vox
    else:
        to_keep[i] = False

vbm_4D_data = vbm_4D_img.get_data()
vbm_4D_data = vbm_4D_data[:, :, :, to_keep]
vbm_4D_img = nib.Nifti1Image(vbm_4D_data, affine=vbm_4D_img.affine)
vbm_4D_img.to_filename(vbm_4D_file.replace('.nii.gz', '_cut.nii.gz'))

print("VBM file size: %i" % vbm_4D_data.shape[-1])

df = df.dropna(how='any')  # removes subs without brainsize
print("N subjects with complete MRI and demographic data: %i" % df.shape[0])
df.to_csv('../privacy_sensitive_data/PREDICTORS.tsv', sep='\t', index=True)
