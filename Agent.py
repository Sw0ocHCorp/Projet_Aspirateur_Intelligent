import random
import numpy as np
GAUCHE= 0
DROITE= 1
ASPIRATION= 2

class Agent:
    def __init__(self, room_position, max_room):
        self.room_position= room_position
        self.max_room= max_room
        self.action= None
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.twUnbound= False
        self.table_interne= dict()
        self.init_position= room_position
    
    def select_action(self, room, mode= 'r'):
        self.isCleaning= False
        if not room.isClean:
            if room.isPresent:
                if self.haveCleaned:
                    self.haveCleaned= False
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
        self.action= random.randint(0, 1)
        self.selected_action= ""
        if self.action == GAUCHE:
            self.selected_action= "<-"
            if self.room_position != 0:
                self.room_position-= 1
                self.visited_rooms+= 1
                if self.haveCleaned:
                    self.haveCleaned= False
            else:
                self.twUnbound= True
            
        elif self.action == DROITE:
            self.selected_action= "->"
            if self.room_position != self.max_room-1:
                self.room_position+= 1
                self.visited_rooms+= 1
                if self.haveCleaned:
                    self.haveCleaned= False
            else:
                self.twUnbound= True
        else:
            print("L'aspirateur ne peut pas nettoyer la salle n'est pas présent dedans")
            
    def take_optimal_movement(self, room):
        etat_possible= np.array([])
        self.twUnbound= False
        self.selected_action= ""
        room_name= room.get_name()
        if room_name not in self.table_interne:
            self.memorize_room_possibility(room)
        etat_possible= np.array(self.table_interne.get(room_name))
        self.action= random.choice(etat_possible)
        if self.action == GAUCHE:
            self.selected_action= "<-"
            self.room_position-= 1
            if self.haveCleaned:
                self.haveCleaned= False  
        elif self.action == DROITE:
            self.selected_action= "->"
            self.room_position+= 1
            if self.haveCleaned:
                self.haveCleaned= False
        self.visited_rooms+= 1
    
    def memorize_room_possibility(self, room):
        room_name= room.get_name()
        actions_possibles= np.array([])
        if self.room_position == 0:
            actions_possibles= np.append(actions_possibles, DROITE)
        elif self.room_position == self.max_room-1:
            actions_possibles= np.append(actions_possibles, GAUCHE)
        else:
            actions_possibles= np.append(actions_possibles, GAUCHE)
            actions_possibles= np.append(actions_possibles, DROITE)
        self.table_interne.update({room_name: actions_possibles})
        


    def get_visited_rooms(self):
        return self.visited_rooms

    def get_twUnbound(self):
        return self.twUnbound

    def reset(self):
        self.room_position= self.init_position
        self.action= None
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.twUnbound= False

    def get_room_position(self):
        return self.room_position