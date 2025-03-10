import random
from random import randrange

#global variables
starting_index = randrange(9)
score = False
grid = [[random.sample(range(9),1)]*3]*3
starting_index = 0
empty_space = [starting_index] * 1 #starting node (changes to walkable)
other_spaces = [0] * 8 #obstacles
open_list = [1,1,1,1,1,1,1,1,1]
closed_list = [0,0,0,0,0,0,0,0,0]

class Node():
    neighbor_cost = [[0 for x in range(3)] for y in range(3)] #can be 3, 5, or 8
    g_cost = 0
    h_cost = 0
    f_cost = 0
    lowest_cost = 0

def calc_cost():
    
    for neighbor in neighbor_cost:
        if open_list[current_index] == 1: #if neighbor has open_list value of 1
                Node.g_cost = other_spaces[starting_index] - empty_space[current_index] #distance from starting node to current position
                Node.h_cost = other_spaces[target_index] - empty_space[current_index] #distance from end node to current index
                Node.f_cost = g_cost + h_cost

def a_star():
    
    starting_index = randrange(9)
    
    while score==False:
    
        calc_cost(empty_space[starting_index])
    
        for i, cost in enumerate(neighbor_cost):
            if i == 0:
                lowest_cost = Node.f_cost[0]
            if neighbor_cost[i] < neighbor_cost[i-1]:
                lowest_cost = Node.f_cost[i]
    
        for i, j in grid: 
            if Node.f_cost == lowest_cost:
                closed_list[i] = 1 #set as new node
                open_list[i] = 0
                starting_index = grid[i][j]
    
        #check that grid is in order
        if grid == [[1,2,3], [4,5,6], [7,8,9]]:
            score = True
            print("The AI won!")
            return score

def main():
    a_star() 