
import pygame


class Puntaje(pygame.sprite.Sprite):
    def __init__(self,x,y,tamano_fuente,color = (255,255,255)) -> None:
        super().__init__()
        self.puntos = 0 
        self.tam_fuente = tamano_fuente
        self.color_fuente = color
        pygame.font.init()
        self.font = pygame.font.SysFont(None,self.tam_fuente)
        self.image = self.font.render(str(self.puntos),True,self.color_fuente)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        self.image = self.font.render(str(self.puntos),True,self.color_fuente)

    def sumar_puntos(self,sumar:int):
        self.puntos +=  sumar

    def get_puntos(self):
        retorno = self.puntos
        return retorno
    