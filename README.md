# 🧠 RAG con Flask – Buscador Inteligente

Este proyecto implementa un sistema de **RAG (Retrieval-Augmented Generation)** desarrollado con **Flask** como interfaz web.  
El objetivo es permitir al usuario cargar un documento y realizar preguntas sobre su contenido, obteniendo respuestas precisas gracias a la combinación de búsqueda semántica y modelos de lenguaje.

---

## 📌 ¿Qué es un RAG?
Un **RAG (Retrieval-Augmented Generation)** es una arquitectura que combina:
1. **Recuperación de información** → Se buscan fragmentos relevantes en un conjunto de documentos (chunks) utilizando embeddings y métricas de similitud.  
2. **Generación de texto** → Esos fragmentos recuperados se utilizan como **contexto adicional** para un modelo de lenguaje (LLM), lo que permite obtener respuestas más precisas, fundamentadas en datos externos.  

En pocas palabras: el RAG conecta documentos con un LLM, de forma que el modelo responde en base a la información del documento y no solo con lo que sabe.

---

## ⚙️ Funcionalidad del proyecto
La aplicación funciona mediante un **formulario web** en el que el usuario:
1. Introduce un **prompt/pregunta**.
2. Carga un fichero en formato **.txt** o **.pdf**.

El sistema realiza los siguientes pasos:
- **Chunking con solapamiento (overlap):**  
  El documento se divide en fragmentos de tamaño fijo (chunks), con cierto solapamiento para evitar pérdida de contexto entre fragmentos contiguos.
- **Embeddings:**  
  Se calculan embeddings tanto de los chunks como del prompt.
- **Búsqueda semántica (similaridad coseno):**  
  Se determina qué chunks son más similares a la consulta del usuario.
- **Selección de contexto (Top-k):**  
  Se seleccionan los chunks más relevantes y se concatenan.
- **Consulta al LLM vía API:**  
  El prompt original + los chunks relevantes se pasan como contexto al modelo de lenguaje.  
  - Si el modelo no encuentra la respuesta en el documento, se le indica que debe informar al usuario de ello.

---

## 🖥️ Interfaz
- La aplicación cuenta con un **frontend en Flask** con un formulario sencillo e intuitivo.
- Tras enviar la consulta, se muestra en pantalla la respuesta generada por el LLM.  
- También se gestionan los errores de entrada (por ejemplo, falta de archivo o extensión no válida).

---

## 🛠️ Tecnologías utilizadas
- **Backend:** Flask (Python)
- **Procesamiento de texto:** Chunking con overlap, embeddings
- **Similitud:** Distancia coseno
- **Modelo de lenguaje:** LLM accesible mediante API
- **Frontend:** Formularios HTML renderizados con Jinja2 (plantillas de Flask)
- **Formatos soportados:** `.txt` y `.pdf`
