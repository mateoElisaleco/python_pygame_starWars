import pygame,puntaje,random,item
from config import ANCHO,ALTO,lista_animaciones_droide,lista_animaciones_clon,lista_animaciones_especiales_droide
from trampa import droide_aereo
from plataforma import Plataforma
from enemigo import Enemigo
from aliado import Aliado
class nivel():
    def __init__(self,sprites:pygame.sprite.Group,plataformas:pygame.sprite.Group,particulas:pygame.sprite.Group,trampas:pygame.sprite.Group,
                 lasers_aliados:pygame.sprite.Group,lasers_enemigos:pygame.sprite.Group,aliados:pygame.sprite.Group,enemigos:pygame.sprite.Group,
                 items:pygame.sprite.Group,reloj:pygame.time.Clock,enemigos_muertos:int,aliados_muertos:int,puntos:puntaje) -> None:
        
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

        self.puntos = puntos

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
        

    def status_nivel(self,bajas_aliados:int,bajas_enemigos:int,objetivos:bool):

        retorno = 0
        if objetivos:
            if self.enemigos_muertos >= bajas_enemigos:
                retorno = 1
            if self.aliados_muertos >= bajas_aliados:
                retorno = -1
        return retorno

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
        print(self.aliados_muertos)
        #print(self.enemigos_muertos)

                    
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
        
        obj = item("./sprites/nave/inicio/14.png",(40,30),(int(random.uniform(20,ANCHO-20)),int(random.uniform(500,20))))
        self.sprites.add(obj)
        self.items.add(obj)

                

class nivel1(nivel):
    def __init__(self, sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
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
        

    def update(self):
        super().update() 
        self.temporizador_aliado += self.reloj.get_time()
        self.temporizador_enemigo += self.reloj.get_time()
                        
        if self.temporizador_aliado >= self.tiempo_aliado and len(self.aliados)< 3:
            self.generar_aliado()
            self.temporizador_aliado = 0

        if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
            self.generar_enemigo()
            self.temporizador_enemigo = 0


class nivel2(nivel):
    def __init__(self, sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
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



    def update(self):
        super().update() 
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
    def __init__(self, sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
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



    def update(self):
        super().update() 
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
    def __init__(self, sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                 aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos):
        super().__init__(sprites, plataformas, particulas, trampas, lasers_aliados, lasers_enemigos,
                         aliados, enemigos, items,reloj,enemigos_muertos,aliados_muertos,puntos)
        self.temporizador_enemigo = 0
        self.temporizador_trampa = 0
        self.tiempo_enemigo = 1000
        self.tiempo_trampa = 2000

        self.piso = Plataforma("./imagenes/JUEGUITO MATU_piso.png",(ANCHO,80),(ANCHO//2,ALTO-40))
        self.sprites.add(self.piso)
        self.plataformas.add(self.piso)



    def update(self):
        super().update() 
        self.temporizador_enemigo += self.reloj.get_time()
        self.temporizador_trampa += self.reloj.get_time()
                        

        if self.temporizador_enemigo >= self.tiempo_enemigo and len(self.enemigos)< 4:
            self.generar_enemigo()
            self.temporizador_enemigo = 0

        if self.temporizador_trampa >= self.tiempo_trampa and len(self.trampas) < 3:
            self.generar_trampas()
            self.temporizador_trampa = 0

