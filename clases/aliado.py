import pygame,random
from config import clon_camina,GRAVEDAD,lista_animaciones_laser_azul
from proyectil import Proyectil

class Aliado(pygame.sprite.Sprite):
    def __init__(self, path_imagen:str,size:tuple,center:tuple,animaciones:list,velocidad: int =3):
        super().__init__()
        
        self.animaciones = animaciones
        self.rect = clon_camina[0].get_rect()
        self.midleft = self.rect.midleft
        self.midright = self.rect.midright 
        self.size = size

        self.bottom = self.rect.bottom

        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)

        self.rect.center = center
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery        

         
        self.speed_y = GRAVEDAD


        self.velocidad = velocidad  
        self.speed_x = 0
        self.que_hace = "quieto"
        self.contador_movimiento = 0
        self.disparos_hechos = 0
        self.tiempo_disparo = 0

        self.playing = True
        self.decidio = False

    def update(self) -> None:
        if self.playing:
            self.animar()            
            self.mover()
        else: 
            self.kill()
            

        
    def dispara(self,sprites,lasers,enemigos):


        hora = pygame.time.get_ticks()
        if hora - self.tiempo_disparo >= 1000:
            laser = Proyectil(lista_animaciones_laser_azul,"sprites/miscelaneos/laser_azul/22.png",(23,54),(self.rect.centerx,self.rect.centery-15),12,int(random.uniform(-8,4)))
            sprites.add(laser)
            lasers.add(laser)
            self.que_hace = "dispara"
            self.tiempo_disparo = hora
            self.disparos_hechos += 1
        


    def stop(self):
        self.playing = False

    def animar(self): 
        
        match self.que_hace:
            
            case "quieto": 
                self.speed_y = 0
                self.speed_x = 0
                self.image = pygame.image.load("sprites/clon/camina/0.png")
                if self.tiempo_disparo > 0 :
                    self.tiempo_disparo -= 1 
            case "cae": 
                self.speed_y = GRAVEDAD
                self.speed_x = 0
                self.image = pygame.image.load("sprites/clon/camina/0.png")
                if self.tiempo_disparo > 0 :
                    self.tiempo_disparo -= 1 
            case"camina": 
                self.speed_y = 0
                self.speed_x = self.velocidad
                self.animar_accion(self.animaciones[0])
                if self.tiempo_disparo > 0 :
                    self.tiempo_disparo -= 1    

            case "dispara": 
                self.speed_y = 0
                self.speed_x = self.velocidad //2
                self.animar_accion(self.animaciones[1])
         
            case "muerto":
                self.speed_y = 0
                self.speed_x = 0              
                self.animar_muerte(self.animaciones[2])
                self.playing = False

            case "sale":
                self.speed_y = 0
                #self.speed_x = -self.velocidad
                self.speed_x = -6
                self.animar_accion(self.animaciones[0]) # falta animar correctamente
    def animar_accion(self,animacion):            

        largo = len(animacion)
        if self.contador_movimiento >= largo:
            if self.que_hace == "muerto":
                self.rect.y -= 15
                
                self.kill()
            self.contador_movimiento = 0

        self.image = animacion[self.contador_movimiento]

        self.contador_movimiento += 1
    def animar_muerte(self,animacion):
        largo = len(self.animaciones[2])
        if self.contador_movimiento >= largo:
            self.rect.y -= 15

            self.contador_movimiento = 0
            
        else:
            self.image = animacion[self.contador_movimiento]
            self.contador_movimiento += 1
    
    
    def mover(self):

        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y        

