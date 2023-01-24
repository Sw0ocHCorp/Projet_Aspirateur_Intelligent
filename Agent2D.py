import random
from math import *
import numpy as np

GAUCHE= 0
DROITE= 1
HAUT= 2
BAS= 3
ASPIRATION= 4

# --> Classe modélisant l'agent évoluant dans l'environnement (Environnement 2D)
class Agent2D:
    # --* Constructeur
    def __init__(self, y_position, x_position, width_env, max_room):
        self.action= None
        self.x_position= x_position
        self.y_position= y_position
        self.init_x_position= x_position
        self.init_y_position= y_position
        self.max_room= max_room
        self.isCleaning= False
        self.visited_rooms= 1
        self.width_env= width_env
        self.height_env= ceil(max_room/width_env)
        self.haveCleaned= False
        self.selected_action= ""
        self.table_interne= dict()
        self.isInverted= False
        self.prev_action= ""
        self.wall_detection= np.array([False, False, False, False])

        if (((self.height_env-1) - self.init_y_position)  % 2) == 0:
            self.isAller= False
        else:
            self.isAller= True

        if (self.height_env % 2) == 0:
            if self.x_position == (self.width_env-1) & self.y_position == self.height_env-1:
                self.isLast= True
            else:
                self.isLast= False
        else:
            if self.x_position == 0 & self.y_position == self.height_env-1:
                self.isLast= True
            else:
                self.isLast= False
    
    def get_futures_location(self):
        return np.array([(self.y_position, self.x_position-1), (self.y_position, self.x_position+1), (self.y_position -1, self.x_position), (self.y_position +1, self.x_position)]) #Futures positions possibles | 0: Gauche | 1: Droite | 2: Haut | 3: Bas

    def set_walls_around(self, walls):
        self.wall_detection= walls

    # --* Méthode permettant de sélectionner le système de prise de décision / action
    def select_action(self, room, mode= 'r'):
        self.isCleaning= False
        if room is not None:
            if not room.isClean:
                if room.isPresent:
                    if self.haveCleaned:
                        self.haveCleaned= False
                        self.take_random_movement()
                        if mode == 'r':
                            self.take_random_movement()
                        elif mode == 'e':
                            self.take_optimal_movement(room)
                        elif mode == 's':
                            self.take_simple_movement()
                    else:
                        self.action= ASPIRATION
                        self.isCleaning= True
                        if mode != 's':
                            self.haveCleaned= True
                        self.selected_action= "|.^|"
                else:
                    print("L'aspirateur ne peut pas nettoyer la salle n'est pas présent dedans")
            else:
                if mode == 'r':
                    self.take_random_movement()
                elif mode == 'e':
                    self.take_optimal_movement(room)
                elif mode == 's':
                    self.take_simple_movement()
        return self.selected_action

    # --* Méthode modélisant le système prise de décision / action aléatoire
    def take_random_movement(self):
        self.action= random.randint(0, 3)
        while self.wall_detection[self.action]:
            self.action= random.randint(0, 3)
        self.selected_action= ""
        if self.action == GAUCHE:
            self.selected_action= "<-"
            self.x_position-= 1
            self.visited_rooms+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == DROITE:
            self.selected_action= "->"
            self.x_position+= 1
            self.visited_rooms+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == HAUT:
            self.selected_action= "^"
            self.y_position-= 1
            self.visited_rooms+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == BAS:
            self.selected_action= "v"
            self.y_position+= 1
            self.visited_rooms+= 1
            if self.haveCleaned:
                self.haveCleaned= False
            
    
    # --* Méthode modélisant le système de prise de décision / action selon la table de transition(etat interne)
    def take_optimal_movement(self, room):
        self.selected_action= ""
        room_name= room.get_name()
        if room_name not in self.table_interne:
            self.memorize_room_possibility(room)
        etat_possible= np.array(self.table_interne.get(room_name))
        self.action= random.choice(etat_possible)
        if self.action == GAUCHE:
            self.selected_action= "<-"
            self.x_position-= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == DROITE:
            self.selected_action= "->"
            self.x_position+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == HAUT:
            self.selected_action= "^"
            self.y_position-= 1
            if self.haveCleaned:
                self.haveCleaned= False
        elif self.action == BAS:
            self.selected_action= "v"
            self.y_position+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        self.visited_rooms+= 1
    
    # --* Méthode permettant de mémoriser les possibilités d'action pour chaque salle (dans la table de transition)
    def memorize_room_possibility(self, room):
        room_name= room.get_name()
        actions_possibles= np.array([])
        for i in range(len(self.wall_detection)):
            if self.wall_detection[i] == False:
                actions_possibles= np.append(actions_possibles, i)
        self.table_interne.update({room_name: actions_possibles})

    def take_simple_movement(self):
        if self.y_position >= 0 & self.y_position <= self.height_env-1:
            if (self.height_env % 2) == 0:          # SI LIGNES ENVIRONNEMENT PAIRE
                if (self.y_position % 2) == 0:
                    self.isAller= False
                else:
                    self.isAller= True
                if self.x_position == (self.width_env-1) and self.y_position == self.height_env-1:    # Dernière salle= BAS DROITE
                    self.isLast= True
                elif self.x_position == (self.width_env-1) and self.y_position == 0:                  # Première salle= HAUT DROITE
                    self.isLast= False        
            else:                                   # SI LIGNES ENVIRONNEMENT IMPAIRE
                if self.isInverted:     #TRAJET REST APRÈS ETRE PASSE PAR LA DERNIERE SALLE
                    if self.x_position == 0 and self.y_position == 0:                         # Reset
                        self.isLast= False
                    if self.x_position == (self.width_env-1) and self.y_position == self.height_env-1:    # Dernière salle= BAS DROITE
                        self.isLast= True
                        self.isInverted= False
                    elif self.x_position == (self.width_env-1) and self.y_position == 0:                  # Première salle= HAUT DROITE
                        self.isLast= False     
                    elif (self.y_position % 2) == 0:
                        self.isAller= True
                    else:
                        self.isAller= False
                else:                   #1er TRAJET JUSQU'A LA DERNIERE SALLE
                    if self.x_position == 0 and self.y_position == self.height_env-1:         # Dernière salle= BAS GAUCHE
                        self.isLast= True
                        self.isInverted= True
                    if self.x_position == 0 and self.y_position == 0:                         # Première salle= HAUT GAUCHE
                        self.isLast= False
                    elif (self.y_position % 2) == 0:
                        self.isAller= False
                    else:
                        self.isAller= True
            if self.isLast:
                self.selected_action= "^"
                self.y_position-= 1
            elif ((self.x_position == 0 and not self.prev_action == "v") and self.y_position != self.height_env-1) and not (self.x_position == 0 and self.y_position == 0 and self.isInverted):
                self.selected_action= "v"
                self.y_position+= 1
                self.visited_rooms+= 1
            elif ((self.x_position == self.width_env-1 and not self.prev_action == "v") and self.y_position != self.height_env-1) and not(self.x_position == self.width_env-1 and self.y_position == 0 and not self.isInverted):
                self.selected_action= "v"
                self.y_position+= 1
                self.visited_rooms+= 1
            elif self.isAller:
                self.selected_action= ">"
                self.x_position+= 1
                self.visited_rooms+= 1
            else:
                self.selected_action= "<"
                self.x_position-= 1
                self.visited_rooms+= 1
            self.prev_action= self.selected_action

    # --* Méthode GETTER du nombre de salle visitées
    def get_visited_rooms(self):
        return self.visited_rooms
    
    # --* Méthode permettant de réinitialiser l'agent
    def reset(self):
        self.x_position= self.init_x_position
        self.y_position= self.init_y_position
        self.action= None
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.isInverted= not self.isInverted
        if self.isInverted:
            if (self.height_env % 2) != 0:
                if self.x_position == (self.width_env-1) & self.y_position == self.height_env:
                    self.isLast= True
                if self.x_position == 0 & self.y_position == 0:
                    self.isLast= False
            else:
                if self.x_position == 0 & self.y_position == self.height_env:
                    self.isLast= True
                if self.x_position == 0 & self.y_position == 0:
                    self.isLast= False
        else:
            if (self.height_env % 2) == 0:
                if self.x_position == (self.width_env-1) & self.y_position == self.height_env:
                    self.isLast= True
                if self.x_position == 0 & self.y_position == 0:
                    self.isLast= False
            else:
                if self.x_position == 0 & self.y_position == self.height_env:
                    self.isLast= True
                if self.x_position == 0 & self.y_position == 0:
                    self.isLast= False

    # --* Méthode GETTER de la position de l'agent
    def get_room_position(self):
        return self.y_position, self.x_position