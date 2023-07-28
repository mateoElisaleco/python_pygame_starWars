import pygame
#from nave import nave


DISPARO_TIEMPO = 400

ROJO = pygame.color.Color(255,0,0)  
AZUL = pygame.color.Color(0,0,255)
VERDE = pygame.color.Color(0,255,0)
NEGRO = pygame.color.Color(0,0,0)
BLANCO = pygame.color.Color(255,255,255)
TRANSPARENTE = pygame.color.Color(0,0,0,0)

TAMAÑO_NAVE = (61,41)


FPS = 15

ANCHO = 1366

ALTO = 768

PANTALLA = (ANCHO,ALTO)
VEL_TRAMPA = 12
velocidad = 17
GRAVEDAD = 4

gravedad = True

#bomba
x_inicial = ANCHO // 2
y_inicial = ALTO //2


def girar_imagenes(lista_original:list,giro_x:bool,giro_y:bool):
    lista_girada = []

    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen,giro_x,giro_y))
        
    return lista_girada


nave_bomba = [pygame.image.load("./sprites/nave/bomba/16.png"),
              pygame.image.load("./sprites/nave/bomba/17.png")]


nave_inicio = [pygame.image.load("./sprites/nave/inicio/14.png"), pygame.image.load("./sprites/nave/inicio/15.png")]

nave_bomba = [pygame.image.load("./sprites/nave/bomba/16.png"),pygame.image.load("./sprites/nave/bomba/17.png")]    

nave_movimiento_izquierda =[pygame.image.load("./sprites/nave/movimiento/12.png"),pygame.image.load("./sprites/nave/movimiento/13.png")]  

nave_movimiento_derecha = girar_imagenes(nave_movimiento_izquierda,True,False)

nave_muere = [pygame.image.load("./sprites/nave/muere/8.png"),
                  pygame.image.load("./sprites/nave/muere/9.png"),
                  pygame.image.load("./sprites/nave/muere/10.png"),
                  pygame.image.load("./sprites/nave/muere/11.png")
                  ]

nave_particulas_izquierda =  [pygame.image.load("./sprites/nave/particulas/7.png"),
                        pygame.image.load("./sprites/nave/particulas/6.png"),
                        pygame.image.load("./sprites/nave/particulas/5.png"),
                        pygame.image.load("./sprites/nave/particulas/4.png"),
                        pygame.image.load("./sprites/nave/particulas/3.png"),
                        pygame.image.load("./sprites/nave/particulas/2.png"),
                        pygame.image.load("./sprites/nave/particulas/1.png"),
                        pygame.image.load("./sprites/nave/particulas/0.png")
                        ]   

nave_particulas_derecha = girar_imagenes(nave_particulas_izquierda,True,False)

lista_animaciones_nave = [nave_inicio,nave_bomba,nave_movimiento_izquierda,nave_muere,nave_particulas_derecha,nave_movimiento_derecha,nave_particulas_izquierda]

rectangulo_nave = nave_inicio[0].get_rect()
rectangulo_nave.x = x_inicial
rectangulo_nave.y = y_inicial

pos_inicial = (x_inicial, y_inicial)


droide_vuela = [pygame.image.load("./sprites/droide/vuela/1.png"),
                  pygame.image.load("./sprites/droide/vuela/2.png"),
                  pygame.image.load("./sprites/droide/vuela/3.png")
                  ]

droide_camina = [pygame.image.load("./sprites/droide/camina/4.png"),
                  pygame.image.load("./sprites/droide/camina/5.png"),
                  pygame.image.load("./sprites/droide/camina/6.png"),
                  pygame.image.load("./sprites/droide/camina/7.png"),
                  pygame.image.load("./sprites/droide/camina/8.png"),
                  pygame.image.load("./sprites/droide/camina/9.png")
                  ]

droide_dispara = [pygame.image.load("./sprites/droide/dispara/10.png"),
                  pygame.image.load("./sprites/droide/dispara/11.png"),
                  pygame.image.load("./sprites/droide/dispara/12.png"),
                  pygame.image.load("./sprites/droide/dispara/13.png"),
                  pygame.image.load("./sprites/droide/dispara/14.png"),
                  pygame.image.load("./sprites/droide/dispara/15.png"),
                  pygame.image.load("./sprites/droide/dispara/16.png"),
                  pygame.image.load("./sprites/droide/dispara/17.png")
                  ]

droide_escudo = [pygame.image.load("./sprites/droide/escudo/18.png"),
                  pygame.image.load("./sprites/droide/escudo/19.png"),
                  pygame.image.load("./sprites/droide/escudo/20.png"),
                  pygame.image.load("./sprites/droide/escudo/21.png"),
                  pygame.image.load("./sprites/droide/escudo/22.png"),
                  pygame.image.load("./sprites/droide/escudo/23.png")
                  ]

droide_muere = [  pygame.image.load("./sprites/droide/muere/24.png"),
                  pygame.image.load("./sprites/droide/muere/25.png"),
                  pygame.image.load("./sprites/droide/muere/26.png"),
                  pygame.image.load("./sprites/droide/muere/27.png"),
                  pygame.image.load("./sprites/droide/muere/28.png"),
                  pygame.image.load("./sprites/droide/muere/29.png"),
                  pygame.image.load("./sprites/droide/muere/30.png"),
                  pygame.image.load("./sprites/droide/muere/31.png"),
                  pygame.image.load("./sprites/droide/muere/32.png"),
                  pygame.image.load("./sprites/droide/muere/33.png"),
                  pygame.image.load("./sprites/droide/muere/34.png"),
                  pygame.image.load("./sprites/droide/muere/35.png")
                  ]

lista_animaciones_droide = [droide_camina,droide_dispara,droide_muere]

lista_animaciones_especiales_droide = [droide_vuela,droide_escudo]

clon_camina = [pygame.image.load("./sprites/clon/camina/0.png"),
               pygame.image.load("./sprites/clon/camina/1.png"),
               pygame.image.load("./sprites/clon/camina/2.png"),
               pygame.image.load("./sprites/clon/camina/3.png"),
                pygame.image.load("./sprites/clon/camina/4.png"),
                pygame.image.load("./sprites/clon/camina/5.png"),
                pygame.image.load("./sprites/clon/camina/6.png")]

clon_dispara = [pygame.image.load("./sprites/clon/dispara/6.png"),
                pygame.image.load("./sprites/clon/dispara/7.png"),
                pygame.image.load("./sprites/clon/dispara/8.png")]

clon_muere = [pygame.image.load("./sprites/clon/muere/14.png"),
              pygame.image.load("./sprites/clon/muere/15.png"),
              pygame.image.load("./sprites/clon/muere/16.png"),
              pygame.image.load("./sprites/clon/muere/17.png"),
              pygame.image.load("./sprites/clon/muere/18.png"),
              pygame.image.load("./sprites/clon/muere/19.png"),
              pygame.image.load("./sprites/clon/muere/20.png"),
              pygame.image.load("./sprites/clon/muere/21.png"),]

lista_animaciones_clon = [clon_camina,clon_dispara,clon_muere]


laser_azul = pygame.image.load("./sprites/miscelaneos/laser_azul/22.png")

laser_azul_explota = [pygame.image.load("./sprites/miscelaneos/laser_azul/explota/26.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/28.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/30.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/32.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/34.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/36.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/38.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_azul/explota/40.png")]

lista_animaciones_laser_azul = [laser_azul,laser_azul_explota]

laser_rojo = pygame.image.load("./sprites/miscelaneos/laser_rojo/24.png")

laser_rojo_explota = [pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/25.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/27.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/29.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/31.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/33.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/35.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/37.png"),
                      pygame.image.load("./sprites/miscelaneos/laser_rojo/explota/39.png")]

lista_animaciones_laser_rojo = [laser_rojo,laser_rojo_explota]
