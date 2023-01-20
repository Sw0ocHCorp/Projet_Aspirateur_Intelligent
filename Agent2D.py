import random
from math import *
import numpy as np

GAUCHE= 0
DROITE= 1
HAUT= 2
BAS= 3
ASPIRATION= 4

class Agent2D:
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
        self.twUnbound= False
        self.table_interne= dict()
    
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
                    else:
                        self.action= ASPIRATION
                        self.isCleaning= True
                        self.haveCleaned= True
                        self.selected_action= "|.^|"
                else:
                    print("L'aspirateur ne peut pas nettoyer la salle n'est pas présent dedans")
            else:
                if mode == 'r':
                    self.take_random_movement()
                elif mode == 'e':
                    self.take_optimal_movement(room)
        return self.selected_action

    def take_random_movement(self):
        self.twUnbound= False
        self.action= random.randint(0, 3)
        self.selected_action= ""
        if self.action == GAUCHE:
            self.selected_action= "<-"
            if self.x_position != 0:
                self.x_position-= 1
                self.visited_rooms+= 1
                if self.haveCleaned:
                    self.haveCleaned= False
            else:
                self.twUnbound= True
        elif self.action == DROITE:
            self.selected_action= "->"
            if self.x_position != self.width_env-1:
                self.x_position+= 1
                self.visited_rooms+= 1
                if self.haveCleaned:
                    self.haveCleaned= False
            else:
                self.twUnbound= True
        elif self.action == HAUT:
            self.selected_action= "^"
            if self.y_position != 0:
                self.y_position-= 1
                self.visited_rooms+= 1
                if self.haveCleaned:
                    self.haveCleaned= False
            else:
                self.twUnbound= True
        elif self.action == BAS:
            self.selected_action= "v"
            if self.y_position != self.height_env:
                if (self.y_position + 1) * self.width_env + self.x_position < self.max_room:
                    self.y_position+= 1
                    self.visited_rooms+= 1
                    if self.haveCleaned:
                        self.haveCleaned= False
            else: 
                self.twUnbound= True
    
    def take_optimal_movement(self, room):
        self.twUnbound= False
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

    def memorize_room_possibility(self, room):
        room_name= room.get_name()
        actions_possibles= np.array([])
        #Test de déplacement vers la Droite | Permet de détecter les bords de l'environnement
        test= (self.y_position ) * self.width_env + self.x_position + 1 
        #Test de déplacement vers le Bas | Permet de détecter les bords de l'environnement
        main_test= (self.y_position + 1) * self.width_env + self.x_position 
        #SI ON A DES BORD EN BAS ET EN HAUT
        if (main_test > self.max_room -1) & (self.y_position == 0):
            #SI ON A UN BORD A DROITE || Bord si Dernière Salle
            if test >= self.max_room -1:
                #SI ON A UN BORD A GAUCHE
                if self.x_position == 0:
                    actions_possibles= np.append(actions_possibles, HAUT)
                #RESTE -> SI ON A RIEN A GAUCHE
                else:
                    actions_possibles= np.append(actions_possibles, GAUCHE)
            #SI ON A UN BORD A DROITE || Bord si Dernière Salle
            elif self.x_position == self.width_env-1:
                actions_possibles= np.append(actions_possibles, GAUCHE)
            #SINON SI ON A UN BORD A GAUCHE
            elif self.x_position == 0:
                actions_possibles= np.append(actions_possibles, DROITE)
            #RESTE -> SI ON A RIEN A DROITE ET A GAUCHE
            else:
                actions_possibles= np.append(actions_possibles, GAUCHE)
                actions_possibles= np.append(actions_possibles, DROITE)
        #SINON SI ON A UN BORD EN BAS
        elif main_test > self.max_room-1:
            actions_possibles= np.append(actions_possibles, HAUT)
            #SI ON A UN BORD A DROITE || Bord si ligne non complète
            if test > self.max_room-1:
                #SI ON A UN BORD A GAUCHE
                if self.x_position == 0:
                    pass                #Pas d'actions supplémentaires possibles
                #RESTE -> SI ON A RIEN A GAUCHE
                else:
                    actions_possibles= np.append(actions_possibles, GAUCHE)
            #SI ON A UN BORD A DROITE || Bord si Dernière Salle
            elif self.x_position == self.width_env-1:
                actions_possibles= np.append(actions_possibles, GAUCHE)
            #SINON SI ON A UN BORD A GAUCHE
            elif self.x_position == 0:
                actions_possibles= np.append(actions_possibles, DROITE)
            #RESTE -> SI ON A RIEN A DROITE ET A GAUCHE
            else:
                actions_possibles= np.append(actions_possibles, GAUCHE)
                actions_possibles= np.append(actions_possibles, DROITE)
        #SINON SI ON A UN BORD EN HAUT
        elif self.y_position == 0:
            actions_possibles= np.append(actions_possibles, BAS)
            #SI ON A UN BORD A DROITE || Bord si ligne non complète
            if test >= self.max_room-1:
                #SI ON A UN BORD A GAUCHE
                if self.x_position == 0:
                    pass                #Pas d'actions supplémentaires possibles
                #RESTE -> SI ON A RIEN A GAUCHE
                else:
                    actions_possibles= np.append(actions_possibles, GAUCHE)
            #SI ON A UN BORD A DROITE || Bord si Dernière Salle
            elif self.x_position == self.width_env-1:
                actions_possibles= np.append(actions_possibles, GAUCHE)
            #SINON SI ON A UN BORD A GAUCHE
            elif self.x_position == 0:
                actions_possibles= np.append(actions_possibles, DROITE)
            #RESTE -> SI ON A RIEN A DROITE ET A GAUCHE
            else:
                actions_possibles= np.append(actions_possibles, GAUCHE)
                actions_possibles= np.append(actions_possibles, DROITE)
        #RESTE -> SI ON A AUCUNS BORDS EN BAS ET EN HAUT
        else:
            #SI ON A UN BORD A GAUCHE
            if self.x_position == 0:
                actions_possibles= np.append(actions_possibles, DROITE)
                #SI SI ON A UN BORD EN BAS
                if main_test > self.max_room-1:
                    actions_possibles= np.append(actions_possibles, HAUT)
                #SINON SI ON A UN BORD EN HAUT
                elif self.y_position == 0:
                    actions_possibles= np.append(actions_possibles, BAS)
                #RESTE -> SI ON A RIEN EN BAS ET EN HAUT
                else: 
                    actions_possibles= np.append(actions_possibles, HAUT)
                    actions_possibles= np.append(actions_possibles, BAS)
            #SINON SI ON A UN BORD A DROITE
            elif self.x_position == self.width_env-1:
                actions_possibles= np.append(actions_possibles, GAUCHE)
                #SI SI ON A UN BORD EN BAS
                if main_test > self.max_room-1:
                    actions_possibles= np.append(actions_possibles, HAUT)
                #SINON SI ON A UN BORD EN HAUT
                elif self.y_position == 0:
                    actions_possibles= np.append(actions_possibles, BAS)
                #RESTE -> SI ON A RIEN EN BAS ET EN HAUT
                else: 
                    actions_possibles= np.append(actions_possibles, HAUT)
                    actions_possibles= np.append(actions_possibles, BAS)
            #RESTE -> SI ON A RIEN A GAUCHE ET A DROITE | Plus globalement, si on a AUCUNS BORDS    
            else:
                actions_possibles= np.append(actions_possibles, GAUCHE)
                actions_possibles= np.append(actions_possibles, DROITE)
                actions_possibles= np.append(actions_possibles, HAUT)
                actions_possibles= np.append(actions_possibles, BAS)
        self.table_interne.update({room_name: actions_possibles})


    def get_visited_rooms(self):
        return self.visited_rooms
    
    def get_twUnbound(self):
        return self.twUnbound
    
    def reset(self):
        self.x_position= self.init_x_position
        self.y_position= self.init_y_position
        self.action= None
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.twUnbound= False

    def get_room_position(self):
        return self.y_position, self.x_position