import pygame
from config import nave_inicio,GRAVEDAD,ANCHO,ALTO
from bomba import Bomba
from vida import vidas
from propulsor import Propulsor

class Nave(pygame.sprite.Sprite):
    def __init__(self, path_imagen:str,size:tuple,center:tuple,animaciones:list,vidas:vidas):
        super().__init__()
        
        self.vidas = vidas
        self.rect = nave_inicio[0].get_rect()
        self.midleft = self.rect.midleft
        self.midright = self.rect.midright 
        self.size = size
        self.animaciones = animaciones
        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)

        self.rect.center = center
        self.speed_x = 0
        self.speed_y = GRAVEDAD

   
        self.puede_subir = True
        self.que_hace = "quieto"
        self.contador_movimiento = 0


        self.playing = True

    def update(self) -> None:
        if self.playing:
            
            self.mover()
            self.animar()
            


    def dispara(self,sprites,lasers):
        bomba = Bomba("sprites/nave/bomba/17.png","./sprites/nave/bomba/16.png",(28,42),self.rect.center)
        sprites.add(bomba)
        lasers.add(bomba)

    def stop(self):
        self.playing = False

    def animar(self): 
        

        match self.que_hace:
            
            case "quieto": 

                self.speed_y = 0
                self.animar_accion(self.animaciones[0])

            case"izquierda": # agregar particulas
 
                self.animar_accion(self.animaciones[2])

            case "derecha": 

                self.animar_accion(self.animaciones[5])
         
            case "muerto":

                self.animar_accion(self,self.animaciones[1])

    def animar_accion(self,animacion):            

        largo = len(animacion)
        if self.contador_movimiento >= largo:
            self.contador_movimiento = 0

        self.image = animacion[self.contador_movimiento]

        self.contador_movimiento += 1
    
    def propulsar(self,sprites,grupo_animaciones,que_hace:str):
        if que_hace == "izquierda":
                particula = Propulsor(self.animaciones[6],(49,100),self.rect.midright,self.speed_x,self.speed_y,"izquierda")
                sprites.add(particula)
                grupo_animaciones.add(particula)
        else:
                particula = Propulsor(self.animaciones[4],(49,100),self.rect.midleft,self.speed_x,self.speed_y,"derecha")
                sprites.add(particula)
                grupo_animaciones.add(particula)
    def mover(self):

        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y        

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= ANCHO:
            self.rect.right = ANCHO
         
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= ALTO-100:
            self.rect.bottom = ALTO -100
