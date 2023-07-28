        
import pygame,random

#trampa

class droide_aereo(pygame.sprite.Sprite): 

    def __init__(self,animaciones,path_imagen:str,size:tuple,center:tuple,speed:int = int(random.uniform(-11,-6)),y:int = int(random.uniform(-8,-14))):
        super().__init__()
        self.animaciones = animaciones
        self.path = path_imagen
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.Bottom = self.rect.bottom   
        self.speed_x = speed
        self.speed_y = y
        self.contador_movimiento = 0
        self.que_hace = "movimiento"
    
 
    def update(self) -> None:
        self.rect.x += self.speed_x        
        self.rect.y += self.speed_y

        self.animar()

        if self.rect.x < 0:
            self.kill()
        if self.rect.y < 0:
            self.kill()

    def animar(self):

        match self.que_hace:

            case"movimiento":
                self.animar_accion(self.animaciones[0])    

            case "explota":      
                self.speed_y = 0
                self.speed_x = 0
                self.animar_accion(self.animaciones[0])
                
    def animar_accion(self,animacion):            

        largo = len(animacion)
        if self.contador_movimiento >= largo:
            if self.que_hace == "explota":
                self.kill()
            self.contador_movimiento = 0


        self.image = animacion[self.contador_movimiento]

        self.contador_movimiento += 1
    
