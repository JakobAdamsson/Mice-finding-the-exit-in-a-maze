"""GA Written by Jakob Adamsson"""


import numpy as np
import math
import random
import time
import names
import ctypes as c
from typing import Tuple, List
from finalMaze import finalMaze
from somemaze import someMaze
import os

"MAZE CONFIG"
ORIGIN = (20, 1)
GOAL = (20, 33)
MAZE = finalMaze(20, 1, 20, 33)

#ORIGIN = (14,6)
#GOAL = (1,15)
#MAZE =someMaze(14,6,1,15)

"""MICE CONFIG"""
POPULATION_SIZE = 100
N_STEPS = 1750
MUTATION_CHANCE = 0.4
NUM_MUTATIONS = int(N_STEPS*0.65)
EPOCHS = 1000

class Moves():
    NO_MOVE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    
class Mouse():
    def __init__(self, name, n_steps, fitness = 0, current_pos=None, start_pos = ORIGIN):
        self._name = name
        self._n_steps = n_steps
        self._fitness = fitness
        self._current_pos = current_pos
        self._start_pos = start_pos
        self._path = MAZE.copy()
        self._trail = []
        self._camper = 0
        self._moves = [random.choice([Moves.NO_MOVE, Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT]) for _ in range(self._n_steps)]
    

    @property
    def camper(self) -> int:
        return self._camper
    
    @property
    def trail(self) -> List[Tuple[int, int]]:
        return self._trail 
        
    @property
    def path(self) -> List[Tuple[int, int]]:
        return self._path

    @path.setter
    def path(self, path_step: Tuple[int, int]):
        x, y = path_step
        self._path[x][y] = 6
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def current_pos(self) -> Tuple[int, int]:
        return self._current_pos
    
    @current_pos.setter
    def current_pos(self, new_pos: Tuple[int, int]):
        self._current_pos = new_pos
    
    @property
    def moves(self) -> List[int]:
        return self._moves
    
    @moves.setter
    def moves(self, new_moves: List[int]):
        self._moves = new_moves

    @property
    def fitness(self) -> int:
        return self._fitness
    

    def inc_camper(self):
        self._camper += 1
    
    def move(self, index: int) -> int:
        return self._moves[index]

    def camper_fitness(self):
        self._fitness = 1000
    
    def reset_fitness(self):
        self._fitness = 0

    def set_new_fitness(self, goal: Tuple[int, int]):
        """Fitness calculated with the help of the euclidan distance, math formula: d = √[ (x_2 - x_1)^2 + (y_2 - y_1)^2]"""
        clib = c.CDLL(os.getcwd()+"/calc.so")
        euclidianfunc = clib.euclidianDistance
        euclidianfunc.argtypes = [c.c_int for _ in range(4)]
        euclidianfunc.restype = c.c_float
        
        if self.camper > 25:
            self.camper_fitness()
            return
        
        if euclidianfunc(self._current_pos[0], goal[0], self._current_pos[1], goal[1]) not in self.trail:
            self._fitness = euclidianfunc(self._current_pos[0], goal[0], self._current_pos[1], goal[1])
            self.trail.append(euclidianfunc(self._current_pos[0], goal[0], self._current_pos[1], goal[1]))
        else:
            self.inc_camper()

        
    def get_new_move(self, index: int) -> Tuple[int, int]:
        cur_x, cur_y = self.current_pos
        next_move = self.move(index)
        if next_move == Moves.NO_MOVE:
            next_x, next_y = cur_x, cur_y
        if next_move == Moves.UP:
            next_x, next_y = cur_x-1, cur_y
        if next_move == Moves.DOWN:
            next_x, next_y = cur_x+1, cur_y
        if next_move == Moves.LEFT:
            next_x, next_y = cur_x, cur_y-1
        if next_move == Moves.RIGHT:
            next_x, next_y = cur_x, cur_y+1
        
        return next_x, next_y
    
def check_if_valid_move(maze, move: Tuple[int, int]) -> bool:
    return True if maze[move[0]][move[1]] != 9 and maze[move[0]][move[1]] != 1 else False

def update_maze(maze, move: Tuple[int, int]):
    maze[move[0]][move[1]] = 6

def walk_maze(mice: List[Mouse], maze: MAZE, n_steps: int):
    for step in range(n_steps):
        for mouse in mice:
            new_move = mouse.get_new_move(step)
            if check_if_valid_move(maze, new_move): 
                mouse.current_pos = new_move
                mouse.path = new_move
                if mouse.current_pos == GOAL:
                    return
                update_maze(maze, new_move)

def mutate(mouse: Mouse, num_mutations: int):
    mutations = random.sample(range(len(mouse.moves)), k=num_mutations)
    for index in mutations:
        mouse.moves[index] = random.choice([Moves.NO_MOVE, Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT])

def crossover(mice: List[Mouse], n_steps: int, population_size: int, mutation_chance: int, origin: Tuple[int, int], num_mutations: int) -> List[Mouse]:
    sorted_mice = sorted(mice, key=lambda x:x.fitness, reverse=False)
    sorted_mice = sorted(mice, key=lambda x:x.camper, reverse=False)
    
    top_mice = sorted_mice[:100]
    
    new_generation = []
    for _ in range(population_size):
        dad_mouse = random.choice(top_mice)
        mom_mouse = random.choice(top_mice)
        cut_index = random.randint(0, n_steps)
        new_moves = dad_mouse.moves[:cut_index] + mom_mouse.moves[cut_index:]
        baby_mouse = Mouse(name = names.get_full_name(),n_steps=n_steps,current_pos = origin, start_pos=origin)
        baby_mouse.moves = new_moves
     
        if random.uniform(0, 1) < mutation_chance:
            mutate(baby_mouse, num_mutations)
            
        new_generation.append(baby_mouse)

    return top_mice + new_generation

def fill_maze(mouse: Mouse):
    for coordinate in mouse.path:
        MAZE[coordinate[0]][coordinate[1]] = 6

def main():
    winner_winner_chicken_dinner = []
    maze = MAZE.copy()

    population = [Mouse(name = names.get_full_name(),n_steps=N_STEPS ,current_pos=ORIGIN, start_pos=ORIGIN) for _ in range(POPULATION_SIZE)]
    
    for epoch in range(EPOCHS):
    
        walk_maze(population, maze, N_STEPS)
        
        for mouse in population:
            mouse.set_new_fitness(GOAL)
        
        if population[0].fitness == 0:
            fill_maze(population[0])
            winner_winner_chicken_dinner.append(population[0])
            break
        
        
        population = crossover(population, N_STEPS, POPULATION_SIZE, MUTATION_CHANCE, ORIGIN, NUM_MUTATIONS)
        if epoch % 10 == 0:
            print(f"\nbest mice of generation {epoch}:\n{population[0].name} {population[0].fitness} {population[0].current_pos} {population[0].camper}")
            for row in population[0].path:
                temp_row = [str(int(elem)) for elem in row]
                temp_row = [struct if struct != '1' else '#' for struct in temp_row]
                temp_row = [struct if struct != '0' else ' ' for struct in temp_row]
                temp_row = [struct if struct != '6' else '*' for struct in temp_row]
                temp_row = [struct if struct != '9' else '@' for struct in temp_row]
                print(' '.join(temp_row))  
            print(f"Current config:\ncurrent population size: {POPULATION_SIZE}, current steps: {N_STEPS}, current mutations {NUM_MUTATIONS}, current mutation chance {MUTATION_CHANCE}")
    
    
    print(f"\nAnd the winner is.... \n{winner_winner_chicken_dinner[0].name}\n{winner_winner_chicken_dinner[0].fitness}\n{winner_winner_chicken_dinner[0].current_pos}")
    for row in winner_winner_chicken_dinner[0].path:
        temp_row = [str(int(elem)) for elem in row]
        temp_row = [struct if struct != '1' else '#' for struct in temp_row]
        temp_row = [struct if struct != '0' else ' ' for struct in temp_row]
        temp_row = [struct if struct != '6' else '.' for struct in temp_row]
        print(' '.join(temp_row))         

main()
    