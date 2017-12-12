# Logan Nielsen
# Assignment 2, CS5401

# AGENT CLASSES

# 0 for Defecting (betray) against the opponent
# 1 for Cooperating (stay silent) with the opponent
import random
import variates
from copy import deepcopy


class TFT_Agent(): #tit-for-tat agent starts out cooperating and then uses the last move of its opponent
    def __init__(self):
        self.last_move = None

    def Make_Move(self):
        return self.last_move

    def Add_Memory(self, outcome):
        _, opponent_move = outcome
        self.last_move = opponent_move


class Genetic_Agent():
    def __init__(self, max_memory_length, controller, parsimony_pressure, length_iterations, tree_depth):
        self.memory = []
        self.max_memory_length = max_memory_length
        self.controller = controller
        self.parsimony_pressure = parsimony_pressure
        self.length_iterations = length_iterations
        self.max_tree_depth = tree_depth
        self._abs_fitness = None
        self._rel_fitness = None
        self._total_nodes = None

    def Make_Move(self):
        move = self.controller.Evaluate(self.memory)
        return move

    def Add_Memory(self, outcome):
        self.memory.append(outcome)
        if len(self.memory) > self.max_memory_length:
            del self.memory[0]

    def Get_Memory(self):
        return self.memory

    def Create_Random_Memory(self):
        for i in range(self.max_memory_length):
            self.Add_Memory((random.randint(0,1), (random.randint(0,1))))

    def Select_Random_Subtree(self):
        rand_num = random.randint(0, self.total_nodes-1)
        _, rand_node = self.controller.Find_Node(rand_num)
        if rand_node is None:
            print(self.controller, rand_num, self.total_nodes)
        return rand_num, rand_node

    def Insert_Subtree(self, location, new_node):
        if location == 0:
            self.controller = new_node
        else:
            self.controller.Replace_Node(location, new_node)
        self.Trigger_Change()

    def Trigger_Change(self):
        self._abs_fitness = None
        self._total_nodes = None

    def Controller_Depth_Check(self):
        self.controller.Fix_Tree_Depth(1, self.max_tree_depth, self.max_memory_length)

    @property
    def total_nodes(self):
        if self._total_nodes is None:
            self._total_nodes = self.controller.total_nodes
        return self._total_nodes

    @property
    def abs_fitness(self):
        if self._abs_fitness is None:
            tft_agent = TFT_Agent()
            tft_agent.Add_Memory(self.memory[self.max_memory_length - 1])
            counter = 0
            while counter < 2*self.max_memory_length:
                tmp_fitness = TFT_Competition(self, tft_agent, self.length_iterations, self.max_memory_length)
                penalty = tmp_fitness * self.parsimony_pressure/100
                counter += 1
            self._abs_fitness = tmp_fitness - penalty
        return self._abs_fitness


def Create_Rand_Agent(max_memory_length, tree_depth, parsimony_pressure, length_iterations):
    rand_num = random.randint(0,2)
    if rand_num == 0:
        rand_controller = variates.Value.From_Random(max_memory_length)
    elif rand_num == 1:
        rand_controller = variates.Univariate.From_Random(max_memory_length, tree_depth)
    elif rand_num == 2:
        rand_controller = variates.Bivariate.From_Random(max_memory_length, tree_depth)
    else:
        raise ValueError("Invalid random number generation -- Create_Rand_Agent Function")
    rand_agent = Genetic_Agent(max_memory_length, rand_controller, parsimony_pressure, length_iterations, tree_depth)
    rand_agent.Create_Random_Memory()
    return rand_agent


def Create_Full_Agent(max_memory_length, tree_depth, parsimony_pressure, length_iterations):
    rand_num = random.randint(1,2)
    if rand_num == 1:
        rand_controller = variates.Univariate.From_Random(max_memory_length, tree_depth)
    elif rand_num == 2:
        rand_controller = variates.Bivariate.From_Random(max_memory_length, tree_depth)
    else:
        raise ValueError("Invalid random number generation -- Create_Rand_Agent Function")
    rand_agent = Genetic_Agent(max_memory_length, rand_controller, parsimony_pressure, length_iterations, tree_depth)
    rand_agent.Create_Random_Memory()
    return rand_agent


def Coevolution(sample_size, population, length_iterations, max_memory_length, parsimony_pressure):
    for agent in population:
        sample_group = set()
        while len(sample_group) != sample_size:
            sample_agent = random.choice(population)
            if sample_agent != agent:
                sample_group.add(sample_agent)
        total_score = 0
        for sa in sample_group:
            total_score += CoE_Competition(agent, sa, length_iterations, max_memory_length)
        agent._rel_fitness = (total_score / sample_size) * ( (100 - parsimony_pressure) / 100)


def CoE_Competition(agent, sample_agent, length_iterations, max_memory_length):
    payoff_total = 0
    for i in range(length_iterations):
        agent_move = agent.Make_Move()
        sample_agent_move = sample_agent.Make_Move()
        agent.Add_Memory((agent_move, sample_agent_move))
        sample_agent.Add_Memory((sample_agent_move, agent_move))
        if i >= 2 * max_memory_length:
            payoff_total += Calculate_Payoff(agent_move, sample_agent_move)
    return (payoff_total/length_iterations)


def TFT_Competition(rand_genetic_agent, tft_agent, length_iterations, max_memory_length):
    payoff_total = 0
    for i in range(length_iterations):
        rand_move = rand_genetic_agent.Make_Move()
        tft_move = tft_agent.Make_Move()
        tft_agent.Add_Memory((tft_move, rand_move))
        rand_genetic_agent.Add_Memory((rand_move, tft_move))
        if i >= 2 * max_memory_length:
            payoff_total += Calculate_Payoff(rand_move, tft_move)
    return (payoff_total/length_iterations)


def Calculate_Payoff(move1, move2):
    if move1 == 1 and move2 == 1:
        payoff = 3
    elif move1 == 1 and move2 == 0:
        payoff = 0
    elif move1 == 0 and move2 == 1:
        payoff = 5
    elif move1 == 0 and move2 == 0:
        payoff = 1
    else:
        print("move1: ",move1, "    move2: ", move2)
        raise ValueError("Invalid Competition Parameters -- Calculate_Payoff Function")
    return payoff
