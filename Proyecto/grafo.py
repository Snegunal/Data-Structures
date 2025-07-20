class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_relacion(self, palabra1, palabra2):
        if palabra1 not in self.adyacencia:
            self.adyacencia[palabra1] = []
        if palabra2 not in self.adyacencia:
            self.adyacencia[palabra2] = []
        if palabra2 not in self.adyacencia[palabra1]:
            self.adyacencia[palabra1].append(palabra2)
        if palabra1 not in self.adyacencia[palabra2]:
            self.adyacencia[palabra2].append(palabra1)

    def vecinos(self, palabra):
        return self.adyacencia.get(palabra, [])
