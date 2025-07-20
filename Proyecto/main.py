#SOLO ES UNA PRUEBA

from Hash import HashTable



diccionario = HashTable()

# Insertar palabras
diccionario.insert("perro", "Animal doméstico de cuatro patas.")
diccionario.insert("errop", "Felino doméstico que maúlla.")
diccionario.insert("pato", "Ave acuática que hace cuac.")

# Buscar una palabra
print("Buscar 'gato':", diccionario.search("gato"))

# Mostrar toda la tabla
print("\nDiccionario actual:")
diccionario.display()

# Eliminar una palabra
diccionario.delete("pato")
print("\nDespués de eliminar 'pato':")
diccionario.display()