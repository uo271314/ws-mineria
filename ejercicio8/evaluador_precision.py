# DNI: 15508581A: otra colección - noticias negacionistas.
import json

# Etiquetado de aciertos y fallos por etiqueta.
aciertos_por_etiqueta = {
    "incendios": 0,
    "calentamiento": 0,
    "emisiones": 0,
    "deshielo": 0,
    "activismo": 0,
    "combustibles": 0,
    "sequia": 0,
    "energiasrenovables": 0,
    "futuro": 0,
    "hidrogeno": 0,
    "efectoinvernadero": 0,
    "oladecalor": 0,
    "offtopic": 0
}
fallos_por_etiqueta = aciertos_por_etiqueta.copy()

with open("./etiquetado_manual/noticias_seleccionadas.txt", "r", encoding="utf-8") as noticias_etiquetadas:
    with open("./etiquetado_manual/etiquetado_manual.txt", "r", encoding="utf-8") as etiquetado_manual:
        noticias = noticias_etiquetadas.readlines()
        manual = etiquetado_manual.readlines()[4:]
        manual = list(filter(lambda etiq: etiq != "\n" and not etiq.startswith("Noticia "), manual))

        for i in range(len(noticias)):
            etiquetas_automaticas = list(json.loads(noticias[i])["etiquetas"].keys())
            etiquetas_manuales = manual[i].strip().split(" ")

            etiq_manuales_faltan = etiquetas_manuales.copy()
            for etiq in etiquetas_automaticas:
                if etiq in etiquetas_manuales:
                    aciertos_por_etiqueta[etiq] += 1
                    etiq_manuales_faltan.remove(etiq)
                else:
                    fallos_por_etiqueta[etiq] += 1

            for etiq in etiq_manuales_faltan:
                fallos_por_etiqueta[etiq] += 1


with open("./precision_clasificador.txt", "w", encoding="utf-8") as writer:
    precisiones = list()
    writer.write("Precisión por etiqueta:\n")
    for etiq in list(aciertos_por_etiqueta.keys()):
        try:
            precision = round(aciertos_por_etiqueta[etiq] / (aciertos_por_etiqueta[etiq] + fallos_por_etiqueta[etiq]), 2)
            precisiones.append(precision)
        except:
            precision = "Sin probar"
        writer.write("\t- Etiqueta '" + etiq + "': " + str(precision) + "\n")


    writer.write("\n")
    writer.write("Precisión total: " + str(sum(precisiones)/len(precisiones)))
    