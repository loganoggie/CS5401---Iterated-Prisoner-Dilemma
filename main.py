# Logan Nielsen
# Assignment 2, CS5401

# MAIN PROGRAM FILE

import functions
import random
import variates
import agent
from decimal import Decimal
from tqdm import tqdm
import sys

def program(lam, mu, survival_strategy, survival_selection, tournament_size, parsimony_pressure, parent_selection, sampling_percentage, over_selection_value,
                termination, termination_criterion, length_iterations, max_memory_length, tree_depth, seed, runs, max_evals, log_file, sol_file):

    log_file = functions.FindFilename(log_file)
    sol_file = functions.FindFilename(sol_file)

    functions.StartLog(lam, mu, survival_strategy, survival_selection, tournament_size, parsimony_pressure, parent_selection, sampling_percentage,
                over_selection_value, termination, termination_criterion, length_iterations, max_memory_length, tree_depth, seed, runs, max_evals, log_file)

    overall_best_fitness = 0
    overall_best_controller = None

    for i in tqdm(range(int(runs)), unit='run', desc='Runs: ', dynamic_ncols=True):
        avg_fitness = 0
        best_fitness = 0
        best_controller = None
        best_agent = None
        functions.NewLogRun(i)
        num_evals = mu
        prev_fitness = 0
        counter = 0

        if termination == 0: ## terminates after max_evals is reached
            def Terminate(num_evals, avg_fitness):
                return num_evals >= max_evals

        elif termination == 1: ## terminates if avg fitness doesn't change over 'n' evaluations
            def Terminate(num_evals, avg_fitness):
                nonlocal prev_fitness
                nonlocal counter
                if avg_fitness == prev_fitness:
                    counter += 1
                else:
                    prev_fitness = avg_fitness
                    counter = 0
                if counter >= termination_criterion:
                    return True
                else:
                    return False

        # generate ramped half and half parent population
        parent_population = functions.CreateParents(mu, max_memory_length, tree_depth, length_iterations, parsimony_pressure)
        sample_size = round(len(parent_population) - 2) * sampling_percentage/100 + 1
        agent.Coevolution(sample_size, parent_population, length_iterations, max_memory_length, parsimony_pressure)
        avg_composite_fitness = sum([parent._rel_fitness for parent in parent_population]) / mu

        for parent in parent_population:
            if parent._rel_fitness > best_fitness:
                best_fitness = parent._rel_fitness
                best_controller = parent.controller
                best_agent = parent
                if best_fitness > overall_best_fitness:
                    overall_best_fitness = best_fitness
                    overall_best_controller = best_controller


        functions.LogEntry(num_evals, round(avg_composite_fitness, 4), round(best_fitness, 4))

        with tqdm(total=max_evals, desc='Evals', unit='eval', leave=False, dynamic_ncols=True, unit_scale=True) as progress_bar:
            while not Terminate(num_evals, avg_fitness):
                offspring_population = functions.CreateOffspringPopulation(lam, parent_selection, parent_population, over_selection_value, max_memory_length, tree_depth)
                if survival_strategy == 0: # plus strategy
                    offspring_population = offspring_population + parent_population
                elif survival_strategy == 1: # comma strategy, no change
                    offspring_population = offspring_population
                else:
                    raise ValueError("Invalid survival strategy selection -- Main File")

                sample_size = round(len(offspring_population) - 2) * sampling_percentage/100 + 1

                agent.Coevolution(sample_size, offspring_population, length_iterations, max_memory_length, parsimony_pressure)

                survivor_population = functions.CreateSurvivorPopulation(mu, survival_selection, offspring_population, tournament_size)
                parent_population = survivor_population

                num_evals += lam*sample_size
                progress_bar.update(lam*sample_size)

                avg_composite_fitness = sum([survivor._rel_fitness for survivor in survivor_population]) / mu

                for survivor in survivor_population:
                    if survivor._rel_fitness > best_fitness:
                        best_fitness = survivor._rel_fitness
                        best_controller = survivor.controller
                        best_agent = survivor
                        if best_fitness > overall_best_fitness:
                            overall_best_fitness = best_fitness
                            overall_best_controller = best_controller


                functions.LogEntry(num_evals, round(avg_composite_fitness, 4), round(best_fitness, 4))

                # format populations
                offspring_population = []
                survivor_population = []

            best_absolute_fitness = best_agent.abs_fitness
            functions.Absolute_Log_Entry(best_absolute_fitness)

    functions.CloseLog()

    functions.WriteSolution(sol_file, overall_best_controller)
