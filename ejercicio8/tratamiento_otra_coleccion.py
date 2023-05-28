# DNI: 15508581A: otra colección - noticias negacionistas.
import json
import spacy, nltk
nltk.download("stopwords")

from nltk.tokenize import TextTilingTokenizer
from nltk.corpus import stopwords

# Carga del core de spaCy en español.
nlp = spacy.load("es_core_news_sm")

# Selección de las noticias.
noticias_negacionistas_segmentadas = list()
vinculo_noticias = list()

with open("../noticias.ndjson", "r", encoding="utf-8") as noticias:
    contenido = noticias.readlines()
    for linea in contenido:
        try:
            data = json.loads(linea)
            if len(data["sentencias_disagree"])>len(data["sentencias_NOT_disagree"]):
                texto = " ".join(data["sentencias"])
                texto = "".join(texto.splitlines())
                # Segmentación en sentencias con spaCy.
                sentencias = "\n\n".join([sent.text for sent in nlp(texto).sents])

                # Segmentación por temáticas coherentes con TextTiling.
                palabras_vacias = set(stopwords.words("spanish"))
                tt = TextTilingTokenizer(stopwords=palabras_vacias)
                segmentacion = list(map(lambda s: s.replace("\n\n", " ").strip(), tt.tokenize(sentencias)))

                # Creación de una lista única para predecir con fasttext.
                pos_inicio = len(noticias_negacionistas_segmentadas)
                data["pos_inicio"] = pos_inicio
                data["pos_final"] = pos_inicio + len(segmentacion) - 1
                vinculo_noticias.append(data)
                noticias_negacionistas_segmentadas.extend(segmentacion)

        except Exception as e:
            pass

with open("./tratamiento/vinculo_noticias_segmentos_negacionistas.txt", "w", encoding="utf-8") as writer:
    for linea in vinculo_noticias:
        writer.write(json.dumps(linea, ensure_ascii=False) + "\n")

with open("./tratamiento/segmentos_negacionistas_a_predecir.txt", "w", encoding="utf-8") as writer:
    for linea in noticias_negacionistas_segmentadas:
        writer.write(linea + "\n")