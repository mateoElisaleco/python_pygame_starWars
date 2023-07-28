import pygame

#plataforma

class Plataforma(pygame.sprite.Sprite):

    def __init__(self, path_imagen:str,size:tuple,center:tuple):
        super().__init__()
        
        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.top = self.rect.top
        self.bottom = self.rect.bottom
        