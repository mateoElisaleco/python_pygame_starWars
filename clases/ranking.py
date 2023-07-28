import pygame,json


class Ranking():
    def __init__(self,ruta:str):
        self.ruta = ruta
        self.ranking = []
        self.cargar_ranking()

    def cargar_ranking(self):
        with open(self.ruta) as archivo:
            self.ranking = json.load(archivo)

    def guardar_ranking(self):
        with open(self.ruta,"w") as archivo:
            json.dump(self.ranking,archivo)

    def agregar_puntaje(self,nombre,puntos):
        self.ranking.append({"nombre":nombre, "puntos":puntos})

    def ordenar(self):
        n = len(self.ranking)
        for i in range(n-1):
            for j in range(n-1-i):
                if self.ranking[j]["puntos"] < self.ranking[j+1]["puntos"]:
                    self.ranking[j], self.ranking[j + 1] = self.ranking[j + 1], self.ranking[j]
                    
    def update(self, display, fuente, x, y, espaciado):
        for i in range(len(self.ranking)):
            item = self.ranking[i]
            texto = fuente.render(f'{item["nombre"]}: {item["puntos"]}', True, (255, 255, 255))
            display.blit(texto, (x, y + i * espaciado))

