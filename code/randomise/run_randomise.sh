FSLPARALLEL=30
export FSLPARALLEL
randomise_parallel -i ../vbm/stats/GM_mod_merg_s3_cut.nii.gz -o reli_analysis -d design.mat -t design.con -f design.fts -n 10000 -x -T --uncorrp -R -m /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask_dil1.nii.gz 

