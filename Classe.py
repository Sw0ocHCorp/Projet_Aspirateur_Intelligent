from colorama import Fore

class Classe:
    def __init__(self, name, isClean= True):
        self.name= name
        self.isClean= isClean
        self.isPresent= False
        self.init_clean= isClean
    
    def set_aspi_present(self, isPresent):
        self.isPresent = isPresent
        self.init_present= isPresent
    
    def get_aspi_present(self):
        return self.isPresent
    
    def clean_room(self):
        if self.isPresent:
            self.isClean= True
        else:
            print("L'aspirateur n'est pas présent dans la salle")

    def mess_room(self):
        self.isClean= False
    
    def get_name(self):
        return self.name
    
    def reset_state(self):
        self.isClean= self.init_clean
        self.isPresent= False

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