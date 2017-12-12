## README


the size of the parent population
> mu= *int*

the size of the offspring population
> lambda=*int*

flag: 0 for plus (μ + λ)-EA | 1 for comma (μ , λ)-EA
> survival_strategy= *0* or *1*

flag: 0 for truncation | 1 for tournament selection
> survival_selection= *0* or *1*

size of tournament for survival selection method
> t_size=*int*

penalty coefficient for parsimony pressure, 0 for no coefficient (off)
> penalty=*int*

flag: 0 for termination based on total number of evals | 1 for termination based on no change in fitness over n evals
> terminate= *0* or *1*

value for termination convergence criterion
> n_value= *int*

over-selection rank crossover point, from 0-100 in terms of percent
> over_selection= *int*

flag: 0 for fitness proportion selection | 1 for over-selection
> parent_selection= *int*

percentage of opponents that will be compared against in coevolutionary fitness sampling, value from 0 to 100
> sampling_percentage= *int*

the sequence length specifying the number of iterations to play
> length_iterations= *int*

the maximum length of the agent memory
> max_memory_length= *int*

the maximum tree depth, where d = 0 would be a tree consisting of just a root which would be a single terminal node
> tree_depth= *int*

Seed for randomization. 'None' for time based randomization
> seed= *int* or *"None"*

the number of runs a single experiment consists of
> runs= *int*

the total number of evaluations per run
> evaluations= *int*

filename / location for logging every program run.
> log_file=*"logs/log"*

filename / location for recording the best-run result.
> sol_file=*"solutions/solution"*
