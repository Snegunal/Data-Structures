class Entry:
    def __init__(self, key, definition):
        self.key = key
        self.definition = definition


class Nodo:
    def __init__(self, entry):
        self.entry = entry
        self.siguiente = None


class ListaEnlazada: #Lista para manejar colisiones
    def __init__(self):
        self.cabeza = None

    def insertar(self, key, definition):
        actual = self.cabeza
        
        while actual:

            if actual.entry.key == key:

                actual.entry.definition = definition  # Actualiza si ya existe

                return
            
            actual = actual.siguiente

        nuevo_nodo = Nodo(Entry(key, definition))

        nuevo_nodo.siguiente = self.cabeza  # Inserta al inicio

        self.cabeza = nuevo_nodo

    def buscar(self, key):
        actual = self.cabeza
        while actual:

            if actual.entry.key == key:
                return actual.entry.definition
            
            actual = actual.siguiente
        return None

    def eliminar(self, key):
        actual = self.cabeza
        anterior = None

        while actual:
            if actual.entry.key == key:

                if anterior:

                    anterior.siguiente = actual.siguiente
                    
                else:
                    self.cabeza = actual.siguiente
                return True
            anterior = actual

            actual = actual.siguiente
        return False

    def obtener_todos(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append((actual.entry.key, actual.entry.definition))
            actual = actual.siguiente
        return elementos


class HashTable:
    def __init__(self, size=101): #inicia la tabla hash con "size" tamaño 

        self.size = size

        self.table = [ListaEnlazada() for _ in range(size)]

    def hash_function(self, key): # funcion hash que suma los Unicode de cada caracter y sca el modulo con el tamaño de la tabla

        return sum(ord(char) for char in key) % self.size

    def insert(self, key, definition): #inserta un dato en la tabla hash y resuelve la colision añadiendo a la lista enlazada

        index = self.hash_function(key)

        self.table[index].insertar(key, definition)

    def search(self, key): #busca la llave en la tabla hash

        index = self.hash_function(key)


        return self.table[index].buscar(key)

    def delete(self, key): # Elimina una entrada del diccionario

        index = self.hash_function(key)

        return self.table[index].eliminar(key)

    def display(self): #imprime en consola contenido de la tabla hash

        for i, lista in enumerate(self.table):

            elementos = lista.obtener_todos()

            if elementos:

                print(f"Índice {i}: {[f'{k} -> {d}' for k, d in elementos]}")

    def keys(self): #devuelve una lista de todas las claves almacenadas
        claves = []


        for lista in self.table:

            claves.extend([k for k, _ in lista.obtener_todos()])

        return claves

    def items(self): #devuelve tuplas de forma (entrada,definicion)
        elementos = []
        for lista in self.table:
            elementos.extend(lista.obtener_todos())
        return elementos
