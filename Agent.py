import random
import numpy as np
GAUCHE= 0
DROITE= 1
ASPIRATION= 2

# --> Classe modélisant l'agent évoluant dans l'environnement (Environnement 1D)
class Agent:
    # --* Constructeur
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
        self.wall_detection= np.array([False, False])
        self.direction= DROITE
    
    def get_futures_location(self):
        return np.array([(0, self.room_position-1), (0, self.room_position+1)]) #Futures positions possibles | 0: Gauche | 1: Droite

    def set_walls_around(self, walls):
        self.wall_detection= walls

    # --* Méthode permettant de sélectionner le système de prise de décision / action
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
        self.twUnbound= False
        self.action= random.randint(0, 1)
        while self.wall_detection[self.action]:
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

    # --* Méthode modélisant le système de prise de décision / action selon la table de transition(etat interne)    
    def take_optimal_movement(self, room):
        self.selected_action= ""
        room_name= room.get_name()
        if room_name not in self.table_interne:
            self.memorize_room_possibility(room)
        actions_possibles= self.table_interne[room_name][0]
        prev_action= self.table_interne[room_name][1]
        self.action= random.choice(actions_possibles)
        if prev_action != -1:
            actions_possibles= np.append(actions_possibles, prev_action)
        prev_action= self.action
        if len(actions_possibles) > 1:
            actions_possibles= np.delete(actions_possibles, np.where(actions_possibles == self.action))
        self.table_interne.update({room_name: (actions_possibles, prev_action)})
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
    
    # --* Méthode permettant de mémoriser les possibilités d'action pour chaque salle (dans la table de transition)
    def memorize_room_possibility(self, room):
        room_name= room.get_name()
        actions_possibles= np.array([])
        for i in range(len(self.wall_detection)):
            if self.wall_detection[i] == False:
                actions_possibles= np.append(actions_possibles, i)
        self.table_interne.update({room_name: (actions_possibles, -1)})
        
    def take_simple_movement(self):
        if self.haveCleaned:
                self.haveCleaned= False
        if self.room_position >= 0 & self.room_position <= self.max_room-1:
            if self.wall_detection[0] == False and self.wall_detection[1] == True:
                self.direction= GAUCHE
            elif self.wall_detection[0] == True and self.wall_detection[1] == False:
                self.direction= DROITE
            if self.direction == GAUCHE:
                self.room_position-= 1
                self.visited_rooms+= 1
                self.selected_action= "<-"
            elif self.direction == DROITE:
                self.room_position+= 1
                self.visited_rooms+= 1
                self.selected_action= "->"

    
    # --* Méthode GETTER du nombre de salle visitées
    def get_visited_rooms(self):
        return self.visited_rooms

    # --* Méthode GETTER du Trigger Warning de sortie de l'environnement
    def get_twUnbound(self):
        return self.twUnbound

    # --* Méthode permettant de réinitialiser l'agent
    def reset(self):
        self.room_position= self.init_position
        self.action= None
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.twUnbound= False

    # --* Méthode GETTER de la position de l'agent
    def get_room_position(self):
        return self.room_position