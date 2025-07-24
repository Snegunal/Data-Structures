class Grafo:
    def __init__(self):
        # Diccionario que representa las listas de adyacencia
        # Cada clave es una palabra y su valor es una lista de palabras relacionadas
        self.adyacencia = {}

    def agregar_relacion(self, palabra1, palabra2):
        # Si la palabra no existe en el grafo, se crea con una lista vacía
        if palabra1 not in self.adyacencia:
            self.adyacencia[palabra1] = []
        if palabra2 not in self.adyacencia:
            self.adyacencia[palabra2] = []
        if palabra2 not in self.adyacencia[palabra1]:
            self.adyacencia[palabra1].append(palabra2)
        if palabra1 not in self.adyacencia[palabra2]:
            self.adyacencia[palabra2].append(palabra1)

    def vecinos(self, palabra):
        # Devuelve la lista de palabras relacionadas con la dada
        # Si la palabra no existe, retorna una lista vacía
        print(self.adyacencia.get(palabra, []))
    
        return self.adyacencia.get(palabra, [])

    
    def eliminar_palabra(self, palabra):
        # Elimina las conexiones desde la palabra
        if palabra in self.adyacencia:
            del self.adyacencia[palabra]

        # Elimina las conexiones hacia la palabra
        for vecinos in self.adyacencia.values():
            if palabra in vecinos:
                vecinos.remove(palabra)

