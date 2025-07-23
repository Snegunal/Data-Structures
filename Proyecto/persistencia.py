import json
import os

def guardar_diccionario(path, table, grafo):
    data = {}
    for palabra in table.keys():
        data[palabra] = {
            "definicion": table.search(palabra),
            "relaciones": grafo.vecinos(palabra)
        }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cargar_diccionario(path, table, grafo, trie):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for palabra, contenido in data.items():
        definicion = contenido["definicion"]
        relaciones = contenido.get("relaciones", [])

        table.insert(palabra, definicion)
        trie.insert(palabra, definicion)
        for rel in relaciones:
            grafo.agregar_relacion(palabra, rel)
