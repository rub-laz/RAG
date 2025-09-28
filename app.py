from flask import Flask, request, render_template
from src.processing.PreparadorRAG import ChunkBuilder
from src.client.APIClient import API
from PyPDF2 import PdfReader
import markdown

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/info_formulario", methods=["POST"])
def buscador():
    prompt = request.form.get("user_message")
    fichero = request.files.get("archivo")

    if not prompt or not fichero:
        return render_template(
            "index.html",
            error=True,
            info="Por favor inserte una consulta y un fichero.",
        )

    if fichero.filename.endswith(".txt"):
        contenido = fichero.read().decode("utf-8")  # leer como texto

        # Se encarga de todas las funciones de chunks
        chunk_builder = ChunkBuilder(contenido, prompt)
        contexto = chunk_builder.top_chunks()

        # Se encarga de hacer la consulta a chatgpt
        api = API(prompt, contexto)
        respuesta_api = api.consulta()
        respuesta_html = markdown.markdown(
            respuesta_api, extensions=["tables", "fenced_code"]
        )

        return render_template("index.html", mensaje=respuesta_html, error=False)
    elif fichero.filename.endswith(".pdf"):
        try:

            lector = PdfReader(fichero)
            numero_de_paginas = len(lector.pages)

            # 7. Itera sobre cada página y extrae el texto
            texto_completo = ""
            for numero_pagina in range(numero_de_paginas):
                pagina = lector.pages[numero_pagina]
                texto_pagina = pagina.extract_text()
                texto_completo += f"--- Página {numero_pagina + 1} ---\n"
                texto_completo += texto_pagina + "\n"
                if texto_pagina:
                    texto_completo += texto_pagina + "\n"

            # 8. Imprime el texto extraído de todo el PDF
            chunk_builder = ChunkBuilder(texto_completo, prompt)
            contexto = chunk_builder.top_chunks()

            # Se encarga de hacer la consulta a chatgpt
            api = API(prompt, contexto)
            respuesta_api = api.consulta()
            respuesta_html = markdown.markdown(
                respuesta_api, extensions=["tables", "fenced_code"]
            )

            return render_template("index.html", mensaje=respuesta_html, error=False)
        except Exception as e:
            return render_template(
                "index.html", error=True, info="El fichero no ha podido leerse."
            )

    else:
        return render_template(
            "index.html", error=True, info="La extensión del fichero no es válida"
        )


if __name__ == "__main__":
    app.run(debug=True)
