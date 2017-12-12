# Logan Nielsen
# Assignment 2, CS5401

# TREE CLASS

import random

class Bivariate:
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    def Evaluate(self, memory):
        l_val = self.left_node.Evaluate(memory)
        r_val = self.right_node.Evaluate(memory)
        return self.__class__.function(l_val, r_val)

    @classmethod # generates a bivariate function non-termainal
    def From_Random(cls, max_memory_length, tree_depth): #send tree-depth - 1 on future calls to From Random
        if tree_depth == 1:
            left_node = Value.From_Random(max_memory_length)
            right_node = Value.From_Random(max_memory_length)

        elif tree_depth > 1:
            rand_left = random.randint(0,2)
            rand_right = random.randint(0,2)

            if rand_left == 0:
                left_node = Value.From_Random(max_memory_length)
            elif rand_left == 1:
                left_node = Univariate.From_Random(max_memory_length, tree_depth - 1)
            elif rand_left == 2:
                left_node = Bivariate.From_Random(max_memory_length, tree_depth - 1)
            else:
                raise ValueError("Invalid random node creation")

            if rand_right == 0:
                right_node = Value.From_Random(max_memory_length)
            elif rand_right == 1:
                right_node = Univariate.From_Random(max_memory_length, tree_depth - 1)
            elif rand_right == 2:
                right_node = Bivariate.From_Random(max_memory_length, tree_depth - 1)
            else:
                raise ValueError("Invalid random node creation - Bivariate Class")

        else:
            raise ValueError("Invalid tree depth in Random tree creation - Bivariate Class")

        sub_cls = random.choice([OR_function, AND_function, XOR_function])
        return sub_cls(left_node, right_node)


    @classmethod # generates a bivariate function non-termainal
    def From_Full(cls, max_memory_length, tree_depth): #send tree-depth - 1 on future calls to From Random
        if tree_depth == 1:
            left_node = Value.From_Random(max_memory_length)
            right_node = Value.From_Random(max_memory_length)

        elif tree_depth > 1:
            rand_left = random.randint(1,2)
            rand_right = random.randint(1,2)

            if rand_left == 1:
                left_node = Univariate.From_Random(max_memory_length, tree_depth - 1)
            elif rand_left == 2:
                left_node = Bivariate.From_Random(max_memory_length, tree_depth - 1)
            else:
                raise ValueError("Invalid random node creation")

            if rand_right == 1:
                right_node = Univariate.From_Random(max_memory_length, tree_depth - 1)
            elif rand_right == 2:
                right_node = Bivariate.From_Random(max_memory_length, tree_depth - 1)
            else:
                raise ValueError("Invalid random node creation - Bivariate Class")

        else:
            raise ValueError("Invalid tree depth in Random tree creation - Bivariate Class")

        sub_cls = random.choice([OR_function, AND_function, XOR_function])
        return sub_cls(left_node, right_node)


    def Find_Node(self, num):
        if num == 0:
            return 0, self
        else:
            num, rand_node = self.left_node.Find_Node(num-1)
            if num == 0:
                return num, rand_node
            num, rand_node = self.right_node.Find_Node(num-1)
            return num, rand_node


    def Replace_Node(self, location, new_node):
        if location == 1:
            self.left_node = new_node
            return 0, self
        else:
            location, tmp_node = self.left_node.Replace_Node(location-1, new_node)
            if location == 1:
                self.right_node = new_node
                return 0, tmp_node
            location, tmp_node = self.right_node.Replace_Node(location-1, new_node)
            return location, tmp_node

    def Fix_Tree_Depth(self, current_tree_depth, max_tree_depth, max_memory_length):
        if current_tree_depth == max_tree_depth - 1:
            if not isinstance(self.left_node, Value):
                self.left_node = Value.From_Random(max_memory_length)
            if not isinstance(self.right_node, Value):
                self.right_node = Value.From_Random(max_memory_length)
        else:
            self.left_node.Fix_Tree_Depth(current_tree_depth + 1, max_tree_depth, max_memory_length)
            self.left_node.Fix_Tree_Depth(current_tree_depth + 1, max_tree_depth, max_memory_length)

    def __repr__(self):
        return '{} {} {}'.format(self.name, self.left_node, self.right_node)

    @property
    def total_nodes(self):
        return 1 + self.left_node.total_nodes + self.right_node.total_nodes


class OR_function(Bivariate):
    function = lambda l_node, r_node: l_node or r_node
    name = 'OR'

class AND_function(Bivariate):
    function = lambda l_node, r_node: l_node and r_node
    name = 'AND'

class XOR_function(Bivariate):
    function = lambda l_node, r_node: l_node ^ r_node
    name = 'XOR'


class Univariate():
    name = 'NOT'

    def __init__(self, node):
        self.node = node

    def Evaluate(self, memory):
        return not self.node.Evaluate(memory)

    @classmethod  # generates a NOT function non-terminal
    def From_Random(cls, max_memory_length, tree_depth): #send tree-depth - 1 on future calls to From Random
        if tree_depth == 1:
            return cls(Value.From_Random(max_memory_length))
        elif tree_depth > 1:
            rand_num = random.randint(0,2)
            if rand_num == 0:
                return cls(Value.From_Random(max_memory_length))
            elif rand_num == 1:
                return cls(Univariate.From_Random(max_memory_length, tree_depth - 1))
            elif rand_num == 2:
                return cls(Bivariate.From_Random(max_memory_length, tree_depth - 1))
            else:
                raise ValueError("Invalid Random Node Creation - Univariate Class")
        else:
            raise ValueError("Invalid tree depth in Random tree creation - Univariate Class")

    def From_Full(cls, max_memory_length, tree_depth):
        if tree_depth == 1:
            return cls(Value.From_Random(max_memory_length))
        elif tree_depth > 1:
            rand_num = random.randint(1,2)
            if rand_num == 1:
                return cls(Univariate.From_Random(max_memory_length, tree_depth - 1))
            elif rand_num == 2:
                return cls(Bivariate.From_Random(max_memory_length, tree_depth - 1))
            else:
                raise ValueError("Invalid Random Node Creation - Univariate Class")
        else:
            raise ValueError("Invalid tree depth in Random tree creation - Univariate Class")

    def Find_Node(self, num):
        if num == 0:
            return 0, self
        else:
            num, rand_node = self.node.Find_Node(num-1)
            return num, rand_node

    def Replace_Node(self, location, new_node):
        if location == 1:
            self.node = new_node
            return 0, self
        else:
            location, tmp_node = self.node.Replace_Node(location-1, new_node)
            return location, tmp_node

    def Fix_Tree_Depth(self, current_tree_depth, max_tree_depth, max_memory_length):
        if current_tree_depth == max_tree_depth - 1:
            if not isinstance(self.node, Value):
                self.node = Value.From_Random(max_memory_length)
        else:
            self.node.Fix_Tree_Depth(current_tree_depth + 1, max_tree_depth, max_memory_length)

    def __repr__(self):
        return '{} {}'.format(self.name, self.node)

    @property
    def total_nodes(self):
        return 1 + self.node.total_nodes

class Value():
    def __init__(self, player, index):
        self.player = player
        self.index = index

    @property
    def name(self):
        return 'PO'[self.player] + str(self.index + 1)

    def Evaluate(self, memory):
        return memory[self.index][self.player]

    @classmethod  # randomly generates a terminal
    def From_Random(cls, max_memory_length):
        return cls(random.randint(0, 1), random.randint(0, max_memory_length-1))

    def Find_Node(self, num):
        if num == 0:
            return num, self
        else:
            return num, None

    def Replace_Node(self, location, new_node):
        return location, None

    def Fix_Tree_Depth(self, current_tree_depth, max_tree_depth, max_memory_length):
        pass

    def __repr__(self):
        return self.name

    @property
    def total_nodes(self):
        return 1
