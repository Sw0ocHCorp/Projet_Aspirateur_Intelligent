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

def test_1(agent_position, room_number, width_env, messies_rooms, obstacles, mode):
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
            if (i, cpt) in obstacles:
                room_row = np.append(room_row, None)
            else:
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
    if mode == "m":
        env.agent.set_env(env)
    env.calculate_opti_cpt(is2D= True)
    env.wall_detection()
    env.agent_interactions(epochs= 2, dimension= 2, mode= mode)


#Q1-a/b
test_1((0,2), 9, 3, [(2,2)], [(1,0)], mode="m")

"""
#Q1-c/d
test_1((0,0), 9, 3, [(1,1)], [], mode="t")
"""
"""
#Q4 --> Faire Modif pour Supprimer Connaissance Innée de l'Environnement avant de lancer le Test(Voir P18 - 21 rapport PDF)
test_1((0,0), 9, 3, [(2,2)], [(1,1)], mode="m")
"""