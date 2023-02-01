import math
from Classe import Classe
import numpy as np
import random
import string

class AlgorithmeAStar():
    def __init__(self, env, agent, is2D= True):
        self.env= env
        self.agent= agent
        next_y= 0
        next_x= 0
        min_dist= 1000
        if is2D:
            self.ref_room= self.env.rooms[self.agent.y_position, self.agent.x_position]
        else:
            self.ref_room= self.env.rooms[self.agent.room_position]
        self.opti_cpt= self.env.messy_rooms
        r= self.env.rooms.copy()
        cpt= self.opti_cpt
        #env.print_2D_env(rooms= rooms)
        if is2D:
            checkpoints= [room for row in self.env.rooms for room in row if room != None and room.isClean == False]
            if (len(checkpoints) > 0):
                if(checkpoints[0] != self.ref_room):
                    checkpoints.insert(0, self.ref_room)
            for i in range(0, len(checkpoints)):
                mini= i
                dist_mini= 1000
                second= 0
                for j in range(i+1, len(checkpoints)):
                    if dist_mini > self.manhattan_distance(checkpoints[mini].position, checkpoints[j].position):
                        dist_mini= self.manhattan_distance(checkpoints[mini].position, checkpoints[j].position)
                        second= j
                if mini < len(checkpoints)-1:
                    checkpoints[mini+1], checkpoints[second]= checkpoints[second], checkpoints[mini+1]
            self.checkpoints= np.array(checkpoints, dtype= Classe) 
            for row in self.env.rooms:
                for room in row:
                    if room != None:
                        room.reset_state(full= False)
        self.is2D= is2D

    def get_obstacles(self):
        self.env.wall_detection()
        return self.agent.walls_detection
    
    def euclidian_distance(self, coord_o, coord_f):
        return math.sqrt(abs(coord_o[0]-coord_f[0]) + abs(coord_o[1]-coord_f[1]))
    
    def manhattan_distance(self, coord_o, coord_f):
        return abs(coord_o[0]-coord_f[0]) + abs(coord_o[1]-coord_f[1])
    
    def get_nb_action(self, room):
        
        while room != None:
            room= room.previous
            if room != None:
                self.opti_cpt+= 1
    
    def get_opti_actions(self):
        if self.is2D:
            for i in range(1, len(self.checkpoints)):
                start_room= self.checkpoints[i-1]
                start_room.set_init_room(True)
                self.reset_rooms()
                end_room= self.checkpoints[i]
                self.run_algorithm(start_room, end_room)
                start_room.set_init_room(False)
        else:
            movements= 0
            last_room= self.ref_room
            for i in range(self.agent.room_position, len(self.env.rooms)):
                if self.env.rooms[i].isClean == False:
                    last_room= self.env.rooms[i]
                movements += self.manhattan_distance(last_room.position, self.ref_room.position)
            if self.agent.room_position != 0:
                    movements= movements * 2
            for i in range(0, self.agent.room_position):
                if self.env.rooms[i].isClean == False:
                    last_room= self.env.rooms[i]
                    movements += self.manhattan_distance(last_room.position, self.ref_room.position)
                    self.opti_cpt += movements
                    return self.opti_cpt
            self.opti_cpt += movements
        return self.opti_cpt
    
    def reset_rooms(self):
        for i in range(self.env.rooms.shape[0]):
            for j in range(self.env.rooms.shape[1]):
                if self.env.rooms[i,j] is None:
                    continue
                else:
                    room= self.env.rooms[i,j]
                    room.reset_Astar_caracteristics()
    
    def run_algorithm(self, first_room, last_room):
        self.examined_rooms= np.array([], dtype= Classe)   #ClosedList | Classes déjà examinées
        self.discover_rooms= np.array([], dtype= Classe)    #OpenList | Classes découvertes mais pas encore examinées
        self.discover_rooms= np.append(self.discover_rooms, first_room)
        while len(self.discover_rooms) != 0:
            current_room= None
            f_min= 100000 
            for room in self.discover_rooms:
                if f_min > room.f:
                    f_min= room.f
                    current_room= room
            if current_room != None:
                if current_room == last_room:
                    #Retourner le chemin
                    return self.get_nb_action(current_room)
                else:
                    i= 0
                    bound= len(self.discover_rooms)
                    while i < bound:
                        if self.discover_rooms[i] == current_room:
                            self.discover_rooms= np.delete(self.discover_rooms, i)
                        i+= 1
                        bound= len(self.discover_rooms)
                    self.examined_rooms= np.append(self.examined_rooms, current_room)
                    neighbors= self.env.get_adjacent_rooms(current_room.position)
                    for room in neighbors:
                        if room is None:
                            continue
                        elif room in self.examined_rooms:
                            continue
                        elif room not in self.discover_rooms:
                            self.discover_rooms= np.append(self.discover_rooms, room)
                        newG= current_room.g + self.manhattan_distance(current_room.position, room.position)
                        if newG < room.g:
                            room.set_Astar_caracteristics(g= newG, h= self.euclidian_distance(room.position, last_room.position),
                                                                previous= current_room)
            else:
                break
    


            

    
