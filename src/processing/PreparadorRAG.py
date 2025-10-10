from ..model.recommender import SentenceTransformerRecommender
import torch


class ChunkBuilder:
    def __init__(self, contenido_fichero, prompt=None):
        self.contenido_fichero = contenido_fichero
        self.prompt = prompt
        self.chunk_size = 200
        self.overlap_size = 30
        self.modelo = SentenceTransformerRecommender()

    def make_chunks(self):
        """
        Función que se encarga de hacer chunks al texto obtenido del fichero
        """
        palabras = self.contenido_fichero.split()
        chunks = []
        start = 0
        while start < len(palabras):

            end = start + self.chunk_size
            chunk = palabras[start:end]
            # Esta linea es para que meta espacios entre las palabras
            chunks.append(" ".join(chunk))
            start = end - self.overlap_size

        return chunks

    def embeddings(self):
        """
        Función que se encarga de hacer los embeddings de los chunks y del prompt
        """
        chunks = self.make_chunks()
        chunks_embeddings = []
        # Embeddings de los chunks
        for chunk in chunks:
            vector = self.modelo.encode(chunk)
            chunks_embeddings.append(vector)

        # Embedding del prompt
        prompt_embedding = self.modelo.encode(self.prompt)

        return chunks_embeddings, prompt_embedding, chunks

    def top_chunks(self):
        """
        Función que se encarga de encontrar los chunks que más se parecen al prompt y juntarlos para que chatGPT busque la respuesta.
        """
        chunks_embeddings, prompt_embedding, chunks = self.embeddings()
        x = self.modelo.similarity(prompt_embedding, chunks_embeddings)[0]
        # devuelve un tensor con los índices
        if len(x) < 3:
            top_indices = torch.topk(x, k=1).indices
        elif len(x) < 5:
            top_indices = torch.topk(x, k=3).indices
        else:
            top_indices = torch.topk(x, k=5).indices

        contexto = "\n\n".join([chunks[c] for c in top_indices])

        return contexto

    def chunks_resumen(self, chunk_size=10000, overlap=500):
        """
        Función que realiza chunks a un fichero en el caso de que su corpus sea demasiado extenso.
        """

        palabras = self.contenido_fichero.split()
        chunks = []
        i = 0
        while i < len(palabras):
            chunk = palabras[i : i + chunk_size]
            chunks.append(" ".join(chunk))
            i += chunk_size - overlap
        return chunks
