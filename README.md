## Area 51 Variation

This program aims to design and implement a variation on the 51 area puzzle. The inspiration is from
https://krazydad.com/area51/ and Mr. John Weible.

## Design:

I would get rid of the uncircled numbers but add the Air Force
protection around fences. Air Force security humans always patrol along the (inside) the fence line. (meaning the
fence must be adjacent to every human on at least one side)
Cactus, 'C': it can only be outside the fences
Alien, 'A': it can only be inside the fences
Circled number: since in this variation there is no uncircled clue, all numbers mean the circled clue
                  It means are always inside the fence; they indicate visibility conditions.
                  This number counts the total squares visible looking north, south, east, and west from the coded location,
                  and includes the code square itself.

### Data Structure

I use a custom class StackDictionary to record each traversed node, `(0, 0) : {'neighbors': [(0, 1)], 'move': [(((0, 0), (1, 0)), 1)], 'color': None}}` 

### Graph Visualization

![alt text](https://github.com/hanlily666/Area_51_puzzle_variation/blob/main/graph.png)

I have successfully implemented the _alien_ and _cactus_ rule checking with the clue of the cell color, where the puzzle can be partially solved and cross out illegal moves (edges).
However, based on the current implementation result of the puzzle solver function. At the node `(3, 2)` it should have taken the move `((3, 2), (3, 3), 1)`. 
What I don't understand is that PyCharm doesn't allow me to do that. I know it could be a bug in the code, but I have looked into this node several times, and I don't understand why 
it cannot take `(3, 3)` which is `(3, 2)` neighbor after hitting the `continue` of the loop during the `self.make_connection` stage. 

I will keep looking at this problem. Hopefully, I can get the puzzle solver fully work soon.

### Algorithm Analysis 

For the puzzle solver class, if the puzzle size is n meaning n number of nodes in the puzzle, the Big-O is n, and Big-Theta is n, and Big-Omega is n.
Through the profiler output, you can also see that the `brute_force_solver` is called the most of the time. What follows are `draw_graph`, `make_connection` and `cross_out_edges_if_two_edges` 
which does being executed repeatedly while traversing each node.

### Future work

![alt text](https://github.com/hanlily666/Area_51_puzzle_variation/blob/main/sample_puzzle.jpg)

Here is the desired result of the implementation. Using color and 'x' marker as a technique to mark the cells are helpful to imply the moves. 
