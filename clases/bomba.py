import pygame


class Bomba(pygame.sprite.Sprite):
    def __init__(self,path_explo, path_imagen:str,size:tuple,center:tuple,speed:int = 11):
        super().__init__()
        self.explo = path_explo
        self.path = path_imagen
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load(path_imagen).convert_alpha(),size)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.Bottom = self.rect.bottom   
        self.speed_y = speed
        self.que_hace = "movimiento"

    def update(self) -> None:
        self.rect.y += self.speed_y        
        self.animar()
    
    def animar(self):

        match self.que_hace:

            case"movimiento":
                self.image = pygame.transform.scale(
                    pygame.image.load(self.path).convert_alpha(),self.size)     

            case "explota":      
                self.speed_y = 0
                self.speed_x = 0
                self.image = pygame.transform.scale(
                    pygame.image.load(self.explo).convert_alpha(),self.size)
                self.kill()     
   