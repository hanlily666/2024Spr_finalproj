"""
Author: Ruixin Han
Title: The final project for 2024 Spring IS 597
Content: This program aims to design and implement a variation on the 51 area puzzle. The inspiration is from
https://krazydad.com/area51/
Design: I would get rid of the uncircled numbers but add the Air Force
protection around fences. Air Force security humans always patrol along the (inside of) the fence line. (meaning the
fence must be adjacent to every human on at least one side)
Cactus, 'C': it can only be outside of the fences
Alien, 'A': it can only be inside of the fences
Circled number: since in this variation there is no uncircled clue, all numbers mean the circled clue
                  It means are always inside the fence; they indicate visibility conditions.
                  This number counts the total squares visible looking north, south, east, and west from the coded location,
                  and includes the code square itself.
Human, 'H': """
import itertools
from collections import Counter
from copy import deepcopy
from typing import Union

import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations


class Clues:
    clue_position = {}
    clues = {}
    aliens = []
    cactus = []
    guard = []
    circled_number = []

    def __init__(self, position, clue_type, puzzle_size):
        self.position = position
        self.row = position[0]
        self.col = position[1]
        self.clue = clue_type
        self.color = None
        self.upper_cell = ()
        self.lower_cell = ()
        self.left_cell = ()
        self.right_cell = ()
        self.upper_edge = ((self.row, self.col), (self.row, self.col+1))
        self.lower_edge = ((self.row+1, self.col+1), (self.row+1, self.col))
        self.left_edge = ((self.row, self.col), (self.row+1, self.col))
        self.right_edge = ((self.row, self.col+1), (self.row+1, self.col+1))
        # all nodes surrounded the cell; same for the surrounded edges
        self.neighbor_nodes = [(self.row, self.col), (self.row, self.col + 1), (self.row + 1, self.col),
                               (self.row + 1, self.col + 1)]
        self.surrounded_edges = [((self.row, self.col), (self.row, self.col + 1)), ((self.row, self.col),
                                                                                    (self.row + 1, self.col)),
                                 ((self.row + 1, self.col + 1), (self.row + 1, self.col)),
                                 ((self.row, self.col + 1), (self.row + 1, self.col + 1))]

        if self.row > 0:
            self.upper_cell = (self.row - 1, self.col)

        if self.row + 1 < puzzle_size[0]:
            self.lower_cell = (self.row + 1, self.col)

        if self.col + 1 < puzzle_size[1]:
            self.right_cell = (self.row, self.col + 1)

        if self.col - 1 > 0:
            self.left_cell = (self.row, self.col - 1)

        if clue_type not in Clues.clues:
            Clues.clues[clue_type] = 1
        else:
            Clues.clues[clue_type] += 1

        if clue_type == 'A':
            Clues.aliens.append(self)
        elif clue_type == 'C':
            Clues.cactus.append(self)
        elif clue_type == 'G':
            Clues.guard.append(self)
        elif isinstance(clue_type, int):
            Clues.circled_number.append(self)

        if position not in Clues.clue_position:
            Clues.clue_position[position] = self

    def __str__(self):
        return f'Clue type is {self.clue}.'

    def is_on_the_upper_left(self, other):
        return self.col < other.col and self.row > other.row

    def is_on_the_left(self, other):
        return self.col < other.col

    def is_on_the_right(self, other):
        return self.col > other.col

    def is_below(self, other):
        return self.row > other.row and self.col == other.col

    def is_above(self, other):
        return self.row < other.row and self.col == other.col

    def direction_to(self, other):
        if self.col < other.col:
            horizontal = 'left'
        elif self.col > other.col:
            horizontal = 'right'
        else:
            horizontal = 'same column'

        # Determine vertical relation
        if self.row < other.row:
            vertical = 'above'
        elif self.row > other.row:
            vertical = 'below'
        else:
            vertical = 'same row'

        # Combine into a single descriptor, ignoring 'same row/column' when in line
        if horizontal == 'same column' and vertical != 'same row':
            return vertical
        elif vertical == 'same row' and horizontal != 'same column':
            return horizontal
        elif horizontal == 'same column' and vertical == 'same row':
            return 'same position'
        else:
            return f"{vertical} and {horizontal}"

    def add_clue_color(self, color):
        self.color = color


    # start with the alien node; check their relative location to other clue; make deduction first
    # connect all edges that attributes are not 2
    # if met a node that has three edges, then go back and mark that one as 2
    # keep track of all the nodes starting with the alien
    # in the end it should form a loop that encounters the original node again





    # find if there are any walls at the same row or col of the circled number
    # if :

    # relationship = nx.get_edge_attributes(G, "relationship")
    # for edges, value in relationship.items():
    #     if value == 1:
    #         # edges = edges.split(',')
    #         count_edges.append(edges)
    # node_with_corner = [node for node, count in Counter(count_edges).items() if count >= 1]
    # print(node_with_corner)

        # compare the position of two edges



# def solve_puzzle(a_puzzle):
#     row_of_puzzle = len(a_puzzle) + 1  # the actual grid includes all the dots surrounded by the clues
#     col_of_puzzle = len(a_puzzle[0]) + 1
#     for row in range(row_of_puzzle):
#         for col in range(col_of_puzzle):
#             if 'clue' in G.nodes[(row, col)]:
#                 the_clue = G.nodes[(row, col)]['clue']
#                 if isinstance(the_clue, int):  # if it is circled number
#                     solve_circled_clue(a_puzzle, (row, col), the_clue)
                    # break


# def solve_circled_clue(a_puzzle, position_of_circled_clue, clue_number):
#     # offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
#     all_squares_clue_can_see = []
#     row_of_puzzle = len(a_puzzle)
#     col_of_puzzle = len(a_puzzle[0])
#     row_of_clue = position_of_circled_clue[0]
#     col_of_clue = position_of_circled_clue[1]  # the col of the clue in the original puzzle
#     one_direction_square = 0
#     if clue_number <= row_of_puzzle and exists_cacutus(position_of_circled_clue):
#
#
#     for i in range(row_of_puzzle):
#         all_squares_clue_can_see.append((i, col_of_puzzle))
#     while visible_fences <= clue_number:
#         # for square in all_squares_clue_can_see:
#         for offset in offsets:
#             # start with the clue square
#
#             if 'clue' in G.nodes[(row_of_puzzle, col_of_puzzle)]:
#                 this_clue = G.nodes[(row_of_puzzle, col_of_puzzle)]['clue']
#                 if this_clue == 'C' and offset == (0, 1):  # TODO: what if the other two offsets?
#                     continue
#             neighbor_row = row_of_clue + offset[0]
#             neighbor_col = col_of_clue + offset[1]
#             if 0 <= neighbor_row < row_of_puzzle and 0 <= neighbor_col < col_of_puzzle:
#                 print(neighbor_row, neighbor_col)
#
#                 if not G.has_edge((row_of_clue, col_of_clue), (neighbor_row, neighbor_col)):
#                     G.add_edge((row_of_clue, col_of_clue), (neighbor_row, neighbor_col))
#                 # TODO: avoid crossing itself (forming a loop without considering all the other clues)
#                 # row = neighbor_row
#                 # col = neighbor_col
#                 print(G.edges((row_of_clue, col_of_clue)))
#
#                 visible_fences += 1
#                 if len(G.edges((row_of_clue, col_of_clue))) == 2:
#                     row_of_clue = neighbor_row
#                     col_of_clue = neighbor_col


class StackDictionary(dict):
    """Subclass a standard dictionary and add convenience methods to make it
        easier to use simultaneously as a stack of key/value pairs.

        Since Python 3.6+ the insertion order of dict keys is retained internally.
        There is a popitem() method which returns and removes the last-added item
        (a key/value pair).

        However, there isn't a convenient way to non-destructively VIEW the top
        item and keep it on the stack. In this program that feature is desirable."""

    def peek(self) -> Union[tuple, None]:
        """Allows getting the top item of the StackDictionary while leaving it
        there. This is implemented by actually using popitem() but then
        adding it back in automatically.
        :returns: None if empty dict. Otherwise, the top item.
        >>> stack_dict = StackDictionary({(0, 1): {'horiz': False, 'cells': ((0,0), (1,0))},
        ...                               (0, 0): {'horiz': True,  'cells': ((0,1), (0,2))}})
        >>> stack_dict.peek()
        ((0, 0), {'horiz': True, 'cells': ((0, 1), (0, 2))})
        >>> empty_dict = StackDictionary({})
        >>> empty_dict.peek()
        >>> print(empty_dict.peek())
        None
        """
        top_item = self.popitem()  # get last-added item.
        if top_item is None:
            return None
        self[top_item[0]] = top_item[1]  # Re-insert the key & value into the dict.
        return top_item

    def peek_last_two(self):
        if len(self) < 2:
            return None
        keys = list(self.keys())
        second_last_key = keys[-2]
        return second_last_key, self[second_last_key]


    def popitem(self) -> Union[tuple, None]:
            """Wraps the dict superclass implementation of popitem() so this will
            return None when empty instead of throwing an exception.
            >>> stack_dict = StackDictionary({(0, 1): {'horiz': False, 'cells': ((0,0), (1,0))},
            ...                               (0, 0): {'horiz': True,  'cells': ((0,1), (0,2))}})
            >>> stack_dict.popitem()
            ((0, 0), {'horiz': True, 'cells': ((0, 1), (0, 2))})

            >>> empty_dict = StackDictionary({})
            >>> empty_dict.popitem()
            >>> print(empty_dict.popitem())
            None
            """
            try:
                result = super().popitem()
                return result
            except KeyError:
                return None


class Solver:
    def __init__(self, the_puzzle):
        self.solutions_found = []  # if multiple solutions, this would be nested list
        self.clues_in_solution = {}
        self.traversed_nodes = StackDictionary()
        self.visited_node = []
        self.clues = Clues.clues
        self.starting_puzzle = the_puzzle
        self.loop_detection = False
        self.starting_graph = nx.Graph()
        self.visited_edge = []

    def create_graph(self):
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        row_of_puzzle = len(self.starting_puzzle) + 1
        col_of_puzzle = len(self.starting_puzzle[0]) + 1
        puzzle_size = (row_of_puzzle, col_of_puzzle)
        for row in range(row_of_puzzle):
            for col in range(col_of_puzzle):
                self.starting_graph.add_node((row, col), clue=None)
                if row < len(self.starting_puzzle) and col < len(self.starting_puzzle[0]):
                    the_clue = self.starting_puzzle[row][col]
                    # if the_clue:
                    # node = Nodes((row, col), the_clue)  # TODO: do i need class to record the the_clue info? keep
                    #  in mind that it needs to be hashable
                    self.starting_graph.add_node((row, col), clue=the_clue)
                    this_clue = Clues((row, col), the_clue, puzzle_size)
                for offset in offsets:
                    neighbor_row = row + offset[0]
                    neighbor_col = col + offset[1]
                    if 0 <= neighbor_row < row_of_puzzle and 0 <= neighbor_col < col_of_puzzle:
                        self.starting_graph.add_edge((row, col), (neighbor_row, neighbor_col), relationship=0)

    def is_valid_connection(self, node, neighbor) -> bool:
        """
        check whether this connection violates any rule.
        :param node1: The node before being added to the traversed edges (stack dictionary)
        :param node2: The node before being added to the traversed edges (stack dictionary)

        :return: boolean
        """
        # check whether alien has any edge and what the color of edge's other side is.
        # the same for the other clues
        for alien in Clues.aliens:
            if alien.color == 'Blue':
                return False

        for cactus in Clues.cactus:
            if cactus.color == 'Green':
                return False

        for guard in Clues.guard:
            if guard.color == 'Blue':
                return False

        return True

        # last_move = self.traversed_nodes.peek()[1]['move']
        # last_node = self.traversed_nodes.peek()[0]
        # for move in last_move:
        #     if move[-1] == 1:
        #         the_last_edge = move[0]
        #         break
        # if node in Clues.clue_position:
        #     clue_object = Clues.clue_position[node]
        #     the_clue_type = Clues.clue_position[node].clue
        #     current_edge = tuple(sorted((node, neighbor)))
        #     if the_clue_type == 'A':
        #         if last_node[0] < node[0]:
        #             if current_edge == clue_object.upper_edge:
        #                 return False
        #         if last_node[1] == node[1]:
        #             if current_edge == clue_object.left_edge:
        #                 return False


    def is_valid_solution(self) -> bool:
        # if self.loop_detection:
        #     for clue in self.clues:
        #         if clue != 'C':
        #             if self.clues_in_solution[clue] != self.clues[clue]:
        #                 return False
        # return True
        return False

    def provide_clues_hints(self):
        count_edges = []
        aliens = Clues.aliens
        cactus = Clues.cactus
        guard = Clues.guard
        circled_number = Clues.circled_number
        direction = None
        # have all combinations of clues, and draw as many clues as possibles
        for pair in self.all_possible_combination_of_clues(aliens, guard):
            if Clues.direction_to(pair[0], pair[1]) == 'left':
                self.starting_graph.add_edge((pair[0].row, pair[0].col + 1), (pair[0].row + 1, pair[0].col + 1), relationship=1)
                self.starting_graph.add_edge((pair[1].row, pair[1].col), (pair[1].row + 1, pair[1].col), relationship=1)
                self.solutions_found.append(tuple(sorted(((pair[0].row, pair[0].col + 1), (pair[0].row + 1, pair[0].col + 1)))))
                self.solutions_found.append(tuple(sorted(((pair[0].row, pair[0].col), (pair[0].row + 1, pair[0].col)))))

                direction = 'right'
        for pair in self.all_possible_combination_of_clues(aliens, cactus):
            if Clues.direction_to(pair[0], pair[1]) == 'above' and pair[1].row == pair[0].row + 1:
                self.starting_graph.add_edge((pair[0].row + 1, pair[0].col), (pair[0].row + 1, pair[0].col + 1), relationship=1)
                self.starting_graph.add_edge((pair[1].row, pair[1].col), (pair[1].row, pair[1].col + 1), relationship=1)
                self.solutions_found.append(
                    tuple(sorted(((pair[0].row + 1, pair[0].col), (pair[0].row + 1, pair[0].col + 1)))))
                self.solutions_found.append(tuple(sorted(((pair[1].row, pair[1].col), (pair[1].row, pair[1].col + 1)))))
                alien_edges = self.check_clue_status((pair[0].row, pair[0].col), self.starting_graph)
                self.cross_out_cactus_other_edges(pair[1], edge_direction='up')
                if alien_edges >= 2 and direction == 'right' and \
                        self.starting_graph.get_edge_data(aliens[0].right_edge[0], aliens[0].right_edge[1])['relationship'] == 1:
                    self.starting_graph.add_edge(aliens[0].left_edge[0], aliens[0].left_edge[1], relationship=1)
                    self.solutions_found.append(
                        tuple(sorted((aliens[0].left_edge[0], aliens[0].left_edge[1]))))

                    direction = 'up'

        if Clues.direction_to(circled_number[0], cactus[0]) == 'above':
            pass

    def check_edge_status(self, node1, node2, current_graph):
        status = current_graph.get_edge_data(node1, node2)['relationship']
        if status == 1:
            return 1
        elif status == 0:
            return 0
        elif status == 'x':
            return 'x'

    def follow_alien_rule(self, node):
        the_clue = Clues.clue_position[node]
        last_edge = None
        # self.check_clue_status(node, self.starting_graph)
        if self.visited_edge:
            for move in self.traversed_nodes.peek_last_two()['move']:
                if move[-1] == 1:
                    last_edge = move[0]  # e.g. ((1, 0), (2, 0))
                    print(f'last edge {last_edge}')
                    break
                else:
                    last_edge = ''
            if the_clue.clue == 'A':
                for edge in the_clue.surrounded_edges:
                    if edge == the_clue.left_edge and self.check_edge_status(edge[0], edge[1], self.starting_graph) == 1:
                        print(f'last edge is {last_edge}')
                        for last_node in last_edge:
                            print(f'last node {last_node}')
                            if last_node != node:
                                if last_node[1] == node[1]:
                                    self.starting_graph.add_edge(the_clue.upper_edge[0], the_clue.upper_edge[1], relationship='x')
                                    print('followed')
                    if edge == the_clue.upper_edge and self.check_edge_status(edge[0], edge[1], self.starting_graph) == 1:
                        for last_node in last_edge:
                            if last_node != node:
                                if last_node[1] == node[1]:
                                    self.starting_graph.add_edge(the_clue.left_edge[0], the_clue.left_edge[1], relationship='x')
                                    if the_clue.upper_edge[1][1] + 1 < len(self.starting_puzzle[0]) + 1:
                                        self.starting_graph.add_edge(the_clue.upper_edge[1][0], the_clue.upper_edge[1][1] + 1, relationship='x')

    def follow_cactus_rule(self, node):
        the_clue = Clues.clue_position[node]
        last_edge = None
        # self.check_clue_status(node, self.starting_graph)
        if self.visited_edge:
            for move in self.traversed_nodes.peek()[1]['move']:
                if move[-1] == 1:
                    last_edge = move[0]  # e.g. ((1, 0), (2, 0))
                    print(f'last edge {last_edge}')
                    break
                else:
                    last_edge = ''
            if the_clue.row == len(self.starting_puzzle) - 1:
                print('yep cross it out')
                self.starting_graph.add_edge(the_clue.left_edge[0], the_clue.left_edge[1], relationship='x')
            # for edge in the_clue.surrounded_edges:
            #     if edge == the_clue.left_edge:
            #         print(f'last edge is {last_edge}')
            #         for last_node in last_edge:
            #             print(f'last node {last_node}')
            #             if last_node != node:
            #                 if last_node[1] == node[1]:
            #                     self.starting_graph.add_edge(the_clue.upper_edge[0], the_clue.upper_edge[1],
            #                                                  relationship='x')
            #                     print('followed')

    def reverse_color_on_other_side(self, node, color):
        reversed_color = None
        if color == 'Green':
            reversed_color = 'Blue'
        elif color == 'Blue':
            reversed_color = 'Green'
        for edge in Clues.clue_position[node].surrounded_edges:
            if self.check_edge_status(edge[0], edge[1], self.starting_graph) == 1:
                if edge == Clues.clue_position[node].upper_edge:
                    upper_cell = Clues.clue_position[node].upper_cell
                    if upper_cell:
                        Clues.clue_position[upper_cell].color = reversed_color
                        # self.traversed_nodes[upper_cell]['color'] =
                elif edge == Clues.clue_position[node].left_edge:
                    left_cell = Clues.clue_position[node].left_cell
                    if left_cell:
                        Clues.clue_position[left_cell].color = reversed_color
                elif edge == Clues.clue_position[node].right_edge:
                    right_cell = Clues.clue_position[node].right_cell
                    if right_cell:
                        Clues.clue_position[right_cell].color = reversed_color
                elif edge == Clues.clue_position[node].lower_edge:
                    lower_cell = Clues.clue_position[node].lower_cell
                    if lower_cell:
                        Clues.clue_position[lower_cell].color = reversed_color

    def add_color(self, node, neighbor):
        if node[0] == 0 or node[0] == len(self.starting_puzzle) or node[0] == 0 or node[0] == len(self.starting_puzzle[0]):
            if neighbor[0] == 0 or neighbor[0] == len(self.starting_puzzle) or neighbor[0] == 0 or neighbor[0] == len(self.starting_puzzle[0]):
                if node in Clues.clue_position:
                    # this color represents the cell's color
                    self.traversed_nodes[node]['color'] = (node, 'Green')
                    Clues.clue_position[node].add_clue_color('Green')
        if node in Clues.clue_position:
            if Clues.clue_position[node].clue == 'A':
                self.clues_in_solution['A'] = [node]
                self.traversed_nodes[node]['color'] = (node, 'Green')
                Clues.clue_position[node].add_clue_color('Green')
                # check if there is edge around the clue cell, if there is, mark the other side cell as Blue
                self.reverse_color_on_other_side(node, 'Green')
            elif Clues.clue_position[node].clue == 'C':
                self.traversed_nodes[node]['color'] = (node, 'Blue')
                Clues.clue_position[node].add_clue_color('Blue')
                self.reverse_color_on_other_side(node, 'Blue')
            elif Clues.clue_position[node].clue == 'G':
                self.clues_in_solution['G'] = [node]
                self.traversed_nodes[node]['color'] = (node, 'Green')
                Clues.clue_position[node].add_clue_color('Green')
                self.reverse_color_on_other_side(node, 'Green')
            elif isinstance(Clues.clue_position[node].clue, int):
                self.clues_in_solution[Clues.clue_position[node].clue] = [node]
                self.traversed_nodes[node]['color'] = (node, 'Green')
                Clues.clue_position[node].add_clue_color('Green')
                self.reverse_color_on_other_side(node, 'Green')
        last_move = self.traversed_nodes.peek_last_two()
        if last_move:
            last_node, move = last_move
            color = None
            if 'color' in move:
                color = move['color'][-1]
            if color:
                if last_node in Clues.clue_position and node in Clues.clue_position:
                    Clues.direction_to(Clues.clue_position[last_node], Clues.clue_position[node])
                    for edge in Clues.clue_position[last_node].surrounded_edges:
                        if edge in Clues.clue_position[last_node].surrounded_edges:
                            if self.check_edge_status(edge[0], edge[1], self.starting_graph) == 'x':
                                self.traversed_nodes[node]['color'] = (node, color)
                                Clues.clue_position[node].add_clue_color(color)

    def check_cell_status(self, the_edge1, the_edge2) -> tuple:
        """
        find the top left corner node position (the cell) given two edges
        :param the_edge1: edge of the graph
        :param the_edge2: edge of the graph
        :return: (row, col) position
        """
        node1, node2 = the_edge1
        node3, node4 = the_edge2
        row = min(node1[0], node2[0], node3[0], node4[0])
        col = min(node1[1], node2[1], node3[1], node4[1])
        return row, col

    def make_connection(self, node, neighbors):
        """
        StackDict (all the valid moves) -> {(row, col): {'neighbor': (), 'move':[]}

        :param node:
        :param neighbors:

        :return:
        """
        # if there is no move yet
        # if 'clue' in self.starting_graph.nodes[node]:
        #     the_clue = self.starting_graph.nodes[node]['clue']
        #     # if self.check_edge_status(node, neighbor, self.starting_graph) == 0:
        if not self.visited_edge:

            self.starting_graph.add_edge(node, neighbors[0], relationship=1)
            print(f'node {node} neighbor {neighbors[0]}')
            print(self.starting_graph[node][neighbors[0]]['relationship'])
            # self.visited_node.append(node)
            # self.visited_node.append(neighbors[0])
            the_edge = tuple(sorted((node, neighbors[0])))
            self.visited_edge.append(the_edge)
            neighbors.remove(neighbors[0])
            self.traversed_nodes[node]['move'].append((the_edge, 1))
            self.add_color(node, neighbors[0])
            if self.check_clue_status(node, self.starting_graph) == 2:
                self.cross_out_edges_if_two_edges(node, self.starting_graph)
            return True
        else:
            # if node[0] < len(self.starting_puzzle) and node[1] < len(self.starting_puzzle[1]):
            #     the_clue = Clues.clue_position[node]
            #     if the_clue.clue == 'C':
            #         self.follow_cactus_rule(node)
            if not neighbors:
                return False
            # elif tuple(sorted((node, neighbors[0]))) in self.visited_edge:
            elif tuple(sorted((node, neighbors[0]))) in self.visited_edge:
                self.loop_detection = True
                print(self.loop_detection)
                # if self.is_valid_solution():
                #     return
                # else:
                return False
            else:
                for neighbor in neighbors:
                    if self.check_edge_status(node, neighbor, self.starting_graph) == 0:
                        # self.is_valid_connection()
                        self.starting_graph.add_edge(node, neighbor, relationship=1)
                        print(f'node {node} neighbor {neighbor}')
                        print(self.starting_graph[node][neighbor]['relationship'])
                        the_edge = tuple(sorted((node, neighbor)))
                        self.visited_edge.append(the_edge)
                        neighbors.remove(neighbor)
                        self.traversed_nodes[node]['move'].append((the_edge, 1))
                        self.add_color(node, neighbor)
                        # self.visited_node.append(node)
                        # self.visited_node.append(neighbors[0])
                        if self.check_clue_status(node, self.starting_graph) == 2:
                            self.cross_out_edges_if_two_edges(node, self.starting_graph)
                        return True
        # try:
        #     if node not in self.visited_node:
        #         status = self.check_edge_status(current_node, node, current_graph)
        #         if status == 1:
        #             neighbors = current_graph.edges(node)
        #             valid_neighbors = self.are_valid_neighbors(node, neighbors, current_graph)
        #             self.traversed_nodes[(current_node, node, current_graph)] = {'neighbor': valid_neighbors,'state': current_graph}
        #         elif status == 0:
        #             current_graph.add_edge(current_node, node, relationship=1)
        #             if self.is_valid_connection(current_graph)


    def next_valid_node(self):
        current_state = self.traversed_nodes.peek()
        if not current_state:
            return 0, 0
        else:
            current_node = self.traversed_nodes.peek()[0]
            if current_state[1]['move']:
                moves = current_state[1]['move']
                if moves:
                    for move in moves:
                        if move[-1] == 1:
                            for next_node in move[0]:
                                if next_node != current_node:
                                    return next_node

    def find_valid_neighbors(self, node):
        valid_neighbors = []
        neighbors = list(self.starting_graph.neighbors(node))
        # if not neighbors:
        #
        potential_next_node = True
        print(list(self.starting_graph.neighbors(node)))
        # if node[0] < len(self.starting_puzzle) and node[1] < len(self.starting_puzzle[1]):
        #     the_clue = Clues.clue_position[node]
        #     if the_clue.clue == 'A':
                # self.follow_alien_rule(node)
        for neighbor in neighbors:
            status = self.check_edge_status(neighbor, node, self.starting_graph)
            if status == 1 and tuple(sorted((neighbor, node))) in self.solutions_found:
                potential_next_node = False
            if status != 'x' and status != 1:
                valid_neighbors.append(neighbor)
        return potential_next_node, valid_neighbors

    def brute_force_solver(self):
        self.create_graph()
        # self.provide_clues_hints()
        # starting from one alien to traverse the puzzle
        # valid_neighbors = self.are_valid_neighbors((aliens[0].row, aliens[0].col), neighbors, self.starting_graph)

        while self.is_valid_solution() is False:
            try:
                next_node = self.next_valid_node()
                next_round, neighbors = self.find_valid_neighbors(next_node)
                self.traversed_nodes[next_node] = {'neighbors': neighbors, 'move': [], 'color': None}
                connecting_edge = self.make_connection(next_node, neighbors)
                # if next_node[0] < len(self.starting_puzzle) and next_node[1] < len(self.starting_puzzle[1]):
                #     the_clue = Clues.clue_position[next_node]
                #     if the_clue.clue == 'A':
                #         self.follow_alien_rule(next_node)
                successful_edge = self.is_valid_connection(next_round, neighbors)
                if not successful_edge:
                    if self.loop_detection:
                        self.is_valid_solution()
                        if not self.is_valid_solution():
                            self.backtrack()
                    else:
                        self.backtrack()
                print(self.traversed_nodes)

                self.draw_graph(self.starting_graph)

            except ValueError as ex:
                if ex.args[0] == 'Backtracked all the way to beginning. No more solutions.':
                    return
                else:
                    raise ex

    def remake_connection(self, node, previous_move, neighbors):
        neighbors.remove(neighbors[0])
        if node not in self.traversed_nodes:
            self.traversed_nodes[node] = {'neighbors': neighbors, 'move': []}
        for the_tuple in previous_move:
            if the_tuple[-1] == 1:
                self.starting_graph.add_edge(the_tuple[0][0], the_tuple[0][1], relationship='x')
                self.traversed_nodes[node]['move'].append((tuple(sorted((the_tuple[0][0], the_tuple[0][1]))), 'x'))
                self.add_color(node, neighbors[0])
                self.visited_node.append(the_tuple[0][0])
                self.visited_node.append(the_tuple[0][1])
            elif the_tuple[-1] == 'x':
                self.starting_graph.add_edge(the_tuple[0][0], the_tuple[0][1], relationship=1)
                self.traversed_nodes[node]['move'].append((tuple(sorted((the_tuple[0][0], the_tuple[0][1]))), 1))
                self.visited_node.append(the_tuple[0][0])
                self.visited_node.append(the_tuple[0][1])
        return True

    def backtrack(self):
        while True:
            last_move = self.traversed_nodes.popitem()
            # if there is a loop but not a solution
            if self.loop_detection:
                last_last_move = self.traversed_nodes.popitem()

            if last_move is None:
                raise ValueError('Backtracked all the way to beginning. No more solutions.')
            if last_move[1]['neighbors']:
                neighbors = last_move[1]['neighbors']

                previous_moves = last_move[1]['move']
                if previous_moves:
                    successful = self.remake_connection(last_move[0], previous_moves, neighbors)
                    if successful:
                        return
                    else:
                        self.backtrack()
                else:
                    self.backtrack()


            else:
                self.backtrack()



    def get_clue_hint(self):
        pass

    def all_possible_combination_of_clues(self, clue1, clue2):
        if len(clue1) > 1 or len(clue2) > 1:
            possible_combinations_between_alien_cactus = list(itertools.product(clue1, clue2))
        else:
            possible_combinations_between_alien_cactus = [(clue1[0], clue2[0])]  # only one for each clue
        return possible_combinations_between_alien_cactus

    def cross_out_cactus_other_edges(self, clue_position, edge_direction=None):
        if edge_direction == 'up':
            self.starting_graph.add_edge(clue_position.right_edge[0], clue_position.right_edge[1], relationship='x')
            self.starting_graph.add_edge(clue_position.lower_edge[0], clue_position.lower_edge[1], relationship='x')
            self.starting_graph.add_edge(clue_position.left_edge[0], clue_position.left_edge[1], relationship='x')

    def check_clue_status(self, clue_position, graph):
        number_of_edges_connected = 0
        if clue_position[0] > 2 or clue_position[1] > 2:
            pass
        else:
            # clue = Clues.clue_position[clue_position]
            # the_clue = Clues(clue_position, clue, self.starting_puzzle)
            for edge in graph.edges((clue_position[0], clue_position[1])):
                if graph.get_edge_data(edge[0], edge[1])["relationship"] == 1:
                    number_of_edges_connected += 1
            # if one node has two edges connected already, then cross out the other two edges that connect to the node
            self.cross_out_edges_if_two_edges(clue_position, graph)

            return number_of_edges_connected

    def cross_out_edges_if_two_edges(self, node_position, graph_state):
        potential_node_to_cross_out = []
        # for node in Clues.clue_position[node_position].neighbor_nodes:
        number_of_confirmed_relationship = 0
        for edge in graph_state.edges(node_position, data=True):
            if edge[-1]['relationship'] == 1:
                number_of_confirmed_relationship += 1
            else:
                potential_node_to_cross_out.append(edge)

        if number_of_confirmed_relationship == 2:
            for edge in potential_node_to_cross_out:
                if edge[-1]['relationship'] == 0:
                    graph_state.add_edge(edge[0], edge[1], relationship='x')
                    self.traversed_nodes[node_position]['move'].append((tuple(sorted((edge[0], edge[1]))), 'x'))
        self.draw_graph(self.starting_graph)

    def draw_graph(self, graph_state):
        # max_y = max(y for _, y in graph_state.nodes())
        #
        # # Invert the y-coordinate of each node.
        # pos = {node: (x, max_y - y) for node, (x, y) in graph_state.nodes(data='pos')}

        pos = {node: node for node in graph_state.nodes()}

        # pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(graph_state, pos, node_size=700)

        node_labels = nx.get_node_attributes(graph_state, 'clue')
        nx.draw_networkx_labels(graph_state, pos, labels=node_labels)
        clue_labels = nx.get_edge_attributes(graph_state, 'relationship')
        nx.draw_networkx_edge_labels(graph_state, pos, edge_labels=clue_labels)
        nx.draw_networkx_edges(graph_state, pos)

        plt.savefig("graph.png")


def generate_puzzle():
    pass


def is_valid_puzzle():
    pass



if __name__ == '__main__':
    valid_puzzle = [[None, None, None],
                    ['A', None, 'G'],
                    ['C', None, 3]]
    solve_puzzle = Solver(valid_puzzle)
    solve_puzzle.brute_force_solver()

