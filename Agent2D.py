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
        self.isInverted= True
        self.prev_action= ""
        self.wall_detection= np.array([False, False, False, False])
        self.model= dict()
        self.isModelInit= False

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
        action= None
        selected_action= ""
        if room is not None:
            if not room.isClean:
                if room.isPresent:
                    if self.haveCleaned:
                        self.haveCleaned= False
                        if mode == 'r':
                            action= self.take_random_action()
                        elif mode == 'e':
                            action= self.take_optimal_action(room)
                        elif mode == 's':
                            action= self.take_simple_action()
                        elif mode == 'm':
                            action= self.take_action_from_model(room)
                        elif mode == 't':
                            action= self.take_action_from_tree() 
                    else:
                        if random.random() <= 1:
                            self.action= ASPIRATION
                            self.isCleaning= True
                            if mode != 's':
                                self.haveCleaned= True
                            selected_action= "|.^|"
                            return selected_action
                        else:
                            selected_action= "/!\ |.^|"
                            print("L'aspiration à échouée")
                            return selected_action
                            
                else:
                    print("L'aspirateur ne peut pas nettoyer la salle n'est pas présent dedans")
            else:
                if mode == 'r':
                    action= self.take_random_action()
                elif mode == 'e':
                    action= self.take_optimal_action(room)
                elif mode == 's':
                    action= self.take_simple_action()
                elif mode == 'm':
                    action= self.take_action_from_model(room)
                elif mode == 't':
                    action= self.take_action_from_tree() 
            if random.random() > 1:
                #L'actions Choisie échoue
                selected_action= "/!\ "
            else:
                if action == GAUCHE:
                    selected_action= "<-"
                    self.x_position-= 1
                    self.visited_rooms+= 1
                    if self.haveCleaned:
                        self.haveCleaned= False
                elif action == DROITE:
                    selected_action= "->"
                    self.x_position+= 1
                    self.visited_rooms+= 1
                    if self.haveCleaned:
                        self.haveCleaned= False
                elif action == HAUT:
                    selected_action= "^"
                    self.y_position-= 1
                    self.visited_rooms+= 1
                    if self.haveCleaned:
                        self.haveCleaned= False
                elif action == BAS:
                    selected_action= "v"
                    self.y_position+= 1
                    self.visited_rooms+= 1
                    if self.haveCleaned:
                        self.haveCleaned= False
        self.prev_action= selected_action
        return selected_action

    # --* Méthode modélisant le système prise de décision / action aléatoire
    def take_random_action(self):
        action= random.randint(0, 3)
        while self.wall_detection[action]:
            action= random.randint(0, 3)
        return action
            
    
    # --* Méthode modélisant le système de prise de décision / action selon la table de transition(etat interne)
    def take_optimal_action(self, room):
        room_name= room.get_name()
        if room_name not in self.table_interne:
            self.memorize_room_possibility(room)
        actions_possibles= self.table_interne[room_name][0]
        prev_action= self.table_interne[room_name][1]
        action= random.choice(actions_possibles)
        if prev_action != -1:
            actions_possibles= np.append(actions_possibles, prev_action)
        prev_action= action
        if len(actions_possibles) > 1:
            actions_possibles= np.delete(actions_possibles, np.where(actions_possibles == action))
            self.table_interne.update({room_name: (actions_possibles, prev_action)})
        return action
        
    # --* Méthode permettant de mémoriser les possibilités d'action pour chaque salle (dans la table de transition)
    def memorize_room_possibility(self, room):
        room_name= room.get_name()
        actions_possibles= np.array([])
        for i in range(len(self.wall_detection)):
            if self.wall_detection[i] == False:
                actions_possibles= np.append(actions_possibles, i)
        self.table_interne.update({room_name: (actions_possibles, -1)})

    def take_simple_action(self):
        action= None
        if self.haveCleaned:
                self.haveCleaned= False
        if self.y_position >= 0 & self.y_position <= self.height_env-1:
            if (self.height_env % 2) == 0:          # SI LIGNES ENVIRONNEMENT PAIRE
                if (self.y_position % 2) == 0:
                    self.isAller= False
                    action= DROITE
                else:
                    self.isAller= True
                    action= GAUCHE
                if self.x_position == (self.width_env-1) and self.y_position == self.height_env-1:    # Dernière salle= BAS DROITE
                    self.isLast= True
                    action= HAUT
                elif self.x_position == (self.width_env-1) and self.y_position == 0:                  # Première salle= HAUT DROITE
                    self.isLast= False        
            else:                                   # SI LIGNES ENVIRONNEMENT IMPAIRE
                if self.isInverted:     #TRAJET REST APRÈS ETRE PASSE PAR LA DERNIERE SALLE
                    if self.x_position == 0 and self.y_position == 0:                         # Reset
                        self.isLast= False
                        action= DROITE
                    elif self.x_position == (self.width_env-1) and self.y_position == self.height_env-1:    # Dernière salle= BAS DROITE
                        self.isLast= True
                        action= HAUT
                        self.isInverted= False
                    elif self.x_position == (self.width_env-1) and self.y_position == 0:                  # Première salle= HAUT DROITE
                        self.isLast= False     
                    elif (self.y_position % 2) == 0:
                        self.isAller= True
                        action= DROITE
                    elif self.isInverted == True:
                        action= HAUT
                    else:
                        self.isAller= False
                        action= DROITE
                else:                   #1er TRAJET JUSQU'A LA DERNIERE SALLE
                    if self.x_position == 0 and self.y_position == self.height_env-1:         # Dernière salle= BAS GAUCHE
                        self.isLast= True
                        action= HAUT
                        self.isInverted= True
                    elif self.x_position == 0 and self.y_position == 0:                         # Première salle= HAUT GAUCHE
                        self.isLast= False
                        action= BAS
                    elif self.x_position == (self.width_env-1) and self.y_position == 0:
                        action= GAUCHE
                    elif (self.x_position == self.width_env-1 or self.x_position == 0) and self.y_position + 1 <= self.height_env-1 and self.prev_action != "v":
                        action= BAS
                    elif (self.y_position % 2) != 0:
                        action= DROITE
                    else:
                        action= GAUCHE
        return action
            
    
    def take_action_from_model(self, room):
        #==> Version Connaissance Innée de l'Environnement
        if self.isModelInit == False:
            self.build_model()
            self.isModelInit= True
        else:
            self.update_model(room)     #--> APPEL FONCTION ACTUALISER-ETAT
        actions_possibles= self.model[room.position]
        #prev_action= self.table_interne[room_name][1]
        action= random.randint(0,3)
        while actions_possibles[action] == -1:
            action += 1
            if action == 4:
                action= 0
        return action
        """
        #==> Version Découverte de l'Environnement
        self.update_model(room)     #--> APPEL FONCTION ACTUALISER-ETAT
        actions_possibles= self.model[room.position]
        #prev_action= self.table_interne[room_name][1]
        action= random.randint(0,3)
        while actions_possibles[action] == -1:
            action += 1
            if action == 4:
                action= 0
        return action
        """
    #Création du Modèle Interne de l'Agent / Table de Transition de l'ensenble des états de l'environnement | Connaissance innée de l'Environnement
    def build_model(self):
        env= self.get_env()
        self.set_env(None)  
        for i in range(self.height_env):
            for j in range(self.width_env):
                actual_position= (i, j)
                action= 0
                #Futures positions possibles | 0: Gauche | 1: Droite | 2: Haut | 3: Bas
                next_positions= [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
                future_locations= dict() 
                for location in next_positions:
                    if env.rooms[actual_position] == None:
                        future_locations[action]= -1
                    elif (location[0] < 0) | (location[0] >= self.height_env) | (location[1] < 0) | (location[1] >= self.width_env) or env.rooms[location] == None:
                        future_locations[action]= -1
                    else:
                        future_locations[action]= location 
                    
                    action +=1
                self.model.update({actual_position: future_locations})

    def update_model(self, room):               #--> FONCTION ACTUALISER-ETAT    
        next_pos_dict= self.model.get(room.position)
        next_positions= [(room.position[0], room.position[1]-1), (room.position[0], room.position[1]+1), (room.position[0]-1, room.position[1]), (room.position[0]+1, room.position[1])]
        action= 0
        
        #==> Version Connaissance Innée de l'Environnement
        for wall in self.wall_detection:
            assert next_pos_dict is not None
            if wall == True and next_pos_dict.get(action) != -1:
                next_pos_dict.update({action: -1})
                self.model.update({next_positions[action]: -1})
            action += 1
        self.model.update({room.position: next_pos_dict})
        """
        #==> Version Découverte de l'Environnement
        self.set_env(None)
        actual_position= room.position
        future_locations= dict() 
        for location in next_positions:
            if self.wall_detection[action] == True:
                    future_locations[action]= -1
            else:
                future_locations[action]= location             
            action +=1
        self.model.update({actual_position: future_locations})
        """
        
    def take_action_from_tree(self):      #--> FONCTION TROUVER-REGLE   
        #   self.wall_detection= [left, right, top, bottom] corrsespond au detecteur de murs autour de l'Agent
        action= None
        if self.wall_detection[0] == True:          #--> S'il y a un mur à gauche   
            if self.wall_detection[1] == True:          #--> Sinon S'il y a un mur à droite
                if self.wall_detection[2] == True:      #--> Sinon S'il y a un mur en haut
                    if self.wall_detection[3] == True:  #--> Sinon S'il y a un mur en bas   | Entouré de murs
                        action= -1
                    else:                                   #Mur Gauche / Droite / Haut
                        action= BAS
                else:
                    if self.wall_detection[3] == True:      #Mur Gauche / Droite / Bas
                        action= HAUT
                    else:                                   #Mur Gauche / Droite
                        action= BAS
            else:
                if self.wall_detection[2] == True:
                    if self.wall_detection[3] == True:      #Mur Gauche / Haut / Bas
                        action= DROITE
                    else:                                   #Mur Gauche / Haut
                        action= DROITE
                else:
                    if self.wall_detection[3] == True:      #Mur Gauche / Bas
                        action= HAUT
                    else:                                   #Mur uniquement à gauche
                        if random.random() < 0.1:
                            action= DROITE
                        else:
                            action= HAUT

        elif self.wall_detection[1] == True:          #--> Sinon S'il y a un mur à droite
            if self.wall_detection[0] == True:          #--> Sinon S'il y a un mur à gauche
                if self.wall_detection[2] == True:      #--> Sinon S'il y a un mur en haut
                    if self.wall_detection[3] == True:  #--> Sinon S'il y a un mur en bas   | Entouré de murs
                        action= -1
                    else:                                   #Mur Droite / Gauche / Haut
                        action= BAS
                else:
                    if self.wall_detection[3] == True:      #Mur Droite / Gauche / Bas
                        action= HAUT
                    else:                                   #Mur Droite / Gauche                               
                        action= HAUT
            else:
                if self.wall_detection[2] == True:      
                    if self.wall_detection[3] == True:      #Mur Droite / Haut / Bas
                        action= -1
                    else:                                   #Mur Droite / Haut
                        action= BAS
                else:
                    if self.wall_detection[3] == True:      #Mur Droite / Bas
                        action= GAUCHE
                    else:                                   #Mur uniquement à Droite
                        if random.random() < 0.1:
                            action= GAUCHE
                        else:
                            action= BAS

        elif self.wall_detection[2] == True:      #--> Sinon S'il y a un mur en haut
            if self.wall_detection[0] == True:          #--> Sinon S'il y a un mur à gauche
                if self.wall_detection[1] == True:      #--> Sinon S'il y a un mur a droite
                    if self.wall_detection[3] == True:  #--> Sinon S'il y a un mur en bas   | Entouré de murs
                        action= -1
                    else:                                   #Mur Haut / Gauche / Droite
                        action= BAS
                else:
                    if self.wall_detection[3] == True:      #Mur Haut / Gauche / Bas
                        action= DROITE
                    else:                                   #Mur Haut / Gauche
                        action= DROITE
            else:
                if self.wall_detection[1] == True:
                    if self.wall_detection[3] == True:      #Mur Haut / Droite / Bas 
                        action= GAUCHE
                    else:                                   #Mur Haut / Droite
                        action= BAS
                else:
                    if self.wall_detection[3] == True:      #Mur Haut / Bas
                        action= DROITE
                    else:                                   #Mur uniquement en haut
                        if random.random() < 0.1:
                            action= BAS
                        else:
                            action= DROITE

        elif self.wall_detection[3] == True:      #--> Sinon S'il y a un mur en bas
            if self.wall_detection[0] == True:          #--> Sinon S'il y a un mur à gauche
                if self.wall_detection[1] == True:      #--> Sinon S'il y a un mur a droite 
                    if self.wall_detection[2] == True:  #--> Sinon S'il y a un mur en haut  | Entouré de murs
                        action= -1
                    else:                                   #Mur Bas / Gauche / Droite
                        action= HAUT
                else:
                    if self.wall_detection[2] == True:      #Mur Bas / Gauche / Haut
                        action= DROITE
                    else:                                   #Mur Bas / Gauche
                        action= HAUT
            else:
                if self.wall_detection[1] == True:
                    if self.wall_detection[2] == True:      #Mur Bas / Droite / Haut
                        action= GAUCHE
                    else:                                   #Mur Bas / Droite
                        action= GAUCHE
                else:
                    if self.wall_detection[2] == True:      #Mur Bas / Haut
                        action= GAUCHE
                    else:                                   #Mur uniquement en bas
                        if random.random() < 0.1:
                            action= HAUT
                        else:
                            action= GAUCHE
        else:                                    #--> Sinon aucun mur                               
            action= random.randint(0,3)
        return action
    
    # --* Méthode permettant de réinitialiser l'agent
    def reset(self):
        self.x_position= self.init_x_position
        self.y_position= self.init_y_position
        self.isCleaning= False
        self.visited_rooms= 1
        self.haveCleaned= False
        self.selected_action= ""
        self.isInverted= not self.isInverted
        self.model= dict()
        self.table_interne= dict()
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

    def set_env(self, env):
        self.env= env
    def get_env(self):
        return self.env