from colorama import Fore
from Classe import Classe
from Agent import Agent
from Agent2D import Agent2D
import random, string
import numpy as np
from math import *

class  Environnement():
    def __init__(self, rooms, dimension= 1):
        self.rooms= rooms
        self.messy_rooms= 0
        if dimension == 1:
            for room in self.rooms:
                if not room.isClean:
                    self.messy_rooms+= 1
        elif dimension == 2:
            for row in self.rooms:
                for room in row:
                    if room is not None:
                        if not room.isClean:
                            self.messy_rooms+= 1
    
    def attach_2D_agent(self, agent):
        self.agent= agent
        self.rooms[agent.y_position, agent.x_position].set_aspi_present(True)

    def attach_agent(self, agent):
        self.agent= agent
        self.rooms[agent.room_position].set_aspi_present(True)
    
    def agent_interactions(self, epochs= 10, dimension= 1, mode= 'r'):
        if dimension == 1:
            self.interaction_1D(epochs, mode= mode)
        elif dimension == 2:
            self.interaction_2D(epochs, mode= mode)
        else:
            print("Dimension non valide")

    def reset_2D_env(self):
        for row in rooms:
            for room in row:
                if room is not None:
                    room.reset_state()
        self.agent.reset()
        self.rooms[self.agent.y_position, self.agent.x_position].set_aspi_present(True)
        
    
    def reset_env(self):
        for room in self.rooms:
            room.reset_state()
        self.agent.reset()
        self.rooms[self.agent.room_position].set_aspi_present(True)
    
    def interaction_1D(self, epochs= 10, mode= 'r'):
        perf_array= np.array([])
        mark_array= np.array([])
        for e in range(epochs):
            self.reset_env()
            rooms= self.rooms
            visited_rooms= 0
            nb_actions= 0
            messy_rooms= self.messy_rooms
            print(" --> EPOCH#", e, end="\n")
            print("Etat Initial de l'environnement", end= "")
            env.print_1D_env(rooms)
            print(messy_rooms, " Salles à nettoyer", end= "\n")
            while messy_rooms > 0:
                agent_position= self.agent.get_room_position()
                isClean= rooms[agent_position].isClean
                selected_action= self.agent.select_action(rooms[agent_position], mode= mode)
                agent_position= self.agent.get_room_position()
                env.env_reaction(agent_position, rooms)
                n_isClean= rooms[agent_position].isClean
                if isClean == False and n_isClean == True:
                    messy_rooms-= 1
                nb_actions+= 1
                print("     > Action n°", nb_actions, "= ", selected_action, end="\n")
                self.print_1D_env(rooms)
                if self.agent.get_twUnbound == True:
                    print("L'agent à été stoppé car il voulait rentrer dans un mur", end="\n")
            visited_rooms= self.agent.get_visited_rooms()
            perf_mark= round(((self.agent.max_room + self.messy_rooms) / nb_actions) * 10)
            print("Nombre de salles visitées= ", visited_rooms)
            print("Note de Performance= ", perf_mark, " / 10")
            perf_array= np.append(perf_array, visited_rooms)
            mark_array= np.append(mark_array, perf_mark)
        print("Note moyenne= ", np.mean(mark_array), " / 10")
        print("Note max= ", np.max(mark_array), " / 10")
        

    def interaction_2D(self, epochs= 10, mode= 'r'):
        perf_array= np.array([])
        mark_array= np.array([])
        for e in range(epochs):
            self.reset_2D_env()
            rooms= self.rooms
            visited_rooms= 0
            nb_actions= 0
            messy_rooms= self.messy_rooms
            print(" --> EPOCH#", e, end="\n")
            print("Etat Initial de l'environnement", end= "")
            env.print_2D_env(rooms)
            print(messy_rooms, " Salles à nettoyer", end= "\n")
            while messy_rooms > 0:
                agent_y_pos, agent_x_pos= self.agent.get_room_position()
                isClean= rooms[agent_y_pos, agent_x_pos].isClean
                selected_action= self.agent.select_action(rooms[agent_y_pos, agent_x_pos],mode = mode)
                agent_y_pos, agent_x_pos= self.agent.get_room_position()
                env.env_2D_reaction(agent_y_pos, agent_x_pos, rooms)
                n_isClean= rooms[agent_y_pos, agent_x_pos].isClean
                if isClean == False and n_isClean == True:
                    messy_rooms-= 1
                nb_actions+= 1
                print("     > Action n°", nb_actions, "= ", selected_action, end="")
                self.print_2D_env(rooms)
                if self.agent.get_twUnbound == True:
                    print("L'agent à été stoppé car il voulait rentrer dans un mur", end="\n")
            visited_rooms= self.agent.get_visited_rooms()
            perf_mark= round(((self.agent.max_room + self.messy_rooms) / nb_actions) * 10)
            print("Nombre de salles visitées= ", visited_rooms)
            print("Note de Performance= ", perf_mark, " / 10")
            perf_array= np.append(perf_array, visited_rooms)
            mark_array= np.append(mark_array, perf_mark)
        print("Note moyenne= ", np.mean(mark_array), " / 10")
        print("Note max= ", np.max(mark_array), " / 10")
    
    def env_2D_reaction(self, agent_y_pos, agent_x_pos, rooms):
        for row in rooms:
            for room in row:
                if room is not None:
                    room.set_aspi_present(False)
                rooms[agent_y_pos, agent_x_pos].set_aspi_present(True)
        if self.agent.isCleaning:
            rooms[agent_y_pos, agent_x_pos].clean_room()

    def env_reaction(self, agent_position, rooms):
        for room in rooms:
            room.set_aspi_present(False)
        rooms[agent_position].set_aspi_present(True)
        if self.agent.isCleaning:
            rooms[agent_position].clean_room()
    
    def print_1D_env(self, rooms):
        for room in rooms:
            print(str(room), end="")
        print()

    def print_2D_env(self, rooms):
        for row in rooms:
            print()
            for room in row:
                if room is None:
                    print(Fore.BLACK + " N " + Fore.RESET, end="")
                else:
                    print(str(room), end="")
        print()

if __name__ == "__main__":
    rooms_names= np.array([], dtype= str)
    dimension= input("Entrée la dimension de l'environnement (1D ou 2D)? ")
    agent_mode= input("Entrée le mode de sélection d'actions de l'agent (Random ou Memorisation)? ")
    dimension= dimension.upper()
    if dimension == "1D":
        dimension= 1
        room_number= input("Entrée le nombre de salles de l'environnement (1D)? ")
        if room_number.isdigit():
            room_number= int(room_number)
            rooms= np.array([], dtype= Classe)
            for room in range(room_number):
                rand_clean= random.randint(0, 1)
                rand_name= random.choice(string.ascii_uppercase)
                if rand_name in rooms_names:
                    rand_name= random.choice(string.ascii_uppercase)
                else:
                    rooms_names= np.append(rooms_names, rand_name)
                rooms= np.append(rooms, Classe(rand_name, isClean= bool(rand_clean)))
            env= Environnement(rooms= rooms, dimension= 1)
            random_agent_seed=  rand_clean= random.randint(0, len(rooms)-1)
            env.attach_agent(Agent(random_agent_seed, len(rooms)))
            # ---> ALGORITHME D'EVOLUTION DE L'AGENT DANS L'ENVIRONNEMENT <--- #
            if agent_mode.upper() == "RANDOM":
                env.agent_interactions(epochs= 2, dimension= 1, mode= 'r')
            elif agent_mode.upper() == "MEMORISATION":
                env.agent_interactions(epochs= 2, dimension= 1, mode= 'e')

            #
    elif dimension.upper() == "2D":
        dimension= 2
        room_number= input("Entrée le nombre de salles de l'environnement (2D)? ")
        width_env= input("Entrée la largeur de l'environnement (2D)? ")
        if room_number.isdigit():
            if width_env.isdigit():
                room_number = int(room_number)
                width_env = int(width_env)
                n_row = ceil(room_number/width_env)
                room_row = np.array([], dtype=Classe)
                rooms = np.empty((n_row, width_env), dtype=Classe)
                global_cpt = 0
                for i in range(n_row):
                    cpt = 0
                    while cpt < width_env:
                        if global_cpt == room_number:
                            break
                        rand_clean = random.randint(0, 1)
                        rand_name = random.choice(string.ascii_uppercase)
                        if rand_name in rooms_names:
                            rand_name= random.choice(string.ascii_uppercase)
                        else:
                            rooms_names= np.append(rooms_names, rand_name)
                        room_row = np.append(room_row, Classe(
                        rand_name, isClean=bool(rand_clean)))
                        cpt += 1
                        global_cpt += 1
                    if cpt < width_env:
                        for j in range(width_env-cpt):
                            room_row = np.append(room_row, None)
                    rooms[i, :] = room_row
                    room_row = np.array([], dtype=Classe)
                env = Environnement(rooms=rooms, dimension=2)
                x_position = random.randint(0, width_env-1)
                y_position = random.randint(0, ceil(room_number/width_env)-1)
                while (y_position * width_env) + x_position >= room_number:
                    x_position = random.randint(0, width_env-1)
                    y_position = random.randint(0, ceil(room_number/width_env)-1)
                env.attach_2D_agent(Agent2D(y_position=1, x_position=2,
                                                width_env=width_env, max_room=room_number))
                # ---> ALGORITHME D'EVOLUTION DE L'AGENT DANS L'ENVIRONNEMENT <--- #
                if agent_mode.upper() == "RANDOM":
                    env.agent_interactions(epochs= 2, dimension= 2, mode= 'r')
                elif agent_mode.upper() == "MEMORISATION":
                    env.agent_interactions(epochs= 2, dimension= 2, mode= 'e')
    else:
        print("Dimension non valide")
    
"""
GAUCHE= 0
DROITE= 1
HAUT= 2
BAS= 3
"""