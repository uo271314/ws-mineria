# DNI: 15508581A: noticias no negacionistas.
import json
import spacy, nltk
nltk.download("stopwords")

from nltk.tokenize import TextTilingTokenizer
from nltk.corpus import stopwords

# Carga del core de spaCy en español.
nlp = spacy.load("es_core_news_sm")
noticias_segmentadas = []
vinculo_noticias = []

with open("../ejercicio1/noticias_sin_cuasi_duplicados.ndjson", "r", encoding="utf-8") as noticias:
    contenido = noticias.readlines()
    for linea in contenido:
        try:
            data = json.loads(linea)
            texto = " ".join(data["sentencias"])
            texto = "".join(texto.splitlines())
            # Segmentación en sentencias con spaCy.
            sentencias = "\n\n".join([sent.text for sent in nlp(texto).sents])

            # Segmentación por temáticas coherentes con TextTiling.
            palabras_vacias = set(stopwords.words("spanish"))
            tt = TextTilingTokenizer(stopwords=palabras_vacias)
            segmentacion = list(map(lambda s: s.replace("\n\n", " ").strip(), tt.tokenize(sentencias)))

            # Creación de una lista única.
            pos_inicio = len(noticias_segmentadas)
            vinculo_noticias.append({
                "identificador": data["identifier"],
                "pos_inicio": pos_inicio,
                "pos_final": pos_inicio + len(segmentacion) - 1
            })
            noticias_segmentadas.extend(segmentacion)

        except Exception as e:
            pass

with open("noticias_segmentadas.txt", "w", encoding="utf-8") as writer:
  for line in noticias_segmentadas:
    writer.write(line + "\n\n")

with open("noticias_segmentadas_vinculadas.txt", "w", encoding="utf-8") as writer:
  for line in vinculo_noticias:
    writer.write(json.dumps(line) + "\n")