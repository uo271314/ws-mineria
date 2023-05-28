# DNI: 15508581A: noticias no negacionistas.
import pickle, math

# Obtención de los clusters seleccionados.
etiquetas_clusters = {
    0: "__label__incendios",
    1: "__label__calentamiento",
    5: "__label__emisiones",
    6: "__label__deshielo",
    7: "__label__activismo",
    14: "__label__combustibles",
    15: "__label__sequia",
    17: "__label__energiasrenovables",
    18: "__label__futuro",
    19: "__label__hidrogeno",
    22: "__label__efectoinvernadero",
    23: "__label__oladecalor",

    4: "__label__offtopic",
    8: "__label__offtopic",
    11: "__label__offtopic",
    12: "__label__offtopic",
    13: "__label__offtopic",
    16: "__label__offtopic",
    21: "__label__offtopic"
}

with open('../ejercicio3/clusters_pickle', 'rb') as archivo_pickle:
    clusters = pickle.load(archivo_pickle)
    clusters = list(filter(lambda c: c["cluster"] in list(etiquetas_clusters.keys()), clusters))

    # Cálculo de las proporciones de las etiquetas.
    num_offtopic = [k for k, v in etiquetas_clusters.items() if v == "__label__offtopic"]

    num_etiquetas = list(filter(lambda c: c["cluster"] not in num_offtopic, clusters))
    num_etiquetas = sum(len(c["contenido"]) for c in num_etiquetas)

    num_offtopic = list(filter(lambda c: c["cluster"] in num_offtopic, clusters))
    num_offtopic = sum(len(c["contenido"]) for c in num_offtopic)

    print("Número de segmentos etiquetados: ", num_etiquetas)
    print("Número de segmentos off-topic: ", num_offtopic)
    print("Segmentos etiquetados = {:0.2f}x segmentos off-topic.\n".format(num_etiquetas/num_offtopic))

    # Cáculo de las proporciones de entrenamiento y testing por cluster.
    contenido_por_cluster = list(map(lambda c: {
        "cluster": c["cluster"],
        "contenido": c["contenido"],
        "entrenamiento": math.trunc(len(c["contenido"]) * 0.8)
        }, clusters))

    total_entrenamiento = sum(c["entrenamiento"] for c in contenido_por_cluster)
    total_segmentos = num_etiquetas + num_offtopic
    print("Número de segmentos para entrenamiento: ", total_entrenamiento, " ({:0.2f}%)".format((total_entrenamiento*100)/total_segmentos))
    print("Número de segmentos para testing: ", total_segmentos - total_entrenamiento, " ({:0.2f}%)".format(((total_segmentos - total_entrenamiento)*100)/total_segmentos))

    with open("entrenamiento.txt", "w", encoding="utf-8") as entr_writer:
        with open("testing.txt", "w", encoding="utf-8") as test_writer:
            for cluster in contenido_por_cluster:
                for i in range(len(cluster["contenido"])):
                    clasificado = etiquetas_clusters[cluster["cluster"]] + " " + \
                        cluster["contenido"][i] + "\n"
                    if i<cluster["entrenamiento"]:
                        entr_writer.write(clasificado)
                    else:
                        test_writer.write(clasificado)

