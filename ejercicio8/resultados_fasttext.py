# DNI: 15508581A: otra colección - noticias negacionistas.
import json

with open("./fasttext/segmentos_negacionistas_tematicas_fasttext.txt", "r", encoding="utf-16") as tematicas_fasttext:
    with open("./tratamiento/vinculo_noticias_segmentos_negacionistas.txt", "r", encoding="utf-8") as vinculo_noticias:
        with open("./noticias_negacionistas_etiquetadas.ndjson", "w", encoding="utf-8") as writer:
            tematicas = tematicas_fasttext.readlines()
            tematicas = list(map(lambda t: t.strip().replace("__label__", ""), tematicas))
            vinculo = vinculo_noticias.readlines()

            for noticia in vinculo:
                noticia = json.loads(noticia)
                etiquetas = list()
                frecuencias_etiquetas = dict()
                for i in range(noticia["pos_inicio"], noticia["pos_final"]+1):
                    etiquetas.append(tematicas[i])
                for etiq in set(etiquetas):
                    frecuencias_etiquetas[etiq] = round(etiquetas.count(etiq)/len(etiquetas), 2)

                del noticia["pos_inicio"]
                del noticia["pos_final"]
                noticia["etiquetas"] = frecuencias_etiquetas
                writer.write(json.dumps(noticia, ensure_ascii=False) + "\n")
