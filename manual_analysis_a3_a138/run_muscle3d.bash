/mnt/c/src/reseek/github_releases/reseek-v2.5-linux-x86 -pdb2mega big_pdb/ -output structs.mega
muscle -align structs.mega -output muscle3d.afa
reseek -msta_lddtmuw muscle3d.afa --input big_pdb/ -lddtmuw_jalview jalview.txt
