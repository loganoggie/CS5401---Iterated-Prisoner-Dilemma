#!/bin/bash

config=$1

. $config

python3 ipd.py -l $length_iterations -k $max_memory_length -d $tree_depth -s $seed -r $runs -e $evaluations -lf $log_file -sf $sol_file -lm $lambda -mu $mu -ss $survival_selection -t $t_size -p $penalty -tm $terminate -n $n_value -x $over_selection -ps $parent_selection -st $survival_strategy -sp $sampling_percentage
