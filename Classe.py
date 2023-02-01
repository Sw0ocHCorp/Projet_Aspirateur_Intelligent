from colorama import Fore

# --> Classe modélisant une salle de l'Environnement (1D ou 2D)
class Classe:
    # --* Constructeur
    def __init__(self, name, position, isClean= True):
        self.name= name
        self.isClean= isClean
        self.isPresent= False
        self.init_clean= isClean
        self.position= position
        self.g= 1000
        self.h= 0
        self.f= self.g + self.h
        self.previous= None
        self.isInit= False

    def set_init_room(self, isInit):
        self.isInit= isInit
    
    

    # --* Méthode permettant d'indiquer la présence de l'aspirateur
    def set_aspi_present(self, isPresent):
        self.isPresent = isPresent
        self.init_present= isPresent
    
    # --* Méthode GETTER de la présence de l'aspirateur
    def get_aspi_present(self):
        return self.isPresent
    
    # --* Méthode permettant de nettoyer la salle
    def clean_room(self):
        if self.isPresent:
            self.isClean= True
        else:
            print("L'aspirateur n'est pas présent dans la salle")

    # --* Méthode permettant de définir la salle comme sale
    def mess_room(self):
        self.isClean= False
    
    # --* Méthode GETTER du nom de la salle
    def get_name(self):
        return self.name
    
    # --* Méthode permettant de réinitialiser la salle
    def reset_state(self, full= True):
        self.isClean= self.init_clean
        if full:
            self.isPresent= False

    # --* Méthode permettant d'afficher la salle dans la console (avec la commande print(str(room)))
    def __str__(self) -> str:
        if self.isClean:
            if self.isPresent:
                return " " + self.name + "* "
            else:
                return " " + self.name + " "
        else:
            if self.isPresent:
                return " " + Fore.RED + self.name + Fore.RESET + "* "
            else:
                return " " + Fore.RED + self.name + Fore.RESET + " "
    
    def set_Astar_caracteristics(self, g, h, previous):
        self.g= g
        self.h= h
        self.f= g+h
        self.previous= previous
    def reset_Astar_caracteristics(self):
        if self.isInit:
            self.g= 0
        else:
            self.g= 1000
        self.h= 0
        self.f= 1000
        self.previous= None