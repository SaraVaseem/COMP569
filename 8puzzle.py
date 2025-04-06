# COMP 569 - Artificial Intelligence
# Spring 2025
# Group Programming Assignment 1
# Group 4: Nicholas Rodriguez Weda, Sarah Vaseem, Tanner Good, Moeeza Nazir, Tamim Sweedan, Luis Olmos

import heapq
from collections import deque

# The 8-puzzle game board
class EightPuzzle:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.zero_index = self.board.index(0)
    
    # For ordering states in Priority Queues
    def __lt__(self, other):
        return self.cost < other.cost
    
    # Check if two states are the same
    def __eq__(self, other):
        return self.board == other.board
    
    # Hash for states to be used in sets
    def __hash__(self):
        return hash(tuple(self.board))
    
    # Generates all possible moves from a given state
    def get_moves(self):
        moves = []
        row, col = divmod(self.zero_index, 3)
        directions = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}
        
        # For each direction
        for move, delta in directions.items():
            
            # Move
            new_index = self.zero_index + delta

            # Bounds checking from move
            if 0 <= new_index < 9:
                if (move == "Left" and col == 0) or (move == "Right" and col == 2):
                    continue
                
                # Create a new board with the numbers swapped after the move
                new_board = self.board[:]
                new_board[self.zero_index], new_board[new_index] = new_board[new_index], new_board[self.zero_index]
                
                # Append the new board (state) to list of possible moves
                moves.append(EightPuzzle(new_board, self, move, self.depth + 1))
        return moves
    
    # Heuristic
    def manhattan_distance(self, goal):
        distance = 0
        for i in range(9):
            if self.board[i] != 0:
                goal_index = goal.index(self.board[i])
                gx, gy = divmod(goal_index, 3)
                x, y = divmod(i, 3)
                distance += abs(gx - x) + abs(gy - y)
        return distance
    

##############################################################

# Breadth First Search Implementation
def bfs(start, goal):

    queue = deque([start])
    visited = set()

    while queue: # queue is not empty

        state = queue.popleft() # pop the first state in the queue
        
        if state.board == goal:# yay!
            print("BFS found a solution!")
            return state
        visited.add(tuple(state.board))
        
        for move in state.get_moves(): # explore all moves from state
            if tuple(move.board) not in visited:
                queue.append(move) # add state to queue
    return None

# Depth First Search Implementation
def dfs(start, goal, depth_limit=float("inf"), announce=True):
    
    stack = [(start, 0)]
    visited = set()
    
    while stack: # stack is not empty
        
        state, depth = stack.pop() # pop the last state in the stack
        
        if state.board == goal: # yay!
            if announce:
                print("DFS found a solution!")
            return state
        
        if depth < depth_limit: # consider depth if calling from IDDFS
            visited.add(tuple(state.board))
            
            for move in reversed(state.get_moves()): # explore all moves from state
                if tuple(move.board) not in visited:
                    stack.append((move, depth + 1)) # push new state to stack
    return None


# IDDFS Implementation
def iterative_deepening(start, goal):
    depth = 0
    while True:
        result = dfs(start, goal, depth, announce=False) # Depth Limited DFS 
        
        if result: # yay!
            print("Iterative Deepening found a solution!")
            return result
        
        depth += 1 # no result -> increase depth, run again with larger depth

# A* Implementation - Heuristic
def astar(start, goal):
    
    open_set = [] # Priority Queue
    heapq.heappush(open_set, (start.manhattan_distance(goal) + start.depth, start))  # start node is f = g (depth) + h (distance)
    visited = set()

    while open_set:
        
        _, state = heapq.heappop(open_set) # get the state with the cheapest f cost
        
        if state.board == goal: # yay!
            print("A* found a solution!")
            return state
        visited.add(tuple(state.board))

        for move in state.get_moves(): # Explore all moves
            if tuple(move.board) not in visited:
                move.cost = move.depth + move.manhattan_distance(goal) # Heuristic: f = g (depth) + h (distance)
                heapq.heappush(open_set, (move.cost, move)) # add the state to the set
    return None

# GBFS Implementation - Heuristic
def greedy_best_first(start, goal):
    open_set = []
    heapq.heappush(open_set, (start.manhattan_distance(goal), start)) # f(n) = h(n) | (distance)
    visited = set()

    while open_set:
        
        _, state = heapq.heappop(open_set) # get the state with the cheapest f cost
        
        if state.board == goal: # yay!
            print("Greedy Best-First found a solution!")
            return state
        visited.add(tuple(state.board))

        for move in state.get_moves():
            if tuple(move.board) not in visited:
                heapq.heappush(open_set, (move.manhattan_distance(goal), move)) # f(n) = h(n) | (distance)
    return None

##############################################################

# Change for different states
start_state = EightPuzzle([1, 2, 3, 4, 0, 5, 6, 7, 8])
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

print("BFS:")
bfs(start_state, goal_state)

print("\nDFS:")
dfs(start_state, goal_state)


print("\nIterative Deepening:")
iterative_deepening(start_state, goal_state)

print("\nA*:")
astar(start_state, goal_state)

print("\nGreedy Best-First:")
greedy_best_first(start_state, goal_state)