import random
import numpy as np
import heapq
import math

#build grid
#grid = [1,2,3,4,5,6,7,8,0] #only needed for random function
#(a,b,c,d,e,f,g,h,i) = grid #unpacking
np_grid = np.array([1,2,3,4,5,6,7,8,0])
solution = np.array([[1,2,3],[4,5,6],[7,8,0]])
random.seed(0)

def randomize_grid():
    global np_grid
    #np_grid = np.random.choice(np_grid, size=9, replace=False)
    random.shuffle(np_grid)
    #np_grid = np.array(grid)
    np_grid = display_grid()
    return np_grid

def display_grid():
    global np_grid
    return np_grid.reshape(3, 3)

def start():
    print(randomize_grid())
    print("\n")

#need to swap space with number
def move_up():
    #add 1 to row
    curr_row = 0
    curr_col = 0
    for col, row in np.ndindex(np_grid.shape):
        if np_grid[row][col] == 0:
            curr_row = row
            curr_col = col
            row_i = row-1
            np_grid[row][col] = np_grid[row_i][col]
    for col, row in np.ndindex(np_grid.shape):
        if row == curr_row-1 and col == curr_col:
            np_grid[row][col] = 0
    print(np_grid)
    print("\n")
    return np_grid

def move_down():
    #subtract 1 from row
    curr_row = 0
    curr_col = 0
    for col, row in np.ndindex(np_grid.shape):
        if np_grid[row][col] == 0:
            curr_row = row
            curr_col = col
            row_i = row+1
            np_grid[row][col] = np_grid[row_i][col]
    for col, row in np.ndindex(np_grid.shape):
        if row == curr_row+1 and col == curr_col:
            np_grid[row][col] = 0
    print(np_grid)
    print("\n")
    return np_grid

def move_left():
    #subtract 1 from col
    curr_row = 0
    curr_col = 0
    for col, row in np.ndindex(np_grid.shape):
        if np_grid[row][col] == 0:
            curr_row = row
            curr_col = col
            col_i = col-1
            np_grid[row][col] = np_grid[row][col_i]
    for col, row in np.ndindex(np_grid.shape):
        if row == curr_row and col == curr_col-1:
            np_grid[row][col] = 0
    print(np_grid)
    print("\n")
    return np_grid

def move_right():
    #add 1 to col
    curr_row = 0
    curr_col = 0
    for col, row in np.ndindex(np_grid.shape):
        if np_grid[row][col] == 0:
            curr_row = row
            curr_col = col
            col_i = col+1
            np_grid[row][col] = np_grid[row][col_i]
    for col, row in np.ndindex(np_grid.shape):
        if row == curr_row and col == curr_col+1:
            np_grid[row][col] = 0
    print(np_grid)
    print("\n")
    return np_grid

def play():
    #a star algorithm
    chosen_row = 0
    chosen_col = 0
    for col, row in np.ndindex(np_grid.shape):
        while(np_grid[row][col] != solution[row][col]):
            
            #find path
            chosen_row, chosen_col = find_num(solution[row][col])

            #swap numbers till we get to target number
            swap(chosen_row,chosen_col)

def find_num(val):

    #manhattan distance
    node_cost = np.zeros((3, 3))

    g_cost = 0
    h_cost = 0
    f_cost = np.zeros((3, 3))
    chosen_node_row = 0
    chosen_node_col = 0
    least_cost = math.inf

    #use manhattan distance to find shortest path from 0 to val, seeing other numbers as obstacles
    for col, row in np.ndindex(np_grid.shape):
        if(np_grid[row][col] == val):
            #need to start counting backwards
            h_cost = node_cost.sum()  #distance from end node to current index
        if(np_grid[row][col] == 0):
            node_cost[row][col] = 0
        elif((row+1 < 3 and col+1 < 3 and np_grid[row+1][col+1] == 0) or
             (row+1 < 3 and np_grid[row+1][col-1] == 0) or 
             (col+1 < 3 and np_grid[row-1][col+1] == 0) or 
             np_grid[row-1][col-1] == 0):
            node_cost[row][col] = math.inf
        elif((row+1 < 3 and np_grid[row+1][col] == 0) or
             (row+1 < 3 and np_grid[row][col+1] == 0) or 
             (np_grid[row-1][col] == 0) or 
             np_grid[row][col-1] == 0):
            node_cost[row][col] = 1
        else:
            node_cost[row][col] = math.inf

        g_cost = node_cost.sum() #distance from starting node to current position
        f_cost[row][col] = g_cost + h_cost

        if(f_cost[row][col] < least_cost and f_cost[row][col] != 0):
            least_cost = f_cost[row][col]
            chosen_node_row = row
            chosen_node_col = col
            #add this node to path
    return chosen_node_row, chosen_node_col

def swap(c_row,c_col):
    for col, row in np.ndindex(np_grid.shape):
        if(np_grid[row][col] == 0 and row == c_row+1 and col == c_col):
            move_up()
            break
        elif(np_grid[row][col] == 0 and row == c_row-1 and col == c_col):
            move_down()
            break
        elif(np_grid[row][col] == 0 and row == c_row and col == c_col+1):
            move_left()
            break
        elif(np_grid[row][col] == 0 and row == c_row+1 and col == c_col-1):
            move_right()
            break

#main function driver
start()
play()

#Outline of what i want to happen:
# new newGame = Game()
#
# newGame.start() //print original board config
# newGame.play() //prints each board config everytime AI makes a move until the board is sorted
# newGame.score() //prints out final config and how many moves the AI took and that it worked!
