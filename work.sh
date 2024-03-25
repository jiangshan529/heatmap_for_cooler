### example usage: 
### to plot three heatmap(matrix1, matrix2, diff_matrix)
##python work.py --input aa.txt,bb.txt --vmin 0.6 --vmax 1.4 --vmin_diff -0.5 --vmax_diff 0.5
### plot a single matrix
##python work.py --input aa.txt --vmin 0.6 --vmax 1.4


## get a bed file on its center and remove chr for coolpup
less aa.bed|awk -v OFS='\t' '{print $1,int(($2+$3)/2),int(($2+$3)/2)}' > aa_center.bed
sed 's/^chr//' aa_center.bed > aa_center_nochr.bed

split -d -l 2000 aa_center_nochr.bed aa_

# Step 2: Run coolpup.py on each split file
for split_file in aa_{00..07}; do
    # Run coolpup.py on each split file
    mv "$split_file" "$split_file.bed"
    coolpup.py HEK_WT1_merge_UU_dedup.pairs_5k.cool ${split_file}.bed --outname HEK_WT1_merge_on_${split_file}_5k.txt --flank 250000 --local --n_proc 16 --clr_weight_name ""
    
    coolpup.py HEK_KO_merge_UU_dedup.pairs_5k.cool ${split_file}.bed --outname HEK_KO_merge_on_${split_file}_5k.txt --flank 250000 --local --n_proc 16 --clr_weight_name ""
        
    python plot_pup.py --input HEK_WT1_merge_on_${split_file}_5k.txt,HEK_KO_merge_on_${split_file}_5k.txt --vmin 0.6 --vmax 1.4 --vmin_diff -0.2 --vmax_diff 0.2
done
