class Entry: # guarda los atributos de key (palabra) y definition (definicion)
    def __init__(self, key, definition):
        self.key = key
        self.definition = definition

class HashTable:
    def __init__(self, size=101):  # tamaño primo por eficiencia que debe re ajustarse para evitar coliciones 
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key): #funcion hash que suma unicode de cada carater de la key y saca el modulo de el tamaño de la tabla
        #print(sum(ord(char) for char in key) % self.size)

        return sum(ord(char) for char in key) % self.size
    

    def insert(self, key, definition):

        index = self.hash_function(key)



        # Si ya existe, actualiza
        for entry in self.table[index]:

            if entry.key == key:

                entry.definition = definition

                return
            
        self.table[index].append(Entry(key, definition)) # si no existe se agrega


        print(self.table)

    def search(self, key): #busqueda hash
        index = self.hash_function(key) # saca hash
        for entry in self.table[index]: #Busca en las listas encadenadas (si hubo coliciones)

            if entry.key == key:

                return entry.definition
        return None

    def delete(self, key):

        index = self.hash_function(key)


        for i, entry in enumerate(self.table[index]):

            if entry.key == key:
                del self.table[index][i]
                return True
            
        return False

    def display(self):

        for i, bucket in enumerate(self.table):

            if bucket:
                
                print(f"Índice {i}: {[f'{e.key} -> {e.definition}' for e in bucket]}")

    def keys(self):
        """Devuelve una lista de todas las claves almacenadas en la tabla hash."""
        claves = []
        for bucket in self.table:
            for entry in bucket:
                claves.append(entry.key)
        return claves

    def items(self):
        """Devuelve una lista de tuplas (clave, definición) de todas las entradas."""
        elementos = []
        for bucket in self.table:
            for entry in bucket:
                elementos.append((entry.key, entry.definition))
        return elementos