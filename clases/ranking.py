import pygame,json,sqlite3
from imprimir import Imprimir

class Ranking():
    def __init__(self,ruta:str,textos:pygame.sprite.Group):
        self.ruta = ruta
        self.textos = textos
        self.conexion = sqlite3.connect(ruta)
        self.cursor = self.conexion.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rankings (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                puntos INTEGER
            )
        """)

    
        self.conexion.commit()

   
        self.ranking = []#

    def agregar_puntaje(self, nombre, puntos):
        self.cursor.execute("INSERT INTO rankings (nombre, puntos) VALUES (?, ?)", (nombre, puntos))
        self.conexion.commit()

    def cargar_ranking(self, limit=5):
        self.cursor.execute("SELECT nombre, puntos FROM rankings ORDER BY puntos DESC LIMIT ?", (limit,)) 
        rankings = self.cursor.fetchall()
        
        return rankings

    def cargar_valores_predeterminados(self):
        if self.cargar_ranking() == []:
            valores_predeterminados = [
                ("obi wan",777),
                ("mace windu",1000),
                ("anakin",666),
                ("r2d2",20000),
                ("palpatine",66)
                ]
            self.cursor.executemany("INSERT INTO rankings (id,nombre, puntos) VALUES (?,?,?)",valores_predeterminados)
            self.conexion.commit() 

    def close_connection(self):
        self.conexion.close()

    def ordenar(self):
        n = len(self.ranking)
        for i in range(n-1):
            for j in range(n-1-i):
                if self.ranking[j]["puntos"] < self.ranking[j+1]["puntos"]:
                    self.ranking[j], self.ranking[j + 1] = self.ranking[j + 1], self.ranking[j]
                    
    def update(self, x, y, espaciado):
        for i in range(len(self.ranking)):
            item = self.ranking[i]
            texto = Imprimir(x,y + i * espaciado,28,f'{item["nombre"]}: {item["puntos"]}', (255, 255, 255))
            self.textos.add(texto)



