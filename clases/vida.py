import pygame
from config import ANCHO



class vidas(pygame.sprite.Sprite):
    def __init__(self,path_imagen:str,ancho:int,alto:int,vidas:int):
        super().__init__()
        self.vidas = vidas
        self.path = path_imagen
        self.ancho = ancho
        self.alto = alto
        self.imagen_vida = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),(self.ancho,self.ancho))
        self.width = int(self.ancho * self.vidas)
        self.image = pygame.Surface((self.width,self.alto))
        self.image.fill((0,0,0,255))
        self.rect = self.image.get_rect()
        self.Bottom = self.rect.bottom   
        self.rect.centerx = ANCHO//2
        self.rect.centery = self.alto
        

    def update(self) -> None:
        self.image = pygame.Surface((self.ancho * self.vidas, self.alto))   
        for i in range(self.vidas):
            
           self.image.blit(self.imagen_vida, (i * self.ancho, 0))              

    def reducir_vidas(self):
        if self.vidas > 0:
            self.vidas -= 1
        
    
    def sumar_vidas(self):
        if self.vidas < 3:
            self.vidas+= 1
