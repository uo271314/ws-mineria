# DNI: 15508581A: noticias no negacionistas.
import json, random
from simhash import Simhash, SimhashIndex

# Selección de las noticias.
no_negacionistas = list()
with open("../noticias.ndjson", "r", encoding="utf-8") as noticias:
  contenido = noticias.readlines()
  for i in range(len(contenido)):
    try:
      data = json.loads(contenido[i])
      if len(data["sentencias_disagree"])<len(data["sentencias_NOT_disagree"]):
        texto = " ".join(data["sentencias"])
        texto = "".join(texto.splitlines())
        no_negacionistas.append({
          "pos": i,
          "noticia": texto
        })
    except Exception as e:
      pass

print("Número de noticias: " + str(len(contenido)))
print("Número de noticias no negacionistas: " + str(len(no_negacionistas)))

# Eliminación de documentos cuasi-duplicados.
firmas = []
tam_firma_simhash = 128

# Creación de firmas por documento.
for i in range(len(no_negacionistas)):
  texto = no_negacionistas[i]["noticia"]
  firma = Simhash(texto, f=tam_firma_simhash)
  firmas.append((i,firma)) 
    
# Creación de un índice con las firmas.
indice = SimhashIndex(firmas, k=10, f=tam_firma_simhash)

# Filtrado de los documentos.
no_negacionistas_filtrados = list()
duplicados = list()

for i in range(len(no_negacionistas)):
  if i not in duplicados:
    noticia = no_negacionistas[i]
    firma = firmas[i][1]
    doc_duplicados = indice.get_near_dups(firma)

    if len(doc_duplicados)==1:
      no_negacionistas_filtrados.append(noticia)
      duplicados.append(i)
    else:
      random.shuffle(doc_duplicados)
      pos_duplicado_seleccionado = int(doc_duplicados[0])
      no_negacionistas_filtrados.append(no_negacionistas[pos_duplicado_seleccionado])
      for pos_duplicado in doc_duplicados:
        duplicados.append(int(pos_duplicado))

no_negacionistas_sin_cuasi_duplicados = list(map(lambda noticia: 
  contenido[noticia["pos"]], no_negacionistas_filtrados))

with open("noticias_sin_cuasi_duplicados.ndjson", "w", encoding="utf-8") as writer:
  for line in no_negacionistas_sin_cuasi_duplicados:
    writer.write(line)
print("Número de noticias no negacionistas sin cuasi-duplicados: " + str(len(no_negacionistas_filtrados)))