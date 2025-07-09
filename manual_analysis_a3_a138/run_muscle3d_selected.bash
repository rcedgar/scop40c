/mnt/c/src/reseek/github_releases/reseek-v2.5-linux-x86 -pdb2mega selected.files -output structs_selected.mega
muscle -align structs_selected.mega -output muscle3d_selected.afa
reseek -msta_lddtmuw muscle3d_selected.afa --input selected.files -lddtmuw_jalview jalview_selected.txt
