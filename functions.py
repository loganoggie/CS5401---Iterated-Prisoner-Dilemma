# Logan Nielsen
# Assignment 2, CS5401

# FUNCTIONS FILE

import variates
import agent
import os.path
import re
import random
from copy import deepcopy

def CreateParents(lam, max_memory_length, tree_depth, length_iterations, parsimony_pressure):
    parent_population = []
    while len(parent_population) <= lam:
        choice = random.randint(0,1)
        if choice == 0: # create full tree agent
            parent_population.append(agent.Create_Full_Agent(max_memory_length, tree_depth, parsimony_pressure, length_iterations))
        elif choice == 1: # create random depth agent
            parent_population.append(agent.Create_Rand_Agent(max_memory_length, tree_depth, parsimony_pressure, length_iterations))
        else:
            raise ValueError("Invalid random number generation -- CreateParents Function")
    return parent_population

def Recombination(parent1, parent2, tree_depth):
    parent1_location, parent1_node = parent1.Select_Random_Subtree()
    parent2_location, parent2_node = parent2.Select_Random_Subtree()
    parent1.Insert_Subtree(parent1_location, deepcopy(parent2_node))
    parent1.Controller_Depth_Check()
    return parent1

def Mutation(parent, max_memory_length, tree_depth):
    rand_num = random.randint(0,2)
    if rand_num == 0:
        rand_subtree = variates.Value.From_Random(max_memory_length)
    elif rand_num == 1:
        rand_subtree = variates.Univariate.From_Random(max_memory_length, 3)
    elif rand_num == 2:
        rand_subtree = variates.Bivariate.From_Random(max_memory_length, 3)
    else:
        raise ValueError("Invalid random number generation -- Mutation Function")

    location, _ = parent.Select_Random_Subtree()
    parent.Insert_Subtree(location, rand_subtree)
    parent.Controller_Depth_Check()
    return parent

def CreateOffspring(parent1, parent2, max_memory_length, tree_depth):
    # 50% chance of recombination, 50% chance of mutation
    rand_num = random.randint(0,1)
    if rand_num == 0:
        offspring = Recombination(parent1, parent2, tree_depth)
    else:
        offspring = Mutation(parent1, max_memory_length, tree_depth)
    return offspring


def CreateOffspringPopulation(lam, parent_selection, parent_population, over_selection_value, max_memory_length, tree_depth):
    offspring_population = []
    sorted_parent_population = list(sorted(parent_population, key=lambda parent: parent._rel_fitness))
    if parent_selection == 0: # fitness proportional selection
        while len(offspring_population) <= lam:
            parent1 = deepcopy(FitnessProportional(sorted_parent_population))
            parent2 = deepcopy(FitnessProportional(sorted_parent_population))
            offspring_population.append(CreateOffspring(parent1, parent2, max_memory_length, tree_depth))

    elif parent_selection == 1: # over-selection
        group1 = sorted_parent_population[len(sorted_parent_population)*over_selection_value//100:]
        group2 = sorted_parent_population[:len(sorted_parent_population)*over_selection_value//100]
        while len(offspring_population) <= lam:
            # 80% of choices come from group1 and 20% of choices come from group2
            rand_num = random.randint(1,5)
            if rand_num < 5:
                parent1 = deepcopy(FitnessProportional(group1))
            else:
                parent1 = deepcopy(FitnessProportional(group2))

            rand_num = random.randint(1,5)
            if rand_num < 5:
                parent2 = FitnessProportional(group1)
            else:
                parent2 = FitnessProportional(group2)

            offspring_population.append(CreateOffspring(parent1, parent2, max_memory_length, tree_depth))
    else:
        raise ValueError("Invalid parent selection value -- CreateOffspringPopulation Function")

    return offspring_population


def CreateSurvivorPopulation(mu, survival_selection, offspring_population, tournament_size):
    if survival_selection == 0: #truncation
        sorted_offspring_population = list(sorted(offspring_population, key=lambda offspring: offspring._rel_fitness))
        survivor_population = offspring_population[-mu:]
    elif survival_selection == 1: #tournament selection
        survivor_population = TournamentSelection(mu, tournament_size, offspring_population)
    else:
        raise ValueError("Invalid suvival selection value -- CreateSurvivorPopulation Function")
    return survivor_population


def FitnessProportional(tmpPopulation):
    fitness_sum = sum([tmp._rel_fitness for tmp in tmpPopulation])
    pick = random.uniform(0, fitness_sum - 1)
    val = 0
    for tmp in tmpPopulation:
        val += tmp._rel_fitness
        if val > pick:
            return tmp
    raise ValueError("Invalid fitness value -- FitnessProportionalSelection Function")


def TournamentSelection(mu, tournament_size, offspring_population): # WITHOUT REPLACEMENT
    survivor_population = set()
    while len(survivor_population) <= mu:
        tournament_population = set()
        while len(tournament_population) < tournament_size:
            tournament_population.add(offspring_population[random.randint(0, len(offspring_population) -1)])
        survivor_population.add(max(tournament_population, key=lambda tmp: tmp._rel_fitness))
    return list(survivor_population)


def FindFilename(filename):
    counter = 1
    while True:
        if os.path.isfile(filename):
            filename = re.sub(r'\d+', '', filename)
            filename = filename + str(counter)
            counter += 1
        else:
            break
    return filename


def WriteSolution(sol_file, overall_best_controller):
    with open(sol_file, 'w+') as f:
        f.write(str(overall_best_controller))


def StartLog(lam, mu, survival_strategy, survival_selection, tournament_size, parsimony_pressure, parent_selection, sampling_percentage, over_selection_value,
                termination, termination_criterion, length_iterations, max_memory_length, tree_depth, seed, runs, max_evals, log_file):
    global log
    log = open(log_file, 'w') # log.write(" ")
    log.write("Result Log\n\n")

    log.write("Parent Selection:   ")
    log.write(str(parent_selection))
    log.write("\n")
    log.write("Sampling percentage:   ")
    log.write(str(sampling_percentage))
    log.write("\n")
    log.write("Over Selection Value:   ")
    log.write(str(over_selection_value))
    log.write("\n")
    log.write("Surival Strategy:   ")
    log.write(str(survival_strategy))
    log.write("\n")

    log.write("Offspring Population Size (lambda):  ")
    log.write(str(lam))
    log.write("\n")
    log.write("Parent/Survivor Population Size (mu):  ")
    log.write(str(mu))
    log.write("\n")
    log.write("Survival Selection (k):  ")
    log.write(str(survival_selection))
    log.write("\n")
    log.write("Tournament Size:  ")
    log.write(str(tournament_size))
    log.write("\n")
    log.write("Parsimony Pressure Coefficient (p):  ")
    log.write(str(parsimony_pressure))
    log.write("\n")
    log.write("Termination Type:  ")
    log.write(str(termination))
    log.write("\n")
    log.write("Termination Criterion (n):  ")
    log.write(str(termination_criterion))
    log.write("\n")

    log.write("Sequence Length (l):  ")
    log.write(str(length_iterations))
    log.write("\n")
    log.write("Max Agent Memory Length:  ")
    log.write(str(max_memory_length))
    log.write("\n")
    log.write("Max Tree Depth (d):  ")
    log.write(str(tree_depth))
    log.write("\n")
    log.write("Seed Value:  ")
    log.write(str(seed))
    log.write("\n")
    log.write("Number of evaluations:   ")
    log.write(str(max_evals))
    log.write("\n")
    log.write("Number of Runs:  ")
    log.write(str(runs))
    log.write("\n\n")

def NewLogRun(runCounter):
    log.write("\n")
    log.write("Run ")
    log.write(str(runCounter))
    log.write("\n")

def LogEntry(evals, avg_fitness, best_fitness):
    log.write(str(evals))
    log.write("\t")
    log.write(str(avg_fitness))
    log.write("\t")
    log.write(str(best_fitness))
    log.write("\n")

def Absolute_Log_Entry(fitness):
    log.write("\nAbsolute Fitness\n")
    log.write(str(fitness))
    log.write("\n")

def CloseLog():
    log.close()
