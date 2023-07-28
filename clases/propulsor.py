import pygame
from config import ANCHO,ALTO

class Propulsor(pygame.sprite.Sprite):
    def __init__(self, animacion:list,size:tuple,center:tuple,speed_x:int,speed_y:int,lado:str):
        super().__init__()

        self.center = center
        self.lado = lado
        self.animacion = animacion
        self.image = animacion[0]
        self.rect = self.image.get_rect()
        self.size = size 
        self.iniciar() 
        self.Bottom = self.rect.bottom   
        self.speed_y = speed_y
        self.speed_x = speed_x
        self.contador_particulas = 0
        
    
    def update(self) -> None:
        self.mover()
        self.animar()
   

    def animar(self):
        self.animar_particulas()

    def animar_particulas(self):
        
        largo = len(self.animacion)
        if self.contador_particulas >= largo:
            self.contador_particulas = 0

        self.image = self.animacion[self.contador_particulas]

        self.contador_particulas += 1

    def mover(self):
        


        self.rect.x += self.speed_x  
        self.rect.y += self.speed_y        

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= ANCHO:
                self.rect.right = ANCHO
         
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= ALTO:
            self.rect.bottom = ALTO

    def iniciar(self):

        if self.lado == "izquierda":

            self.rect.midleft = self.center
        else :
            self.rect.midright = self.center            
 