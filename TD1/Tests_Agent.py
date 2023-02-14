from math import *
import string
import random
import numpy as np
import sys	

sys.path.append('C:\\Users\\nclsr\\OneDrive\\Bureau\\Cours_L3IA\\Agent_Intelligent')
from Agent import Agent
from Agent2D import Agent2D
from Environnement import Environnement
from Classe import Classe

#==> Test Agent avec réflexes simples dans un environnement 2D
# S'assurer que ligne 238 - 241 du fichier Environnement.py sont commentées
# remplacer la ligne 100 du fichier Agent2D.py par : if random.random() > 1: 
# et remplacer la ligne 76 du fichier Agent2D.py par : if random.random() <= 1:
def test_1(agent_position, room_number, width_env, messies_rooms):
    rooms_names= np.array([], dtype= str)
    n_row = ceil(room_number/width_env)
    room_row = np.array([], dtype=Classe)
    rooms = np.empty((n_row, width_env), dtype=Classe)
    global_cpt = 0
    for i in range(n_row):
        cpt = 0
        while cpt < width_env:
            isObstacle = False
            if global_cpt == room_number:
                break
            rand_clean = random.randint(0, 1)
            rand_name = random.choice(string.ascii_uppercase)
            if rand_name in rooms_names or (rand_name == "N"):
                rand_name= random.choice(string.ascii_uppercase)
            else:
                rooms_names= np.append(rooms_names, rand_name)
            isClean = True
            if (i, cpt) in messies_rooms:
                isClean = False
            room_row = np.append(room_row, Classe(
                        rand_name, isClean=isClean, position= (i, cpt)))
            cpt += 1
        rooms[i, :] = room_row
        room_row = np.array([], dtype=Classe)
    env = Environnement(rooms=rooms, dimension=2, width=width_env, height=n_row)
    env.attach_2D_agent(Agent2D(y_position= agent_position[0], x_position= agent_position[1],
                                                width_env=width_env, max_room=room_number))
    env.calculate_opti_cpt(is2D= True)
    env.agent_interactions(epochs= 1, dimension= 2, mode= 's')


def test_2(agent_position, room_number, width_env, messies_rooms, number_obstacles, agent_mode):
    rooms_names= np.array([], dtype= str)
    n_row = ceil(room_number/width_env)
    room_row = np.array([], dtype=Classe)
    rooms = np.empty((n_row, width_env), dtype=Classe)
    global_cpt = 0
    for i in range(n_row):
        cpt = 0
        while cpt < width_env:
            isObstacle = False
            isClean = True
            if global_cpt == room_number:
                break
            if (i, cpt) in messies_rooms:
                isClean = False
            rand_name = random.choice(string.ascii_uppercase)
            if rand_name in rooms_names or (rand_name == "N"):
                rand_name= random.choice(string.ascii_uppercase)
            else:
                rooms_names= np.append(rooms_names, rand_name)
            
            number_obstacles = int(number_obstacles)    
            if number_obstacles > 0:
                rand_obstacle = random.randint(0, 3)
                if rand_obstacle == 3:
                    isObstacle = True
                    number_obstacles -= 1
                    room_row = np.append(room_row, None)
                else:
                    room_row = np.append(room_row, Classe(
                                                    rand_name, isClean= isClean, position= (i, cpt)))
            else:
                room_row = np.append(room_row, Classe(
                                                    rand_name, isClean= isClean, position= (i, cpt)))
            cpt += 1
            global_cpt += 1
        if cpt < width_env:
            for j in range(width_env-cpt):
                room_row = np.append(room_row, None)
        rooms[i, :] = room_row
        room_row = np.array([], dtype=Classe)
    env = Environnement(rooms=rooms, dimension=2, width=width_env, height=n_row)
    x_position = random.randint(0, width_env-1)
    y_position = random.randint(0, ceil(room_number/width_env)-1)
    while (y_position * width_env) + x_position >= room_number or env.rooms[y_position, x_position] is None:
        x_position = random.randint(0, width_env-1)
        y_position = random.randint(0, ceil(room_number/width_env)-1)
    env.attach_2D_agent(Agent2D(y_position= agent_position[0], x_position= agent_position[1],
                                                width_env=width_env, max_room=room_number))
                # ---> ALGORITHME D'EVOLUTION DE L'AGENT DANS L'ENVIRONNEMENT <--- #
    env.calculate_opti_cpt(is2D= True)
    if agent_mode.upper() == "RANDOM":
        env.agent_interactions(epochs= 1, dimension= 2, mode= 'r')
    elif agent_mode.upper() == "MEMORISATION":
        env.agent_interactions(epochs= 1, dimension= 2, mode= 'e')
    elif agent_mode.upper() == "SIMPLE":
        env.agent_interactions(epochs= 1, dimension= 2, mode= 's')
"""
#Q2
# S'assurer que ligne 238 - 241 du fichier Environnement.py sont commentées
# remplacer la ligne 100 du fichier Agent2D.py par : if random.random() > 1: 
# et remplacer la ligne 76 du fichier Agent2D.py par : if random.random() <= 1:

# --> Test 1.1= Environnement 2D, Stratégie Simple , 9 pièces dont 3 par lignes, Agent2D en (0,0), 3 pièces sales (0,1), (2,0), (2,2)
test_1((0,0), 9, 3, [(0,1), (2,0), (2,2)])
# --> Test 1.2= Environnement 2D, Stratégie Simple , 9 pièces dont 3 par lignes, Agent2D en (0,2), 3 pièces sales (0,1), (2,0), (2,2)
test_1((0,2), 9, 3, [(0,1), (2,0), (2,2)])
# --> Test 1.3= Environnement 2D, Stratégie Simple , 9 pièces dont 3 par lignes, Agent2D en (1,1), 3 pièces sales (0,1), (0,2), (2,1), (2,2)
test_1((1,1), 9, 3, [(0,1), (0,2), (2,1), (2,2)])
# --> Test 1.3= Environnement 2D, Stratégie Simple , 9 pièces dont 3 par lignes, Agent2D en (0,2), 3 pièces sales (2,0)
test_1((1,1), 9, 3, [(2,0)])
"""
"""
#Q3
#--> Test 1.3
test_1((1,1), 9, 3, [(0,1), (0,2), (2,1), (2,2)])
print("---------------------------------------------")
print("---------------------------------------------")
#--> Test 2
test_2(agent_position= (1,1), room_number= 9, width_env= 3, messies_rooms= [(0,1), (0,2), (2,1), (2,2)], number_obstacles= 0, agent_mode= "RANDOM")
print("---------------------------------------------")
"""
"""
#Q4
test_2(agent_position= (1,1), room_number= 9, width_env= 3, messies_rooms= [(0,1), (0,2), (2,1), (2,2)], number_obstacles= 0, agent_mode= "MEMORISATION")
"""
"""
#Q7
test_1((0,2), 9, 3, [(1,2)])
print("---------------------------------------------")
print("---------------------------------------------")
test_2(agent_position= (0,2), room_number= 9, width_env= 3, messies_rooms= [(1,2)], number_obstacles= 0, agent_mode= "RANDOM")
"""
"""
#Q8
test_1((0,2), 9, 3, [(1,0)])                            #Agent Réflexes Simples
print("---------------------------------------------")
print("---------------------------------------------")
test_2(agent_position= (0,2), room_number= 9, width_env= 3, messies_rooms= [(1,0)], number_obstacles= 0, agent_mode= "RANDOM")
"""
"""
#Q9
#test_1((0,2), 9, 3, [(1,2)])                            #Agent Réflexes Simples
print("---------------------------------------------")
print("---------------------------------------------")
test_2(agent_position= (0,2), room_number= 9, width_env= 3, messies_rooms= [(1,2)], number_obstacles= 2, agent_mode= "MEMORISATION")
"""
