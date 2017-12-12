# Logan Nielsen
# Assignment 2, CS5401

# ARGPARSE FILE

from main import program
import argparse
import random
import time

def main():
    p = argparse.ArgumentParser()

    p.add_argument('-mu','--mu', help = "the size of the parent population", type = int)
    p.add_argument('-lm','--lam', help = "the size of the offspring population", type = int)
    p.add_argument('-st','--survival_strategy', help = "flag: 0 for plus (μ + λ)-EA | 1 for comma (μ , λ)-EA", type = int)
    p.add_argument('-ss','--survival_selection', help = "flag: 0 for truncation | 1 for tournament selection", type = int, default = 0)
    p.add_argument('-t', '--tournament_size', help = "size of tournament for survival selection method", type = int, default = 10)
    p.add_argument('-p', '--parsimony_pressure', help = "penalty coefficient for parsimony pressrue, 0 for no coefficient (off)", type = int, default = 0)
    p.add_argument('-ps','--parent_selection', help = "flag: 0 for fitness proportion selection | 1 for over-selection", type = int, default = 0)
    p.add_argument('-sp','--sampling_percentage', help = "percentage of opponents that will be compared against in coevolutionary fitness sampling, value from 0 to 100", type = int, default = 0)
    p.add_argument('-x', '--over_selection_value', help = "over-selection rank crossover point, from 0-100 in terms of percent", type = int, default = 20)
    p.add_argument('-tm','--termination', help = "flag: 0 for termination based on total number of evals | 1 for termination based on no change in fitness over n evals", type = int, default = 0)
    p.add_argument('-n', '--termination_criterion', help = "value for termination convergence criterion", type = int, default = 10)
    p.add_argument('-l', '--length_iterations', help = "the sequence length specifying the number of iterations to play", type = int)
    p.add_argument('-k', '--max_memory_length', help = 'the maximum length of the agent memory', type = int)
    p.add_argument('-d', '--tree_depth', help = "the maximum tree depth, where d = 0 would be a tree consisting of just a root which would be a single terminal node", type = int)
    p.add_argument('-s', '--seed', help = "Seed for randomization. 'None' for time based randomization.", default = "None")
    p.add_argument('-r', '--runs', help = "the number of runs a single experiment consists of", type = int, default = 30)
    p.add_argument('-e', '--evaluations', help="Total number of allowed evaluations per run", type = int, default = 10000)
    p.add_argument('-lf','--log_file', help = "filename / location for logging every program run.", default = "logs/log")
    p.add_argument('-sf','--sol_file', help = "filename / location for recording the best-run result.", default = "solutions/solution")
    args = p.parse_args() # creates the argument variables -- ex: args.instance_filename, args.seed, etc

    if args.seed == "None":
        args.seed = time.time()
    random.seed(args.seed)

    program(args.lam, args.mu, args.survival_strategy, args.survival_selection, args.tournament_size, args.parsimony_pressure, args.parent_selection,
                args.sampling_percentage, args.over_selection_value, args.termination, args.termination_criterion, args.length_iterations,
                    args.max_memory_length, args.tree_depth, args.seed, args.runs, args.evaluations, args.log_file, args.sol_file)


if __name__ == "__main__" :
    main()

"""
Implement single-population Coevolution and Genetic Programming to coevolve within a configurable number of runs and a configurable number of fitness evaluations per run.

Implement the IPD prisoner agent strategies which incur the least prison time versus the other coevolved strategies (relative fitness)

Test the fittest final population coevolved strategy (the locally best of the final generation over all runs) against a fixed tit-for-tat strategy (absolute fitness).

The (composite coevolutionary) fitness of a strategy is computed by averaging the fitness of that strategy against a sampling of its opponents, as determined by the
“coevolutionary fitness sampling percentage” strategy parameter where the minimum is one opponent and the maximum is μ + λ − 1 opponents.

Determining the fitness of a strategy against a particular opponent is accomplished by first playing 2k IPD rounds before starting to count scores towards fitness
(i.e., the fitness of a strategy against a given opponent strategy is proportional to its average payoff for the last l − 2k rounds after playing l rounds of IPDF);

To ensure a sufficient number of rounds to average over, you need to enforce l ≥ 3k.

The definition of “one fitness evaluation” is determining the fitness of one strategy against one other strategy. So if sampling requires a strategy to be pitted
against ten other strategies in order to determine its (composite coevolutionary) fitness, then that counts as ten fitness evaluations.

"""
