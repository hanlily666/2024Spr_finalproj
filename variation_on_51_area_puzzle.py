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
import networkx as nx

G = nx.Graph()


class Nodes:
    def __init__(self, position, clue):
        self.position = position
        self.clue = clue
        # self.puzzle = puzzle
        # self.row = len(self.puzzle) + 1  # the actual grid includes all the dots surrounded by the clues
        # self.col = len(self.puzzle[0]) + 1


def create_graph(a_puzzle):
    row_of_puzzle = len(a_puzzle) + 1
    col_of_puzzle = len(a_puzzle[0]) + 1
    for row in range(row_of_puzzle):
        for col in range(col_of_puzzle):
            G.add_node((row, col))
            if row < len(a_puzzle) and col < len(a_puzzle[0]):
                the_clue = a_puzzle[row][col]
                if the_clue:
                    # node = Nodes((row, col), the_clue)  # TODO: do i need class to record the the_clue info? keep
                    #  in mind that it needs to be hashable
                    G.add_node((row, col), clue=the_clue)
    print(G.nodes)


def solve_puzzle(a_puzzle):
    row_of_puzzle = len(a_puzzle) + 1  # the actual grid includes all the dots surrounded by the clues
    col_of_puzzle = len(a_puzzle[0]) + 1
    for row in range(row_of_puzzle):
        for col in range(col_of_puzzle):
            if 'clue' in G.nodes[(row, col)]:
                the_clue = G.nodes[(row, col)]['clue']
                if isinstance(the_clue, int):  # if it is circled number
                    solve_circled_clue(a_puzzle, (row, col), the_clue)



def solve_circled_clue(a_puzzle, position_of_circled_clue, clue_number):
    # offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    all_squares_clue_can_see = []
    row_of_puzzle = len(a_puzzle)
    col_of_puzzle = position_of_circled_clue[1]
    for i in range(row_of_puzzle):
        all_squares_clue_can_see.append((i, col_of_puzzle))
    print(all_squares_clue_can_see)
    visible_fences = 0
    while visible_fences <= clue_number:
        for square in all_squares_clue_can_see:
            if 'clue' in G.nodes[(row_of_puzzle, col_of_puzzle)]:
                this_clue = G.nodes[(row_of_puzzle, col_of_puzzle)]['clue']
                if this_clue == 'C' and offset == (0, 1):  # TODO: what if the other two offsets?
                    continue
            neighbor_row = row_of_puzzle + offset[0]
            neighbor_col = col_of_puzzle + offset[1]
            if 0 <= neighbor_row < row_of_puzzle and 0 <= neighbor_col < col_of_puzzle:
                print(neighbor_row, neighbor_col)

                if not G.has_edge((row_of_puzzle, col_of_puzzle), (neighbor_row, neighbor_col)):
                    G.add_edge((row_of_puzzle, col_of_puzzle), (neighbor_row, neighbor_col))
                # TODO: avoid crossing itself (forming a loop without considering all the other clues)
                # row = neighbor_row
                # col = neighbor_col

                print(G.edges((row_of_puzzle, col_of_puzzle)))
                visible_fences += 1
                if len(G.edges((row_of_puzzle, col_of_puzzle))) == 2:
                    row_of_puzzle = neighbor_row
                    col_of_puzzle = neighbor_col

        break




def generate_puzzle():
    pass


def is_valid_puzzle():
    pass


if __name__ == '__main__':
    simplest_puzzle = [[5, 'C'],
                       ['A', None]]

    # create_graph(simplest_puzzle)
    # solve_puzzle(simplest_puzzle)
    solve_circled_clue(simplest_puzzle, (0, 0))