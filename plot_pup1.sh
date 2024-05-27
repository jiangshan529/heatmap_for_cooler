
## usage
# python ~/script/plot_pup1.sh cool1 cool2 /broad/boxialab/shawn/projects/J/self_data/ChIP-seq/12-22/1.mapping/HCT116_J_chip_85_87_sort_dedup_q005_peaks.narrowPeak 10-9 10-10 0.6 1.4 -0.2 0.2

 

input_cool1=$1
input_cool2=$2
bed=$3
output1=$4
output2=$5
vmin=$6
vmax=$7
vmindiff=$8
vmaxdiff=$9




bedtools intersect -a $bed -b /broad/boxialab/index/hg38/black_list/hek293T_black_list.bed -v|uniq > aa
sed 's/^chr//' aa > aa_nochr.bed
coolpup.py $input_cool1 aa_nochr.bed --outname ${output1}.txt --flank 250000 --local --n_proc 16 --clr_weight_name ""
coolpup.py $input_cool2 aa_nochr.bed --outname ${output2}.txt --flank 250000 --local --n_proc 16 --clr_weight_name ""
python ~/script/plot_pup.py --input ${output1}.txt,${output2}.txt --vmin $vmin --vmax $vmax --vmin_diff $vmindiff --vmax_diff $vmaxdiff
