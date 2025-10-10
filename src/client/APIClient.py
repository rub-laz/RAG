import requests
import json
import time
from ..processing.PreparadorRAG import ChunkBuilder


class API:
    def __init__(self, contexto, prompt=None):
        self.contexto = contexto
        self.prompt = prompt
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = "api"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def consulta(self):
        """
        Función que hace la consulta a chatGPT con el prompt y los chunks en lo que podría estar la información.
        """
        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Según el texto que te voy a pasar, {self.prompt}? Si no encuentras una respuesta apropiada en el texto dime: no he encontrado la respuesta:  {self.contexto} .",
                }
            ],
        }

        # Send the request
        response = requests.post(
            self.api_url, headers=self.headers, data=json.dumps(payload)
        )

        # Handle the response
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: Request failed with status {response.status_code}"

    def resumen(self):
        """
        Función que hace el resumen de un corpus si su tamaño no excede las 80000 palabras, si no es así,
        llama a otra función para hacer chunks al corpus y realizar los resúmenes de los chunks para luego
        juntarlos y crear un metaresumen.
        """
        if len(self.contexto) < 80000:

            payload = {
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Resume el siguiente texto destacando los aspectos más importantes, {self.contexto} .",
                    },
                ],
            }

            # Send the request
            response = requests.post(
                self.api_url, headers=self.headers, data=json.dumps(payload)
            )

            # Handle the response
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: Request failed with status {response.status_code}"

        else:
            return self.meta_resumen()

    def meta_resumen(self):
        """
        Función que por cada chunk hace un resumen para luego juntarlos todos y hacer un metaresumen.
        """
        chunk_builder = ChunkBuilder(self.contexto)
        chunks = chunk_builder.chunks_resumen()
        resumenes = []
        for chunk in chunks:
            payload = {
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un experto en resumir textos",
                    },
                    {
                        "role": "user",
                        "content": f"Resume el siguiente texto, {chunk} .",
                    },
                ],
            }

            # Send the request
            response = requests.post(
                self.api_url, headers=self.headers, data=json.dumps(payload)
            )
            if response.status_code == 200:
                result = response.json()
                resumenes.append(result["choices"][0]["message"]["content"])
            else:
                return f"Error: Request failed with status {response.status_code}"

            time.sleep(5)

        texto_resumenes = "\n\n".join(resumenes)

        # CONSULTA FINAL CON TODOS LOS RESÚMENES DE LOS CHUNKS.
        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"""Estos son resúmenes parciales de un texto largo. 
                                Crea un resumen global que integre la información más importante, 
                                sin redundancias y manteniendo coherencia: {texto_resumenes} """,
                },
            ],
        }

        # Send the request
        response = requests.post(
            self.api_url, headers=self.headers, data=json.dumps(payload)
        )
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: Request failed with status {response.status_code}"
