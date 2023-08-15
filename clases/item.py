
import pygame, random
from config import ANCHO

class Item(pygame.sprite.Sprite):
    def __init__(self,path_imagen:str,size:tuple,center:tuple,speed:int=2,limite_y:int = 400 ):
        super().__init__()  
        self.path = path_imagen
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)
        self.rect = self.image.get_rect()        
        self.rect.center = center
        self.bottom = self.rect.bottom  
        self.speed_y = speed
        self.limite_y = limite_y
        self.direction_y = random.choice([-1, 1])
        self.direction_x = random.choice([-3, 3])

    def update(self):
        self.rect.y += self.speed_y * self.direction_y
        if self.rect.y > self.limite_y:
            self.direction_y *= -1
        elif self.rect.y < 40 :
            self.direction_y *= -1
    
        if self.rect.x > ANCHO:
            self.direction_x *= -1
        elif self.rect.y < 0 :
            self.direction_x *= -1            
