those scripts are to plot Aggregate plot for coolpup. the script for myself is in ~/script/plot_pup1.sh and ~/script/plot_pup.py

## usage
 python ~/script/plot_pup1.sh cool1 cool2 /broad/boxialab/shawn/projects/J/self_data/ChIP-seq/12-22/1.mapping/HCT116_J_chip_85_87_sort_dedup_q005_peaks.narrowPeak 10-9 10-10 0.6 1.4 -0.2 0.2

### this code to plot 2 matrixs and its difference map

python work.py --input aa.txt,bb.txt --vmin 0.6 --vmax 1.4 --vmin_diff -0.2 --vmax_diff 0.2
![image](https://github.com/jiangshan529/heatmap_for_cooler/assets/75197626/fd89ea3a-8e52-4475-a5fa-79b6214704cd)

### or to plot a single heatmap for one matrix

python work.py --input HEK_WT1_merge_on_hek_H7_J_on_H7_merge_q0.05_CTCF_cobound_descend_00_5k.txt --vmin 0.6 --vmax 1.4
![image](https://github.com/jiangshan529/heatmap_for_cooler/assets/75197626/344bb5e9-da4a-4720-a33a-f2f1a7915d75)
