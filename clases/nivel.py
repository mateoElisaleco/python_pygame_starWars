import pygame,puntaje,random
from config import PANTALLA,ANCHO,ALTO,lista_animaciones_droide,lista_animaciones_clon,lista_animaciones_especiales_droide,BLANCO,mensaje_nivel_uno_1,mensaje_nivel_uno_2,mensaje_nivel_dos_1,mensaje_nivel_dos_2,mensaje_nivel_dos_3,mensaje_nivel_tres,mensaje_survival
from trampa import droide_aereo
from plataforma import Plataforma
from enemigo import Enemigo
from aliado import Aliado
from item import Item
from imprimir import Imprimir
from puntaje import Puntaje
from ranking import Ranking
class nivel():
    def __init__(self,textos:pygame.sprite.Group,sprites:pygame.sprite.Group,plataformas:pygame.sprite.Group,particulas:pygame.sprite.Group,trampas:pygame.sprite.Group,
                 lasers_aliados:pygame.sprite.Group,lasers_enemigos:pygame.sprite.Group,aliados:pygame.sprite.Group,enemigos:pygame.sprite.Group,
                 items:pygame.sprite.Group,reloj:pygame.time.Clock,enemigos_muertos:int,aliados_muertos:int,puntos:Puntaje) -> None:
        
        self.sprites = sprites
        self.plataformas = plataformas
        self.particulas = particulas
        self.trampas = trampas
        self.lasers_aliados = lasers_aliados
        self.lasers_enemigos = lasers_enemigos
        self.aliados = aliados
        self.enemigos = enemigos
        self.items = items
        self.reloj = reloj
        self.enemigos_muertos = enemigos_muertos
        self.aliados_muertos = aliados_muertos
        self.textos = textos    
        self.inicio = False
        self.puntos = puntos
        self.puntos.set_puntos(0)

    def menu_config(self):


        background = pygame.Surface(PANTALLA,pygame.SRCALPHA)
        background.fill((0,0,0,128)) 
        self.background_sprite = pygame.sprite.Sprite()
        self.background_sprite.image = background
        self.background_sprite.rect = background.get_rect()

        

        audio_1 = Imprimir(ANCHO//3,500,28,"0%",BLANCO)
        audio_2 = Imprimir((ANCHO//3)+50,500,28,"20%",BLANCO)
        audio_3 = Imprimir((ANCHO//3)+100,500,28,"40%",BLANCO)
        audio_4 = Imprimir((ANCHO//3)+150,500,28,"60%",BLANCO)
        audio_5 = Imprimir((ANCHO//3)+200,500,28,"80%",BLANCO)
        audio_6 =Imprimir((ANCHO//3)+250,500,28,"100%",BLANCO)
        play = Imprimir(ANCHO//3,450+100,28,"volver",BLANCO)
        self.textos.add(audio_1,audio_2,audio_3,audio_4,audio_5,audio_6,play)    
        self.sprites.add(self.background_sprite)



    def intro(self,texto_boton:str):
        background = pygame.Surface(PANTALLA,pygame.SRCALPHA)
        background.fill((0,0,0,128)) 

        comenzar = Imprimir(ANCHO//4,600,28,texto_boton,BLANCO)
        self.background_sprite = pygame.sprite.Sprite()
        self.background_sprite.image = background
        self.background_sprite.rect = background.get_rect()

        self.sprites.add(self.background_sprite)
        self.textos.add(comenzar)

    def terminar_nivel(self):
        for plataforma in self.plataformas:
            plataforma.kill()
        for trampa in self.trampas:
            trampa.kill()
        for particula in self.particulas:
            particula.kill()
        for laser in self.lasers_aliados:
            laser.kill()
        for laser in self.lasers_enemigos:
            laser.kill()
        for aliado in self.aliados:
            aliado.kill()
        for enemigo in self.enemigos:
            enemigo.kill()
        for item in self.items:
            item.kill()
        self.textos.empty()
        self.sprites.remove(self.background_sprite)
        self.inicio = False
        
   
    def status_nivel(self,bajas_aliados:int,bajas_enemigos:int,objetivos:bool):

        retorno = 0
        if objetivos:
            if self.enemigos_muertos >= bajas_enemigos:
                retorno = 1
            if self.aliados_muertos >= bajas_aliados:
                retorno = -1
        return retorno

    def update(self):
    
        if self.inicio:    
            for enemigo in self.enemigos:
                if enemigo.rect.left > ANCHO:
                    enemigo.kill()
                else:
                    lista = pygame.sprite.spritecollide(enemigo, self.aliados, True)
                    if lista:
                        enemigo.kill()
                        self.enemigos_muertos += 1
                    
                    coliciono = pygame.sprite.spritecollideany(enemigo, self.plataformas)
                    if coliciono:
                        enemigo.que_hace = "camina"                    
                        if enemigo.rect.x < 900 and enemigo.disparos_hechos < 4:
                            enemigo.que_hace = "dispara"
                            enemigo.dispara(self.sprites,self.lasers_enemigos,self.enemigos)
                        else: enemigo.que_hace = "camina"
                    else:
                        enemigo.que_hace = "cae"


            for aliado in self.aliados:
                if aliado.rect.left > ANCHO:
                    aliado.kill()
                else:
                    lista = pygame.sprite.spritecollide(aliado,self.enemigos,True)
                    if lista: 
                        aliado.kill()
                        self.aliados_muertos += 1

                    coliciono = pygame.sprite.spritecollideany(aliado,self.plataformas)
                    if coliciono:
                        aliado.que_hace = "camina"
                        if aliado.rect.x > 400 and aliado.disparos_hechos < 6:
                            aliado.que_hace = "dispara"
                            aliado.dispara(self.sprites, self.lasers_aliados, self.enemigos)
                        else: aliado.que_hace = "camina"
                    else: aliado.que_hace = "cae"

            for laser in self.lasers_aliados:
                lista =  pygame.sprite.spritecollide(laser,self.enemigos,False)
                for enemigo in lista:
                    enemigo.que_hace = "muerto"
                    laser.que_hace = "explota"
                    self.enemigos_muertos += 1
                    self.puntos.sumar_puntos(66)

            for laser in self.lasers_enemigos:
                lista =  pygame.sprite.spritecollide(laser,self.aliados,False)
                for aliado in lista:
                    aliado.que_hace = "muerto"
                    laser.que_hace = "explota"
                    self.aliados_muertos += 1
                    # falta sumar puntos


            for plataforma in self.plataformas:
                for laser in self.lasers_enemigos:
                    if laser.rect.colliderect(plataforma):
                        laser.que_hace = "explota"
                        
                    else:
                        lista = pygame.sprite.spritecollide(laser,self.aliados,False)
                        if len(lista) != 0:
                            laser.que_hace = "explota"
                            
                for laser in self.lasers_aliados:
                    if laser.rect.colliderect(plataforma):
                        laser.que_hace = "explota"

                    
    def generar_enemigo(self):
        x = random.randint(ANCHO//2+200,ANCHO)
        y = random.randint(300,ALTO//2)
        enemigo1 = Enemigo("./sprites/droide/camina/4.png",(46,53),(x,y),lista_animaciones_droide,-4)        
        self.sprites.add(enemigo1)
        self.enemigos.add(enemigo1)
        
    def generar_aliado(self):

        x = random.randint(40,100)
        y = random.randint(300,ALTO//2)
        aliado1 = Aliado("./sprites/clon/camina/0.png",(37,56),(x,y),lista_animaciones_clon,4)
        self.sprites.add(aliado1)
        self.aliados.add(aliado1)
        
    def generar_trampas(self):
            
        trampa = droide_aereo(lista_animaciones_especiales_droide,"./sprites/droide/vuela/0.png",(46,53),(ANCHO - 150,ALTO - 150),int(random.uniform(-11,-6)), int(random.uniform(-8,-14)))
        self.sprites.add(trampa)
        self.trampas.add(trampa)
        #self.lasers_enemigos.add(trampa)

    def generar_item(self):
        
        obj = Item("./sprites/nave/inicio/14.png",(40,30),(int(random.uniform(30,ANCHO-30)),int(random.uniform(500,20))))
        self.sprites.add(obj)
        self.items.add(obj)

class nivel1(nivel):
    def __init__(self,textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_enemigo = 0
        self.temporizador_aliado = 0
        self.tiempo_enemigo = 3000
        self.tiempo_aliado = 6000

        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)

        self.plataforma = Plataforma("./imagenes/plataforma.png",(250,26),(1100,self.piso.top-150))
        self.sprites.add(self.plataforma)
        self.plataformas.add(self.plataforma)
        self.intro(mensaje_nivel_uno_1,mensaje_nivel_uno_2,"comenzar")        

    def intro(self,mensaje_nivel_uno_1,mensaje_nivel_uno_2,mensaje:str):
        super().intro(mensaje)
        texto_uno = Imprimir(ANCHO//4,300,28,mensaje_nivel_uno_1,BLANCO)
        texto_dos = Imprimir(ANCHO//4,350,28,mensaje_nivel_uno_2,BLANCO)
        self.textos.add(texto_uno,texto_dos)

    def update(self):
        super().update() 
        if self.inicio:    
            self.temporizador_aliado += self.reloj.get_time()
            self.temporizador_enemigo += self.reloj.get_time()
                            
            if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 3:
                self.generar_aliado()
                self.temporizador_aliado = 0

            if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
                self.generar_enemigo()
                self.temporizador_enemigo = 0


class nivel2(nivel):
    def __init__(self,textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_enemigo = 0
        self.temporizador_aliado = 0
        self.temporizador_trampa = 0
        self.tiempo_enemigo = 2000
        self.tiempo_aliado = 6000
        self.tiempo_trampa = 4000


        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)

        self.plataforma = Plataforma("./imagenes/plataforma.png",(125,26),(1100,self.piso.top-200))
        self.sprites.add(self.plataforma)
        self.plataformas.add(self.plataforma)
        
        self.plataforma1 = Plataforma("./imagenes/plataforma.png",(125,26),(1000,self.piso.top-100))
        self.sprites.add(self.plataforma1)
        self.plataformas.add(self.plataforma1)

        self.plataforma2 = Plataforma("./imagenes/plataforma.png",(125,26),(1200,self.piso.top-100))
        self.sprites.add(self.plataforma2)
        self.plataformas.add(self.plataforma2)
        self.intro(mensaje_nivel_dos_1,mensaje_nivel_dos_2,mensaje_nivel_dos_3,"comenzar")        

    def intro(self,mensaje_nivel_dos_1,mensaje_nivel_dos_2,mensaje_nivel_dos_3,mensaje:str):
        super().intro(mensaje)
        texto_uno = Imprimir(ANCHO//4,300,28,mensaje_nivel_dos_1,BLANCO)
        texto_dos = Imprimir(ANCHO//4,350,28,mensaje_nivel_dos_2,BLANCO)
        texto_tres = Imprimir(ANCHO//4,400,28,mensaje_nivel_dos_3,BLANCO)
        self.textos.add(texto_uno,texto_dos,texto_tres)


    def update(self):
        super().update() 
        if self.inicio:    
            self.temporizador_aliado += self.reloj.get_time()
            self.temporizador_enemigo += self.reloj.get_time()
            self.temporizador_trampa += self.reloj.get_time()
                            
            if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 3:
                self.generar_aliado()
                self.temporizador_aliado = 0

            if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
                self.generar_enemigo()
                self.temporizador_enemigo = 0

            if self.temporizador_trampa >= self.tiempo_trampa and len(self.trampas) < 4: 
                self.generar_trampas()
                self.temporizador_trampa = 0

class nivel3(nivel):
    def __init__(self,textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_enemigo = 0
        self.temporizador_aliado = 0
        self.temporizador_item = 0
        self.temporizador_trampa = 0
        self.tiempo_enemigo = 2000
        self.tiempo_aliado = 6000
        self.tiempo_trampa = 2000
        self.tiempo_item = 5000

        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)
        self.intro(mensaje_nivel_tres,"comenzar")        

    def intro(self,mensaje_nivel_tres,mensaje:str):
        super().intro(mensaje)
        texto_uno = Imprimir(ANCHO//4,300,28,mensaje_nivel_tres,BLANCO)
        self.textos.add(texto_uno)


    def update(self):
        super().update()
        if self.inicio:    
            self.temporizador_aliado += self.reloj.get_time()
            self.temporizador_enemigo += self.reloj.get_time()
            self.temporizador_trampa += self.reloj.get_time()
            self.temporizador_item += self.reloj.get_time()
                            
            if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 3:
                self.generar_aliado()
                self.temporizador_aliado = 0

            if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
                self.generar_enemigo()
                self.temporizador_enemigo = 0

            if self.temporizador_trampa >= self.tiempo_trampa and len(self.trampas) < 3:
                self.generar_trampas()
                self.temporizador_trampa = 0

            if self.temporizador_item >= self.tiempo_item and len(self.items)< 1:
                self.generar_item()
                self.temporizador_item = 0

class survival(nivel):
    def __init__(self,textos, sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_enemigo = 0
        self.temporizador_trampa = 0
        self.tiempo_enemigo = 1000
        self.tiempo_trampa = 2000

        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)
        self.intro(mensaje_survival,"comenzar")
        

    def intro(self,mensaje_survival,mensaje:str):
        super().intro(mensaje)
        texto_uno = Imprimir(ANCHO//4,300,28,mensaje_survival,BLANCO)
        self.textos.add(texto_uno)


    def update(self):
        super().update()
        if self.inicio:    
            self.temporizador_enemigo += self.reloj.get_time()
            self.temporizador_trampa += self.reloj.get_time()
                            

            if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
                self.generar_enemigo()
                self.temporizador_enemigo = 0

            if self.temporizador_trampa >= self.tiempo_trampa and len(self.trampas) < 3:
                self.generar_trampas()
                self.temporizador_trampa = 0


class demo(nivel):
    def __init__(self, textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos,pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_aliado = 0
        self.tiempo_aliado = 2000
        self.pts_nivel_uno= pts_nivel_uno
        self.pts_nivel_dos= pts_nivel_dos
        self.pts_nivel_tres= pts_nivel_tres
        self.pts_survival = pts_survival
        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)
        self.intro(pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival)

    def menu_config(self):
        opcion_1 = Imprimir(ANCHO//3,300,28,"1. Reset score nivel 1",BLANCO)
        opcion_2 = Imprimir(ANCHO//3,350,28,"2. Reset score nivel 2",BLANCO)
        opcion_3 = Imprimir(ANCHO//3,400,28,"3. Reset score nivel 3",BLANCO)
        opcion_4 = Imprimir(ANCHO//3,450,28,"4. Reset score Survival",BLANCO)
        audio_1 = Imprimir(ANCHO//3,500,28,"0%",BLANCO)
        audio_2 = Imprimir((ANCHO//3)+50,500,28,"20%",BLANCO)
        audio_3 = Imprimir((ANCHO//3)+100,500,28,"40%",BLANCO)
        audio_4 = Imprimir((ANCHO//3)+150,500,28,"60%",BLANCO)
        audio_5 = Imprimir((ANCHO//3)+200,500,28,"80%",BLANCO)
        audio_6 =Imprimir((ANCHO//3)+250,500,28,"100%",BLANCO)

        play = Imprimir(ANCHO//3,450+100,28,"volver",BLANCO)
        self.textos.add(opcion_1,opcion_2,opcion_3,audio_1,audio_2,audio_3,audio_4,audio_5,audio_6,play,opcion_4)    
        

    def intro(self,pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival):
        titulo = Imprimir(((ANCHO//2-100)),int(200),int(28)," Menu Principal",BLANCO) #cambiar mensaje con metodo tipo menu ->str
        opcion_1 = Imprimir(ANCHO//3,300,28,"1. Nivel 1",BLANCO)
        opcion_2 = Imprimir(ANCHO//3,350,28,"2. Nivel 2",BLANCO)
        opcion_3 = Imprimir(ANCHO//3,400,28,"3. Nivel 3",BLANCO)
        opcion_4 = Imprimir(ANCHO//3,450,28,"4.Survival",BLANCO)
        opcion_5 = Imprimir(ANCHO//3,500,28,"5.Ranking",BLANCO)
        opcion_6 = Imprimir(ANCHO//3,550,28,"6.Configuracion",BLANCO)

        if pts_nivel_uno :
            nivel_uno = Imprimir((ANCHO//3)+120,300,28,str(pts_nivel_uno),(74,135,69))
            self.textos.add(nivel_uno)
        if pts_nivel_dos :
            nivel_dos = Imprimir((ANCHO//3)+120,350,28,str(pts_nivel_dos),(74,135,69))
            self.textos.add(nivel_dos)
        if pts_nivel_tres :
            nivel_tres = Imprimir((ANCHO//3)+120,400,28,str(pts_nivel_tres),(74,135,69))
            self.textos.add(nivel_tres)
        if pts_survival:
            survival = Imprimir((ANCHO//3)+120,450,28,str(pts_survival),(74,135,69))
            self.textos.add(survival)
        self.textos.add(titulo,opcion_1,opcion_2,opcion_3,opcion_4,opcion_5,opcion_6)

    def terminar_nivel(self):
        for plataforma in self.plataformas:
            plataforma.kill()
        for trampa in self.trampas:
            trampa.kill()
        for particula in self.particulas:
            particula.kill()
        for laser in self.lasers_aliados:
            laser.kill()
        for laser in self.lasers_enemigos:
            laser.kill()
        for aliado in self.aliados:
            aliado.kill()
        for enemigo in self.enemigos:
            enemigo.kill()
        for item in self.items:
            item.kill()
        self.textos.empty()

        self.inicio = False
        
    def update(self):
        for enemigo in self.enemigos:
            if enemigo.rect.left > ANCHO:
                enemigo.kill()
            else:
                lista = pygame.sprite.spritecollide(enemigo, self.aliados, True)
                if lista:
                    enemigo.kill()
                    self.enemigos_muertos += 1
                    
                coliciono = pygame.sprite.spritecollideany(enemigo, self.plataformas)
                if coliciono:
                    enemigo.que_hace = "camina"                    
                    if enemigo.rect.x < 900 and enemigo.disparos_hechos < 4:
                        enemigo.que_hace = "dispara"
                        enemigo.dispara(self.sprites,self.lasers_enemigos,self.enemigos)
                    else: enemigo.que_hace = "camina"
                else:
                    enemigo.que_hace = "cae"


        for aliado in self.aliados:
            if aliado.rect.left > ANCHO:
                aliado.kill()
            else:
                lista = pygame.sprite.spritecollide(aliado,self.enemigos,True)
                if lista: 
                    aliado.kill()
                    self.aliados_muertos += 1

                coliciono = pygame.sprite.spritecollideany(aliado,self.plataformas)
                if coliciono:
                    aliado.que_hace = "camina"
                    if aliado.rect.x > 400 and aliado.disparos_hechos < 8:
                        aliado.que_hace = "dispara"
                        aliado.dispara(self.sprites, self.lasers_aliados, self.enemigos)
                    else: aliado.que_hace = "camina"
                else: aliado.que_hace = "cae"

        for laser in self.lasers_aliados:
            lista =  pygame.sprite.spritecollide(laser,self.enemigos,False)
            for enemigo in lista:
                enemigo.que_hace = "muerto"
                laser.que_hace = "explota"
                self.enemigos_muertos += 1
                self.puntos.sumar_puntos(66)

        for laser in self.lasers_enemigos:
            lista =  pygame.sprite.spritecollide(laser,self.aliados,False)
            for aliado in lista:
                aliado.que_hace = "muerto"
                laser.que_hace = "explota"
                self.aliados_muertos += 1



        for plataforma in self.plataformas:
            for laser in self.lasers_enemigos:
                if laser.rect.colliderect(plataforma):
                    laser.que_hace = "explota"
                        
                else:
                    lista = pygame.sprite.spritecollide(laser,self.aliados,False)
                    if len(lista) != 0:
                        laser.que_hace = "explota"
                            
            for laser in self.lasers_aliados:
                if laser.rect.colliderect(plataforma):
                    laser.que_hace = "explota"


        self.temporizador_aliado += self.reloj.get_time()

        if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 1:
            self.generar_aliado()
            self.temporizador_aliado = 0


class rank(nivel):
    def __init__(self, textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos,ranking:Ranking,
                 pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival):
        super().__init__(textos,sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_aliado = 0
        self.tiempo_aliado = 2000

        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)
        self.ranking = ranking
        self.score = None
        self.intro(pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival)
    def mostrar_ranking(self,lista:list,espaciado,tam_fuente,color):
        self.textos.empty()
        puesto_1 = Imprimir(ANCHO//3,300 + 1 * espaciado, tam_fuente,f"{lista[0]}",color)
        puesto_2 = Imprimir(ANCHO//3,300 + 2 * espaciado, tam_fuente,f"{lista[1]}",color)         
        puesto_3 = Imprimir(ANCHO//3,300 + 3 * espaciado, tam_fuente,f"{lista[2]}",color)
        puesto_4 = Imprimir(ANCHO//3,300 + 4 * espaciado, tam_fuente,f"{lista[3]}",color)
        puesto_5 = Imprimir(ANCHO//3,300 + 5 * espaciado, tam_fuente,f"{lista[4]}",color)
        volver = Imprimir(ANCHO//2,450,28,"volver",BLANCO)
        self.textos.add(puesto_1,puesto_2,puesto_3,puesto_4,puesto_5,volver)
        

    def intro(self,pts_nivel_uno,pts_nivel_dos,pts_nivel_tres,pts_survival):
        titulo = Imprimir(((ANCHO//2-100)),int(200),int(28),"Ranking",BLANCO) 
        if pts_nivel_uno != None and pts_nivel_dos != None and pts_nivel_tres != None:
            resultado = pts_nivel_uno + pts_nivel_dos + pts_nivel_tres
            self.score = resultado
            texto = Imprimir(ANCHO//4,300,28,"Completaste todos los niveles",BLANCO)
            texto_2 = Imprimir(ANCHO//4,350,28,"podes cargar tu resultado:",BLANCO)
            texto_3 = Imprimir(ANCHO//4,400,28,f"{resultado}",BLANCO)
            texto_4 = Imprimir(ANCHO//4,450,28,"aceptar",BLANCO)
            texto_5 = Imprimir(ANCHO//2,450,28,"volver",BLANCO)
            self.textos.add(texto,texto_2,texto_3,texto_4,texto_5)
        else:
            texto = Imprimir(ANCHO//3,300,28,"todavia no completo todos los niveles",BLANCO)
            texto_2 = Imprimir(ANCHO//4,450,28,"aceptar",BLANCO)
            texto_3 = Imprimir(ANCHO - 500,450,28,"volver",BLANCO)
            self.textos.add(texto,texto_2,texto_3)
        self.textos.add(titulo)

    def ingresar_puntaje(self,nombre:str):
        pass

    def terminar_nivel(self):
        for plataforma in self.plataformas:
            plataforma.kill()
        for trampa in self.trampas:
            trampa.kill()
        for particula in self.particulas:
            particula.kill()
        for laser in self.lasers_aliados:
            laser.kill()
        for laser in self.lasers_enemigos:
            laser.kill()
        for aliado in self.aliados:
            aliado.kill()
        for enemigo in self.enemigos:
            enemigo.kill()
        for item in self.items:
            item.kill()
        self.textos.empty()

        self.inicio = False
        

    def update(self):
        for enemigo in self.enemigos:
            if enemigo.rect.left > ANCHO:
                enemigo.kill()
            else:
                lista = pygame.sprite.spritecollide(enemigo, self.aliados, True)
                if lista:
                    enemigo.kill()
                    self.enemigos_muertos += 1
                    
                coliciono = pygame.sprite.spritecollideany(enemigo, self.plataformas)
                if coliciono:
                    enemigo.que_hace = "camina"                    
                    if enemigo.rect.x < 900 and enemigo.disparos_hechos < 4:
                        enemigo.que_hace = "dispara"
                        enemigo.dispara(self.sprites,self.lasers_enemigos,self.enemigos)
                    else: enemigo.que_hace = "camina"
                else:
                    enemigo.que_hace = "cae"


        for aliado in self.aliados:
            if aliado.rect.left > ANCHO:
                aliado.kill()
            else:
                lista = pygame.sprite.spritecollide(aliado,self.enemigos,True)
                if lista: 
                    aliado.kill()
                    self.aliados_muertos += 1

                coliciono = pygame.sprite.spritecollideany(aliado,self.plataformas)
                if coliciono:
                    aliado.que_hace = "camina"
                    if aliado.rect.x > 400 and aliado.disparos_hechos < 6:
                        aliado.que_hace = "dispara"
                        aliado.dispara(self.sprites, self.lasers_aliados, self.enemigos)
                    else: aliado.que_hace = "camina"
                else: aliado.que_hace = "cae"

        for laser in self.lasers_aliados:
            lista =  pygame.sprite.spritecollide(laser,self.enemigos,False)
            for enemigo in lista:
                enemigo.que_hace = "muerto"
                laser.que_hace = "explota"
                self.enemigos_muertos += 1
                self.puntos.sumar_puntos(66)

        for laser in self.lasers_enemigos:
            lista =  pygame.sprite.spritecollide(laser,self.aliados,False)
            for aliado in lista:
                aliado.que_hace = "muerto"
                laser.que_hace = "explota"
                self.aliados_muertos += 1



        for plataforma in self.plataformas:
            for laser in self.lasers_enemigos:
                if laser.rect.colliderect(plataforma):
                    laser.que_hace = "explota"
                        
                else:
                    lista = pygame.sprite.spritecollide(laser,self.aliados,False)
                    if len(lista) != 0:
                        laser.que_hace = "explota"
                            
            for laser in self.lasers_aliados:
                if laser.rect.colliderect(plataforma):
                    laser.que_hace = "explota"


        self.temporizador_aliado += self.reloj.get_time()

        if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 1:
            self.generar_aliado()
            self.temporizador_aliado = 0