from flask import Flask, request, render_template
from src.processing.PreparadorRAG import ChunkBuilder
from src.client.APIClient import API
from PyPDF2 import PdfReader
import markdown
import traceback

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/info_formulario", methods=["POST"])
def buscador():
    """
    Función que obtiene el prompt y el fichero y realiza dicha consulta sobre el fichero.
    Si no encuentra la información en el fichero, se lo hace saber al usuario.
    """
    prompt = request.form.get("user_message")
    fichero = request.files.get("archivo")

    if not prompt or not fichero:
        return render_template(
            "index.html",
            error=True,
            info="Por favor inserte una consulta y un fichero.",
        )
    try:
        contenido = leer_contenido_fichero(fichero)  # sacar el texto del fichero

        # Se encarga de todas las funciones de chunks
        chunk_builder = ChunkBuilder(contenido, prompt)
        contexto = chunk_builder.top_chunks()

        # Se encarga de hacer la consulta a chatgpt
        api = API(contexto, prompt)
        respuesta_api = api.consulta()
        respuesta_html = markdown.markdown(
            respuesta_api, extensions=["tables", "fenced_code"]
        )

        return render_template("index.html", mensaje=respuesta_html, error=False)
    except Exception:
        print(traceback.format_exc())
        return render_template(
            "index.html", error=True, info="Error procesando el fichero o la consulta."
        )


@app.route("/resumen", methods=["POST"])
def resumir_fichero():
    """
    Función que se encarga de resumir el fichero obtenido.
    """

    fichero = request.files.get("archivo")

    if not fichero:
        return render_template(
            "index.html",
            error=True,
            info="Por favor inserte un fichero.",
        )

    try:
        contenido = leer_contenido_fichero(fichero)  # leer como texto

        # Se encarga de hacer la consulta a chatgpt
        api = API(contenido)
        respuesta_api = api.resumen()
        respuesta_html = markdown.markdown(
            respuesta_api, extensions=["tables", "fenced_code"]
        )

        return render_template("index.html", mensaje=respuesta_html, error=False)
    except Exception:
        print(traceback.format_exc())
        return render_template(
            "index.html", error=True, info="Error procesando el fichero o la consulta."
        )


def leer_contenido_fichero(fichero):
    """
    Función que se encarga de obtener el texto de los ficheros.
    """
    nombre = fichero.filename.lower()
    if nombre.endswith(".txt"):
        return fichero.read().decode("utf-8")

    elif nombre.endswith(".pdf"):
        lector = PdfReader(fichero)
        numero_de_paginas = len(lector.pages)

        # Itera sobre cada página y extrae el texto
        texto_completo = ""
        for numero_pagina in range(numero_de_paginas):
            pagina = lector.pages[numero_pagina]
            texto_pagina = pagina.extract_text()
            texto_completo += f"--- Página {numero_pagina + 1} ---\n"
            texto_completo += texto_pagina + "\n"
            if texto_pagina:
                texto_completo += texto_pagina + "\n"

        return texto_completo
    else:
        raise ValueError("Extensión de fichero no válida. Solo se permiten .txt o .pdf")


if __name__ == "__main__":
    app.run(debug=True)
