
import pygame,sys
from config import PANTALLA,ANCHO,ALTO,TAMAÑO_NAVE,pos_inicial,lista_animaciones_nave,FPS,GRAVEDAD,BLANCO,AZUL,velocidad
from nivel import nivel1,nivel2,nivel3,survival,demo,rank
from vida import vidas
from nave import Nave
from puntaje import Puntaje
from ranking import Ranking
from imprimir import Imprimir

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

        self.grupo_nave.add(self.nave)
        #puntos
        
        self.puntos = Puntaje(40,40,24)
        self.sprites.add(self.puntos)
        self.puntos_nivel_uno =  100 #None
        self.puntos_nivel_dos =  100 #None
        self.puntos_nivel_tres =  100 #None
        self.puntos_survival =  100 #None

        
        #fuente
        pygame.font.init()
        self.font = pygame.font.SysFont(None,28)

        self.ranking = Ranking("ranking_juego.db",self.textos)

        self.ranking.cargar_valores_predeterminados() 

        self.lista_plataformas = []
        self.enemigos_muertos = 0
        self.aliados_muertos = 0
        self.input = ""
        self.escribiendo = False
        self.nivel = None
        self.opcion_menu = None
        self.salir = False
        self.survival = False
        self.is_playing = False
        self.victoria = False
        self.perdio = False
        self.pause = False
        self.debug = False
        self.ultimo_nivel = None
        pygame.init()
 
    
    def play(self):

        while not self.salir:

            self.reloj.tick(FPS)
            self.update()
            self.handle_events()
            
            self.render()
        

    def handle_events(self):
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
                            self.pause = True
                            self.textos.empty()
                            self.nivel.menu_config()

                
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

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                
                    for boton in self.textos:
                        if boton.rect.collidepoint(evento.pos):
   
                            if boton.texto == "comenzar":
                                self.nivel.inicio = True
                                self.textos.empty()
                                self.sprites.remove(self.nivel.background_sprite) 

                            elif boton.texto =="0%":
                                self.sonido.stop()        
                            elif boton.texto =="20%":
                                self.sonido.stop()
                                self.sonido.set_volume(20)
                                self.sonido.play()
                            elif boton.texto =="40%":
                                self.sonido.stop()
                                self.sonido.set_volume(40)
                                self.sonido.play()
                            elif boton.texto =="60%":
                                self.sonido.stop()
                                self.sonido.set_volume(60)
                                self.sonido.play()
                            elif boton.texto =="80%":
                                self.sonido.stop()
                                self.sonido.set_volume(80)
                                self.sonido.play()
                            elif boton.texto =="100%":
                                self.sonido.stop()
                                self.sonido.set_volume(100)
                                self.sonido.play()
                            
                            
            else:
                
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                
                    for boton in self.textos:
                        if boton.rect.collidepoint(evento.pos):
                            print("Button")

                            if self.opcion_menu == 5 :
                                if boton.es_textbox:
                                    print("click en escribir")
                                    boton.set_click(True)
                                    self.escribiendo = True
                                else:
                                    boton.set_click(False)
                                    self.escribiendo = False
                                if boton.texto == "aceptar" and self.escribiendo == False and self.puntos_nivel_uno != None and self.puntos_nivel_dos != None and self.puntos_nivel_tres != None:
                                    self.textos.empty()
                                    input = Imprimir(ANCHO//2,250,30,"ingrese su nombre:",BLANCO,True)
                                    volver = Imprimir(ANCHO - 500,450,28,"volver",BLANCO)
                                    guardar = Imprimir((ANCHO//2) - 250,450,28,"guardar",BLANCO)
                                    self.textos.add(input,volver,guardar)

                            if boton.texto == "1. Nivel 1":                                
                                self.opcion_menu = 1
                                self.comenzar_nivel()
                                print("Op 1")
                                
                            elif boton.texto == "2. Nivel 2":
                                self.opcion_menu = 2
                                self.comenzar_nivel()
                                print("Op 2 ")
                                
                            elif boton.texto == "3. Nivel 3":
                                self.opcion_menu = 3
                                self.comenzar_nivel()
                                print("Op 3 ")
                                
                            elif boton.texto == "4.Survival":
                                self.opcion_menu = 4
                                self.comenzar_nivel()
                                print("Op4")
                            elif boton.texto == "5.Ranking":
                                self.opcion_menu = 5
                                self.comenzar_nivel()                             
                            elif boton.texto == "volver":
                                if not self.pause:
                                    self.opcion_menu = 6
                                    self.comenzar_nivel()
                                    self.nave.playing = False                
                                    self.is_playing = False   
                                else:
                                    self.textos.empty()
                                    self.sprites.remove(self.nivel.background_sprite) 
                                    self.is_playing = True
                                    self.pause = False
                            elif boton.texto == "6.Configuracion":
                                self.textos.empty()
                                self.nivel.menu_config()
                            elif boton.texto == "play":
                                self.textos.empty()
                                self.nivel.intro(self.puntos_nivel_uno,self.puntos_nivel_dos,self.puntos_nivel_tres,self.puntos_survival)
                            elif boton.texto =="1. Reset score nivel 1":
                                self.puntos_nivel_uno = None
                            elif boton.texto =="2. Reset score nivel 2":
                                self.puntos_nivel_dos = None
                            elif boton.texto =="3. Reset score nivel 3":
                                self.puntos_nivel_tres = None
                            elif boton.texto =="4. Reset score Survival":
                                self.puntos_survival = None
                            elif boton.texto =="0%":
                                self.sonido.stop()        
                            elif boton.texto =="20%":
                                self.sonido.stop()
                                self.sonido.set_volume(20)
                                self.sonido.play()
                            elif boton.texto =="40%":
                                self.sonido.stop()
                                self.sonido.set_volume(40)
                                self.sonido.play()
                            elif boton.texto =="60%":
                                self.sonido.stop()
                                self.sonido.set_volume(60)
                                self.sonido.play()
                            elif boton.texto =="80%":
                                self.sonido.stop()
                                self.sonido.set_volume(80)
                                self.sonido.play()
                            elif boton.texto =="100%":
                                self.sonido.stop()
                                self.sonido.set_volume(100)
                                self.sonido.play()
                            if boton.texto == "guardar":                                               
                                puntos = self.puntos_nivel_uno+self.puntos_nivel_dos+self.puntos_nivel_tres
                                nombre = self.input
                                print(nombre)
                                self.ranking.agregar_puntaje( nombre,puntos)
                                self.ranking.ordenar()
                                posiciones = self.ranking.cargar_ranking(5)
                                for rank, (nombre, puntos) in enumerate(posiciones, start=1):
                                    print(f"Rank {rank}: {nombre} - {puntos} puntos")
                                self.escribiendo = False

                if evento.type == pygame.KEYDOWN:

                    if self.escribiendo :
                        
                        if evento.key == pygame.K_BACKSPACE:
                            self.input = self.input[:-1]

                        elif evento.key == pygame.K_RETURN:
                            print("toma el nombre")
                            puntos = self.puntos_nivel_uno+self.puntos_nivel_dos+self.puntos_nivel_tres
                            nombre = self.input
                            print(nombre)
                            self.ranking.agregar_puntaje( nombre,puntos)
                            self.ranking.ordenar()
                            posiciones = self.ranking.cargar_ranking(5)
                            for rank, (nombre, puntos) in enumerate(posiciones, start=1):
                                print(f"Rank {rank}: {nombre} - {puntos} puntos")
                            self.nivel.mostrar_ranking(posiciones,30,28,BLANCO)
                            self.escribiendo = False
                        else:
                            self.input += evento.unicode
                            for boton in self.textos:
                                if boton.es_textbox:
                                    boton.set_texto(self.input)
                            print(f"{self.input}")

 
                    if evento.key == pygame.K_ESCAPE and self.pause:
                        
                        self.textos.empty()
                        self.sprites.remove(self.nivel.background_sprite) 
                        self.is_playing = True
                        self.pause = False


    def comenzar_nivel(self):
        if self.nivel != None:
            self.nivel.terminar_nivel()
        self.victoria = False
        self.nivel = None
        self.nave.vidas.set_vidas(3)
        self.nave.speed_x = 0
        self.nave.speed_y = 0
        self.is_playing = True
        self.nave.playing = True
        self.perdio = False

    def gana_nivel(self):
        
        self.nivel.terminar_nivel()
        self.nivel = None
        self.perdio = False
        self.is_playing = False
        self.nave.playing = False        
        self.opcion_menu = 6


    def pierde_nivel(self):
        if self.survival == True:
            print("pierde y reconoce surv")
            self.puntos_survival = self.puntos.get_puntos()
            self.survival = False
            self.opcion_menu = 6
        self.nivel.terminar_nivel()
        self.nave.playing = False
        self.is_playing = False
        self.opcion_menu = 6
        self.nivel = None
        self.perdio = True
        self.victoria = False

    def update(self):
        if self.is_playing:
            self.sprites.add(self.nave)
            self.sprites.add(self.vidas_nave)

            if self.nave.vidas.get_vidas() == 0:
                self.pierde_nivel()

            match self.opcion_menu:

                case 1:
                    if self.nivel == None:
                        self.nave.playing = True
                        self.nivel = nivel1(self.textos,self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 2:
                    if self.nivel == None :
                        self.nave.playing = True
                        self.nivel = nivel2(self.textos,self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 3:
                    if self.nivel == None :
                        self.nave.playing = True
                        self.nivel = nivel3(self.textos,self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 4:
                    if self.nivel == None:
                        self.survival = True
                        self.nave.playing = True
                        self.nivel = survival(self.textos,self.sprites,self.plataformas,self.particulas,
                        self.trampas,self.lasers_aliados,self.lasers_enemigos,
                        self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos)
                    self.nivel.update()
                case 5:
                    if self.nivel == None:
                        self.is_playing = False
                        self.nave.playing = False
                        self.nivel = rank(self.textos,self.sprites,self.plataformas,self.particulas,
                            self.trampas,self.lasers_aliados,self.lasers_enemigos,
                            self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,
                            self.aliados_muertos,self.puntos,self.ranking,self.puntos_nivel_uno,self.puntos_nivel_dos,
                            self.puntos_nivel_tres,self.puntos_survival)     

                    self.nivel.update()

                case 6:
                    if self.pause == False:
                        if self.perdio :
                            self.comenzar_nivel()                    
                            
                        if self.nivel == None:
                            self.nave.playing = False                
                            self.is_playing = False        
                            self.nivel = demo(self.textos,self.sprites,self.plataformas,self.particulas,
                                    self.trampas,self.lasers_aliados,self.lasers_enemigos,self.aliados,
                                    self.enemigos,self.items,self.reloj,self.enemigos_muertos,
                                    self.aliados_muertos,self.puntos,self.puntos_nivel_uno,self.puntos_nivel_dos,
                                    self.puntos_nivel_tres,self.puntos_survival)     
                                
                            
                        self.nivel.update()
                    self.textos.update()
        

            if self.opcion_menu == 1:
                status = self.nivel.status_nivel(6,5,True)
                if status == 1:
                    self.puntos_nivel_uno = self.puntos.get_puntos()
                    self.gana_nivel()
                elif status == -1:
                    self.pierde_nivel()

            elif self.opcion_menu == 2:
                status = self.nivel.status_nivel(8,10,True)
                if status == 1:
                    self.puntos_nivel_dos = self.puntos.get_puntos()    
                    self.gana_nivel()
                elif status == -1:
                    self.pierde_nivel()

            elif self.opcion_menu == 3:
                status = self.nivel.status_nivel(10,15,True)
                if status == 1:
                    self.puntos_nivel_tres = self.puntos.get_puntos()
                    self.gana_nivel()
                elif status == -1:
                    self.pierde_nivel()

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


            self.sprites.update() 
        else:

            if self.pause == False:
                if self.nivel == None:
                    self.nave.playing = False                
                    self.is_playing = False   
                    self.nivel = demo(self.textos,self.sprites,self.plataformas,self.particulas,
                            self.trampas,self.lasers_aliados,self.lasers_enemigos,
                            self.aliados,self.enemigos,self.items,self.reloj,self.enemigos_muertos,self.aliados_muertos,self.puntos,
                            self.puntos_nivel_uno,self.puntos_nivel_dos,self.puntos_nivel_tres,self.puntos_survival)     
                    
   
                self.nivel.update()
                self.sprites.update()


            self.textos.update()
        

    def render(self):
  
        if self.is_playing:

            self.display.blit(self.fondo,(0,0))

            self.sprites.draw(self.display)
            self.textos.draw(self.display)
        else:
            #self.render_menu()
            self.display.blit(self.fondo,(0,0))

            self.sprites.draw(self.display)
            self.textos.draw(self.display)
        
        if self.debug:

            for sprite in self.sprites:
                pygame.draw.rect(self.display,AZUL,sprite.rect,2)

        pygame.display.flip()
        
    def render_menu(self):

        
        self.display.blit(self.fondo,(0,0))

        self.sprites.draw(self.display)
        self.textos.draw(self.display)
       