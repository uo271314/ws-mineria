# DNI: 15508581A: otra colección - noticias negacionistas.
import json, random

counter = 0
with open("./noticias_negacionistas_etiquetadas.ndjson", "r", encoding="utf-8") as noticias_etiquetadas:
    with open("./etiquetado_manual/noticias_seleccionadas.txt", "w", encoding="utf-8") as writer:
        with open("./etiquetado_manual/noticias_a_etiquetar.txt", "w", encoding="utf-8") as manual_writer:
            noticias = noticias_etiquetadas.readlines()
            random.shuffle(noticias)
            for noticia in noticias[:10]:
                writer.write(noticia)

                noticia = json.loads(noticia)
                counter += 1
                texto = " ".join(noticia["sentencias"])
                texto = "".join(texto.splitlines())
                manual_writer.write("Noticia " + str(counter) + ": " + noticia["headline"] + "\n")
                manual_writer.write(texto + "\n\n")