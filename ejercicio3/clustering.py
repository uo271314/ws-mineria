# DNI: 15508581A: noticias no negacionistas.
import spacy, random, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Carga del core de spaCy en español.
nlp = spacy.load("es_core_news_sm")
palabras_vacias = list(spacy.lang.es.stop_words.STOP_WORDS)

with open("../ejercicio2/noticias_segmentadas.txt", "r", encoding="utf-8") as segmentos:
    contenido = list(filter(lambda s: s != "\n", segmentos.readlines()))
    contenido = list(map(lambda s: s.strip(), contenido))
    
    # Vectorización de los segmentos con scikit-learn.
    vectorizador = TfidfVectorizer(encoding="utf-8", lowercase=True,
                               stop_words=palabras_vacias, ngram_range=(1,3), 
                               max_features=10000)
    matriz_corpus = vectorizador.fit_transform(contenido)

    # Clustering con k-means.
    clustering = KMeans(n_clusters=25, init='k-means++', max_iter=1000, n_init=1, verbose=True)
    clustering.fit(matriz_corpus)

    segmentos_clusterizados = dict()
    segmentos_por_cluster = dict()

    for i in range(len(clustering.labels_)):
        try:
            segmentos_clusterizados[clustering.labels_[i]].append(i)
            segmentos_por_cluster[clustering.labels_[i]]+=1
        except:
            segmentos_clusterizados[clustering.labels_[i]] = list()
            segmentos_clusterizados[clustering.labels_[i]].append(i)
            segmentos_por_cluster[clustering.labels_[i]]=1

    ids = list(segmentos_por_cluster.keys())
    ids.sort()
    segmentos_por_cluster_ordenados = {i: segmentos_por_cluster[i] for i in ids}

    # Traducción de los segmentos.
    contenido_segmentos = vectorizador.get_feature_names_out()

    cluster_centers = clustering.cluster_centers_
    indice_cluster_segmentos = cluster_centers.argsort()[:, ::-1]

    # Escritura de los clusters.
    data = []
    with open("clusters.txt", "w", encoding="utf-8") as writer:
        for cluster_id in segmentos_por_cluster_ordenados:
            writer.write("Cluster %d (%d documentos): " % (cluster_id, segmentos_por_cluster[cluster_id]))

            cluster_keywords = []
            for term_id in indice_cluster_segmentos[cluster_id, :10]:
                if cluster_centers[cluster_id][term_id]!=0:
                    writer.write('"%s" ' % contenido_segmentos[term_id])
                    cluster_keywords.append(contenido_segmentos[term_id])
            writer.write("\n")

            cluster_contenido = []
            resultados = segmentos_clusterizados[cluster_id]
            random.shuffle(resultados)
            counter = 0
            for resultado in resultados:
                if(counter < 5):
                    counter += 1
                    writer.write("\t" + contenido[resultado][0:140] + "...\n")
                cluster_contenido.append(contenido[resultado])
            writer.write("\n\n")

            data.append({
                "cluster": cluster_id,
                "keywords": cluster_keywords,
                "contenido": cluster_contenido
            })

        with open("clusters_pickle", "wb") as archivo_pickle:
            pickle.dump(data, archivo_pickle)