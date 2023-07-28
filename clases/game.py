
import pygame,sys
from config import PANTALLA,ANCHO,ALTO,TAMAÑO_NAVE,pos_inicial,lista_animaciones_nave,FPS,GRAVEDAD,BLANCO,AZUL,velocidad
from nivel import nivel1,nivel2,nivel3,survival
from vida import vidas
from nave import Nave
from puntaje import Puntaje
from ranking import Ranking
from imprimir import Imprimir
#juego


def cambiar_modo(debug:bool):

    debug = not debug

    return debug



class Game():
    def __init__(self) -> None:
        pygame.mixer.init()
        self.reloj = pygame.time.Clock()
        self.sonido = pygame.mixer.Sound("./sonido/Star Wars Imperial March FULL.mp3")
        self.sonido.play(1)
        self.display = pygame.display.set_mode((PANTALLA))
        pygame.display.set_caption("yoda")
        #grupos
        self.fondo = pygame.image.load("./imagenes/JUEGUITO MATU.png")
        self.sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.particulas = pygame.sprite.Group()
        self.trampas = pygame.sprite.Group()
        self.lasers_aliados = pygame.sprite.Group()
        self.lasers_enemigos = pygame.sprite.Group()
        self.aliados = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()    
        self.grupo_nave = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.textos = pygame.sprite.Group()

        #nave
        
        self.vidas_nave = vidas("./sprites/nave/inicio/14.png",50,40,3)
        self.nave = Nave("./sprites/nave/inicio/14.png",TAMAÑO_NAVE,pos_inicial,lista_animaciones_nave,self.vidas_nave)
        self.sprites.add(self.nave)
        self.sprites.add(self.vidas_nave)
        self.grupo_nave.add(self.nave)
        

        #puntos
        
        self.puntos = Puntaje(40,40,24)
        self.sprites.add(self.puntos)
        


        #fuente
        pygame.font.init()
        self.font = pygame.font.SysFont(None,28)


        self.ranking = Ranking("./ranking.json")

        self.ranking.cargar_ranking()


        
        self.lista_plataformas = []
        self.enemigos_muertos = 0
        self.aliados_muertos = 0
        self.nivel = None
        self.opcion_menu = None
        self.salir = False
        self.survival = False
        self.is_playing = False
        self.victoria = False
        self.perdio = False
        self.pause = False
        self.debug = False
        pygame.init()

    
                             
         
    
    def play(self):

        while not self.salir:

            self.reloj.tick(FPS)
            self.update()
            self.handle_events()
            
            self.render()
        

    def handle_events(self):
        #todo metodo event
        for evento in pygame.event.get():
        
            if evento.type == pygame.QUIT:
                self.salir = True
                pygame.quit()
                sys.exit()

            elif self.is_playing:
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_a:
                        self.nave.speed_x = -velocidad
                        self.nave.speed_y =  GRAVEDAD
                        self.nave.que_hace = "izquierda"
                        self.nave.propulsar(self.sprites,self.particulas,self.nave.que_hace)
                    elif evento.key == pygame.K_d:
                        self.nave.speed_x = velocidad
                        self.nave.speed_y =  GRAVEDAD
                        self.nave.que_hace = "derecha"
                        self.nave.propulsar(self.sprites,self.particulas,self.nave.que_hace)
                    elif evento.key == pygame.K_SPACE :
                        self.nave.speed_y = -velocidad
                    elif evento.key == pygame.K_s:
                        self.nave.dispara(self.sprites,self.lasers_aliados)
                    elif evento.key == pygame.K_p:
                        self.debug = cambiar_modo(self.debug)
                    elif evento.key == pygame.K_m:
                        self.sonido.stop() 
                    elif evento.key == pygame.K_p:
                        self.sonido.play()
                    elif evento.key == pygame.K_ESCAPE:
                        self.is_playing = False
                
                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_a and self.nave.speed_x < 0:
                        self.nave.speed_x = 0
                        self.nave.speed_y = 0                
                    elif evento.key == pygame.K_d and self.nave.speed_x > 0:
                        self.nave.speed_x = 0
                        self.nave.speed_y = 0
                    elif evento.key == pygame.K_SPACE :
                        self.nave.speed_y =  0
                        self.nave.puede_subir = True
            else:


                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.opcion_menu = 1
                        if self.nivel != None:
                            self.nivel.terminar_nivel()
                        self.victoria = False    
                        self.nivel = None
                        self.is_playing = True
                        self.perdio = False
                        print("Op 1")
                        
                    elif evento.key == pygame.K_2:
                        self.opcion_menu = 2
                        if self.nivel != None:
                            self.nivel.terminar_nivel()
                        self.victoria = False
                        self.nivel = None
                        self.is_playing = True
                        self.perdio = False
                        print("Op 2 ")
                        
                    elif evento.key == pygame.K_3:
                        self.opcion_menu = 3
                        if self.nivel != None:
                            self.nivel.terminar_nivel()
                        self.victoria = False
                        self.nivel = None
                        self.is_playing = True
                        self.perdio = False
                        print("Op 3 ")
                        
                    elif evento.key == pygame.K_4:
                        self.opcion_menu = 4
                        if self.nivel != None:
                            self.nivel.terminar_nivel()
                        self.victoria = False
                        self.nivel = None
                        self.is_playing = True
                        self.perdio = False
                        print("Op4")
                    elif evento.key == pygame.K_5:
                        self.opcion_menu = 5
                        if self.nivel != None:
                            self.nivel.terminar_nivel()
                        self.victoria = False
                        self.nivel = None
                        self.is_playing = True
                        self.perdio = False
                    
                        
                    elif evento.key == pygame.K_RETURN:
                        self.is_playing = True
                    elif evento.key == pygame.K_m:
                        self.sonido.stop()
                    elif evento.key == pygame.K_p:
                        self.sonido.play()
                    elif evento.key == pygame.K_ESCAPE:
                        self.is_playing = True


    def update(self):
        if self.is_playing:

            match self.opcion_menu:

                case 1:
                    if self.nivel == None:

                        self.nave.playing = True

                        self.nivel = nivel1(self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()

                case 2:
                    if self.nivel == None :

                        self.nave.playing = True

                        self.nivel = nivel2(self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()

                case 3:
                    if self.nivel == None :
                    
                        self.nave.playing = True

                        self.nivel = nivel3(self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 4:
                    if self.nivel == None:
                        self.nave.playing = True

                        self.nivel = survival(self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 5:
                    if self.nivel == None:
                        self.nivel = self.ranking
                        self.ranking.update(self.display, self.font, ANCHO//2, ALTO//2, 3)

            if self.nave.vidas == 0:
                if self.survival == True:
                    self.nivel.terminar_nivel()
                    self.survival = False

                self.nave.playing = False
                self.is_playing = False
                self.opcion_menu = None
                self.nivel = None
                self.perdio = True
                self.victoria = False

            
            if self.opcion_menu == 1:
                status = self.nivel.status_nivel(6,5,True)
                if status == 1:
                    #gana nivel
                    print("gana nivel 1")
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = False
                    self.opcion_menu = 2
                elif status == -1:
                    #perdio
                    self.nave.playing = False
                    self.is_playing = False
                    self.opcion_menu = None
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = True


            elif self.opcion_menu == 2:
                status = self.nivel.status_nivel(8,10,True)
                if status == 1:
                    #gana nivel
                    print("gana nivel 2")
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = False
                    self.opcion_menu = 3
             
                elif status == -1:
                    #perdio
                    self.nave.playing = False
                    self.is_playing = False
                    self.opcion_menu = None
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = True


            elif self.opcion_menu == 3:
                status = self.nivel.status_nivel(10,15,True)
                if status == 1:
                    #gana nivel
                    print("gana nivel 3")
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = False
                    self.victoria = True
                    self.opcion_menu = None
                    self.is_playing = False
                    self.nave.playing = False
                elif status == -1:
                    #perdio
                    self.nave.playing = False
                    self.is_playing = False
                    self.opcion_menu = None
                    self.nivel.terminar_nivel()
                    self.nivel = None
                    self.perdio = True
            elif self.opcion_menu == 4:
                status = self.nivel.status_nivel(0,0,False)

                if status == 0:
                    self.survival == True



            for trampa in self.trampas:
                lista = pygame.sprite.spritecollide(trampa,self.grupo_nave,False)
                if len(lista) != 0:
                    self.nave.vidas.reducir_vidas()
                    trampa.kill()
                        
            for item in self.items:
                lista = pygame.sprite.spritecollide(item,self.grupo_nave,False)
                if len(lista) != 0:
                    item.kill()
                    if self.nave.vidas.vidas < 3:
                        self.nave.vidas.sumar_vidas()
                    else:
                        self.puntos.sumar_puntos(100)

            for particula in self.particulas:
                
                if self.nave.rect.centerx - 90 > particula.rect.centerx or self.nave.rect.centerx + 90 < particula.rect.centerx or self.nave.rect.centery +2 < particula.rect.centery:
                    particula.kill()
            if self.nave.vidas.vidas == 0:
                self.nave.playing =False
                self.is_playing = False     
                self.opcion_menu = None 

            self.sprites.update() 
        else:
            titulo = Imprimir(((ANCHO//2-100)),int(200),int(28)," Menu Principal",BLANCO) #cambiar mensaje con metodo tipo menu ->str
            opcion_1 = Imprimir(ANCHO//3,300,28,"1. Nivel 1",BLANCO)
            opcion_2 = Imprimir(ANCHO//3,350,28,"2. Nivel 2",BLANCO)
            opcion_3 = Imprimir(ANCHO//3,400,28,"3. Nivel 3",BLANCO)
            opcion_4 = Imprimir(ANCHO//3,450,28,"4.Survival",BLANCO)
            opcion_5 = Imprimir(ANCHO//3,500,28,"5.Ranking",BLANCO)

            self.textos.add(titulo)
            self.textos.add(opcion_1)
            self.textos.add(opcion_2)       
            self.textos.add(opcion_3)
            self.textos.add(opcion_4)       
            self.textos.add(opcion_5)       

            self.textos.update()


       
    def render(self):
  
        if self.is_playing:

            self.display.blit(self.fondo,(0,0))

            self.sprites.draw(self.display)
        else:
            self.render_menu()
        


        if self.debug:

            for sprite in self.sprites:
                pygame.draw.rect(self.display,AZUL,sprite.rect,2)

                  

        pygame.display.flip()
        
    def render_menu(self):
        #self.display.blit(NEGRO)
        
        self.textos.draw(self.display)
       