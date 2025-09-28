import requests
import json


class API:
    def __init__(self, prompt, contexto):
        self.prompt = prompt
        self.contexto = contexto
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = (
            "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"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def consulta(self):
        """
        Función que hace la consulta a chatGPT con el prompt y los chunks en lo que podría estar la información
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
