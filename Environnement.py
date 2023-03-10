from colorama import Fore
from Classe import Classe
from Agent import Agent
from Agent2D import Agent2D
import random, string
import numpy as np
from math import *

from AlgorithmeAStar import AlgorithmeAStar

# --> Classe modélisant l'environnement
class  Environnement():
    # --* Constructeur
    def __init__(self, rooms, dimension= 1, width= 0, height= 0,):
        self.rooms= rooms
        self.width= width
        self.height= height
        self.messy_rooms= 0
        self.opti_cpt= 0
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
    # --* Méthode permettant de lier l'agent à l'environnement (Pour une disposition 2D)
    def attach_2D_agent(self, agent):
        self.agent= agent
        self.rooms[agent.y_position, agent.x_position].set_aspi_present(True)
        self.man_distance= 0
        x= agent.x_position
        y= agent.y_position
        isPrevWall= False
        isWall= False
        for i in range(self.width):
            for j in range(self.height):
                if self.rooms[j, i] is not None:
                    if isPrevWall == True:
                        isWall= False
                        self.man_distance+=1
                    if not self.rooms[j, i].isClean:
                        self.man_distance += abs(x - i) + abs(y - j)
                        x= i
                        y= j
                else:
                    if (i == 0 & j == 0) | (i == self.width - 1 & j == 0) | (i == 0 & j == self.height - 1) | (i == self.width - 1 & j == self.height - 1):
                        pass
                    else:
                        if isPrevWall == False:
                            isWall= True
                        self.man_distance+=1
                        self.man_distance+=1
        self.man_distance+= self.messy_rooms
    # --* Méthode permettant de lier l'agent à l'environnement (Pour une disposition 1D)
    def attach_agent(self, agent):
        self.agent= agent
        self.rooms[agent.room_position].set_aspi_present(True)
    # --* Méthode permettant de choisir les interactions effectuées entre l'agent et l'environnement (en Fonction de la dimension de l'environnement)
    def agent_interactions(self, epochs= 10, dimension= 1, mode= 'r'):
        if dimension == 1:
            self.interaction_1D(epochs, mode= mode)
        elif dimension == 2:
            self.interaction_2D(epochs, mode= mode)
        else:
            print("Dimension non valide")
    # --* Méthode permettant de reset l'environnement (Pour une disposition 2D) || Utilisée pour préparer le prochain epoch
    def reset_2D_env(self):
        for row in self.rooms:
            for room in row:
                if room is not None:
                    room.reset_state()
        self.agent.reset()
        self.rooms[self.agent.y_position, self.agent.x_position].set_aspi_present(True)
        
    # --* Méthode permettant de reset l'environnement (Pour une disposition 1D) || Utilisée pour préparer le prochain epoch
    def reset_env(self):
        for room in self.rooms:
            room.reset_state()
        self.agent.reset()
        self.rooms[self.agent.room_position].set_aspi_present(True)

    def wall_detection(self, is2D= True):
        wall_rooms= np.array([])
        if is2D == True:
            for  location in self.agent.get_futures_location():
                if (location[0] < 0) | (location[0] >= self.height) | (location[1] < 0) | (location[1] >= self.width):
                    wall_rooms= np.append(wall_rooms, True)
                elif self.rooms[location[0], location[1]] is None:
                    wall_rooms= np.append(wall_rooms, True)
                else:
                    wall_rooms= np.append(wall_rooms, False)
        else:
            for location in self.agent.get_futures_location():
                if (location[1] < 0) | (location[1] >= len(self.rooms)):
                    wall_rooms= np.append(wall_rooms, True)
                elif self.rooms[location] is None:
                    wall_rooms= np.append(wall_rooms, True)
                else:
                    wall_rooms= np.append(wall_rooms, False)
        self.agent.set_walls_around(wall_rooms)
        
    def get_adjacent_rooms(self, location): #location = (x, y) | x = colonne | y = ligne (Convention plan 2D)
        adjacent_rooms= np.array([])
        adjacent_positions= np.array([(location[0], location[1]-1), (location[0], location[1]+1), (location[0] -1, location[1]), (location[0] +1, location[1])]) #Futures positions possibles | 0: Gauche | 1: Droite | 2: Haut | 3: Bas
        for location in adjacent_positions:
            if (location[1] < 0) | (location[1] >= self.width) | (location[0] < 0) | (location[0] >= self.height):
                continue
            elif self.rooms[location[0], location[1]] is None:
                continue
            else:
                adjacent_rooms= np.append(adjacent_rooms, self.rooms[location[0], location[1]])
        return adjacent_rooms
    
    def calculate_opti_cpt(self, is2D= True):
        self.astar_algo= AlgorithmeAStar(self, self.agent, is2D= is2D)
        self.opti_cpt= self.astar_algo.init_opti_cpt()
        if self.opti_cpt == -1:
            print("Erreur dans le calcul de la performance optimale")
            self.opti_cpt= 0

    # --* Méthode de modélisation des interactions entre l'agent et l'environnement (Pour une disposition 1D)
    def interaction_1D(self, epochs= 10, mode= 'r'):
        perf_array= np.array([])
        mark_array= np.array([])
        for e in range(epochs):
            self.reset_env()
            rooms= self.rooms
            nb_actions= 0
            messy_rooms= self.messy_rooms
            print(" --> EPOCH#", e, end="\n")
            print("Etat Initial de l'environnement", end= "")
            self.print_1D_env(rooms)
            print(messy_rooms, " Salles à nettoyer", end= "\n")
            print("Nombre d'actions Minimum= ", self.opti_cpt, end= "\n")
            while messy_rooms > 0:
                self.wall_detection(is2D= False)
                agent_position= self.agent.get_room_position()
                isClean= rooms[agent_position].isClean
                selected_action= self.agent.select_action(rooms[agent_position], mode= mode)
                agent_position= self.agent.get_room_position()
                self.env_reaction(agent_position, rooms)
                n_isClean= rooms[agent_position].isClean
                if isClean == False and n_isClean == True:
                    messy_rooms-= 1
                nb_actions+= 1
                print("     > Action n°", nb_actions, "= ", selected_action, end="\n")
                self.print_1D_env(rooms)
                if self.agent.get_twUnbound == True:
                    print("L'agent à été stoppé car il voulait rentrer dans un mur", end="\n")
            perf_mark= round(((nb_actions) / self.opti_cpt) * 10)
            print("Note de Performance= ", perf_mark, " / 10")
            perf_array= np.append(perf_array, nb_actions)
            mark_array= np.append(mark_array, perf_mark)
        print("Note moyenne= ", np.mean(mark_array), " / 10")
        print("Note max= ", np.max(mark_array), " / 10")
        
    # --* Méthode de modélisation des interactions entre l'agent et l'environnement (Pour une disposition 1D)
    def interaction_2D(self, epochs= 10, mode= 'r'):
        perf_array= np.array([])
        mark_array= np.array([])
        rooms= self.rooms
        visited_rooms= 0
        nb_actions= 0
        step= 0
        for e in range(epochs):
            modified_env= False
            print(" --> EPOCH#", e, end="\n")
            self.reset_2D_env()
            messy_rooms= self.messy_rooms
            print("Etat Initial de l'environnement", end= "")
            self.print_2D_env(rooms)
            print(messy_rooms, " Salles à nettoyer", end= "\n")
            print("Nombre d'actions Minimum pour tout Nettoyer= ", self.opti_cpt, end= "\n")
            if mode == 's':    
                selected_action= ""
                while messy_rooms > 0:
                    agent_y_pos, agent_x_pos= self.agent.get_room_position()
                    isClean= rooms[agent_y_pos, agent_x_pos].isClean
                    """if step == 0:
                        selected_action= self.agent.take_f_action()
                    else:"""
                    selected_action= self.agent.select_action(rooms[agent_y_pos, agent_x_pos],mode = mode)
                    agent_y_pos, agent_x_pos= self.agent.get_room_position()
                    self.env_2D_reaction(agent_y_pos, agent_x_pos, rooms)
                    n_isClean= rooms[agent_y_pos, agent_x_pos].isClean
                    if isClean == False and n_isClean == True:
                        messy_rooms-= 1
                    nb_actions+= 1
                    step+= 1
                    print("     > Action n°", nb_actions, "= ", selected_action, end="")
                    self.print_2D_env(rooms)
            else:
                    while messy_rooms > 0:
                        self.wall_detection(is2D= True)
                        agent_y_pos, agent_x_pos= self.agent.get_room_position()
                        isClean= rooms[agent_y_pos, agent_x_pos].isClean
                        selected_action= self.agent.select_action(rooms[agent_y_pos, agent_x_pos],mode = mode)
                        agent_y_pos, agent_x_pos= self.agent.get_room_position()
                        modified_env, added_messy_rooms= self.env_2D_reaction(agent_y_pos, agent_x_pos, rooms)
                        messy_rooms+= added_messy_rooms
                        n_isClean= rooms[agent_y_pos, agent_x_pos].isClean
                        if isClean == False and n_isClean == True:
                            messy_rooms-= 1
                        nb_actions+= 1
                        print("     > Action n°", nb_actions, "= ", selected_action, end="")
                        self.print_2D_env(rooms)
                        if modified_env:
                            self.opti_cpt= self.astar_algo.update_opti_cpt(rooms= rooms, opti_cpt= self.opti_cpt)
                            print("L'environnement à été modifié", end="\n")
                            print("Nombre Total d'actions Minimum= ", self.opti_cpt)
            perf_mark= 0
            if nb_actions > self.opti_cpt:
                perf_mark= 10 - (nb_actions - self.opti_cpt) * 0.5
                if perf_mark < 0:
                    perf_mark= 0
            else:
                perf_mark= round((nb_actions / self.opti_cpt) * 10)
                if perf_mark > 10:
                    perf_mark= 10
            print("Note de Performance= ", perf_mark, " / 10")
            perf_array= np.append(perf_array, visited_rooms)
            mark_array= np.append(mark_array, perf_mark)
        print("Note moyenne= ", np.mean(mark_array), " / 10")
        print("Note max= ", np.max(mark_array), " / 10")
    
    # --* Méthode de MAJ de l'Environnement en Fonction de l'action de l'agent (Pour une disposition 2D)
    def env_2D_reaction(self, agent_y_pos, agent_x_pos, rooms):
        nrow=0
        ncol= 0
        messy_rooms= 0
        modified_env= False
        for row in rooms:
            for room in row:
                if room is not None:
                    room.set_aspi_present(False)
                    if (nrow != agent_y_pos) & (ncol != agent_x_pos):
                        """if random.random() < 0.05:
                            modified_env= True
                            room.mess_room()
                            messy_rooms+= 1
                        """
                if rooms[agent_y_pos, agent_x_pos] is not None:
                    rooms[agent_y_pos, agent_x_pos].set_aspi_present(True)
            ncol += 1
            nrow += 1
        if self.agent.isCleaning:
            rooms[agent_y_pos, agent_x_pos].clean_room()
        return modified_env, messy_rooms

    # --* Méthode de MAJ de l'Environnement en Fonction de l'action de l'agent (Pour une disposition 1D)
    def env_reaction(self, agent_position, rooms):
        for room in rooms:
            room.set_aspi_present(False)
        rooms[agent_position].set_aspi_present(True)
        if self.agent.isCleaning:
            rooms[agent_position].clean_room()
    
    # --* Méthode d'affichage de l'environnement (Pour une disposition 1D)
    def print_1D_env(self, rooms):
        for room in rooms:
            print(str(room), end="")
        print()
    # --* Méthode d'affichage de l'environnement (Pour une disposition 2D)
    def print_2D_env(self, rooms):
        for row in rooms:
            print()
            for room in row:
                if room is None:
                    print(Fore.BLACK + " N " + Fore.RESET, end="")
                else:
                    print(str(room), end="")
        print()
"""
# --* TEST DE L'ENVIRONNEMENT   | FONCTION MAIN |
if __name__ == "__main__":
    rooms_names= np.array([], dtype= str)
    dimension= input("Entrée la dimension de l'environnement (1D ou 2D)? ")
    agent_mode= input("Entrée le mode de sélection d'actions de l'agent (Random ou Memorisation ou Simple)? ")
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
                if (rand_name in rooms_names):
                    rand_name= random.choice(string.ascii_uppercase)
                else:
                    rooms_names= np.append(rooms_names, rand_name)
                rooms= np.append(rooms, Classe(rand_name, isClean= bool(rand_clean), position= (0, room)))
            env= Environnement(rooms= rooms, dimension= 1)
            random_agent_seed=  rand_clean= random.randint(0, len(rooms)-1)
            env.attach_agent(Agent(len(rooms)-1, len(rooms)))
            # ---> ALGORITHME D'EVOLUTION DE L'AGENT DANS L'ENVIRONNEMENT <--- #
            env.calculate_opti_cpt(is2D= False)
            if agent_mode.upper() == "RANDOM":
                env.agent_interactions(epochs= 2, dimension= 1, mode= 'r')
            elif agent_mode.upper() == "MEMORISATION":
                env.agent_interactions(epochs= 2, dimension= 1, mode= 'e')
            elif agent_mode.upper() == "SIMPLE":
                env.agent_interactions(epochs= 2, dimension= 1, mode= 's')

            #
    elif dimension.upper() == "2D":
        dimension= 2
        room_number= input("Entrée le nombre de salles de l'environnement (2D)? ")
        width_env= input("Entrée la largeur de l'environnement (2D)? ")
        number_obstacles= input("Entrée le nombre maximum d'obstacles que vous voulez dans l'environnement (2D)? ")
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
                        isObstacle = False
                        if global_cpt == room_number:
                            break
                        rand_clean = random.randint(0, 1)
                        rand_name = random.choice(string.ascii_uppercase)
                        if rand_name in rooms_names or (rand_name == "N"):
                            rand_name= random.choice(string.ascii_uppercase)
                        else:
                            rooms_names= np.append(rooms_names, rand_name)
                        if str(number_obstacles).isdigit():
                            number_obstacles = int(number_obstacles)    
                            if number_obstacles > 0:
                                rand_obstacle = random.randint(0, 3)
                                if rand_obstacle == 3:
                                    isObstacle = True
                                    number_obstacles -= 1
                                    room_row = np.append(room_row, None)
                                else:
                                    room_row = np.append(room_row, Classe(
                                                            rand_name, isClean=bool(rand_clean), position= (i, cpt)))
                            else:
                                    room_row = np.append(room_row, Classe(
                                                            rand_name, isClean=bool(rand_clean), position= (i, cpt)))
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
                env.attach_2D_agent(Agent2D(y_position= y_position, x_position= x_position,
                                                width_env=width_env, max_room=room_number))
                # ---> ALGORITHME D'EVOLUTION DE L'AGENT DANS L'ENVIRONNEMENT <--- #
                env.calculate_opti_cpt(is2D= True)
                if agent_mode.upper() == "RANDOM":
                    env.agent_interactions(epochs= 2, dimension= 2, mode= 'r')
                elif agent_mode.upper() == "MEMORISATION":
                    env.agent_interactions(epochs= 2, dimension= 2, mode= 'e')
                elif agent_mode.upper() == "SIMPLE":
                    env.agent_interactions(epochs= 2, dimension= 2, mode= 's')
    else:
        print("Dimension non valide")
"""