import pygame 


class Imprimir(pygame.sprite.Sprite):
    def __init__(self,x,y,tamano_fuente,texto:str,color = (255,255,255),es_box:bool = False) -> None:
        super().__init__()
        self.tam_fuente = tamano_fuente
        self.color_fuente = color
        self.texto = texto
        pygame.font.init()
        self.font = pygame.font.SysFont(None,self.tam_fuente)
        self.image = self.font.render(texto,True,self.color_fuente)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.es_textbox = es_box
        self.clicked = False

    def set_click(self,valor:bool):
        self.clicked = valor

    def set_texto(self,nuevo_texto:str):
        self.texto = nuevo_texto

    def update(self) -> None:
        self.image = self.font.render(self.texto,True,self.color_fuente)
             

