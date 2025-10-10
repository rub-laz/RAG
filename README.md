# 🧠 RAG con Flask – Buscador y Resumen Inteligente

Este proyecto implementa un sistema de **RAG (Retrieval-Augmented Generation)** desarrollado con **Flask** como interfaz web.  
El objetivo es permitir al usuario **cargar un documento y realizar preguntas sobre su contenido** o **generar un resumen automático**, aprovechando la combinación de **búsqueda semántica**, **procesamiento de lenguaje natural** y **modelos de lenguaje (LLM)**.

---

## 📌 ¿Qué es un RAG?

Un **RAG (Retrieval-Augmented Generation)** es una arquitectura que combina:

1. **Recuperación de información (Retrieval)** → Se buscan fragmentos relevantes en un conjunto de documentos (chunks) mediante embeddings y métricas de similitud.  
2. **Generación de texto (Generation)** → Los fragmentos recuperados se utilizan como **contexto adicional** para un modelo de lenguaje (LLM), que produce una respuesta fundamentada en la información del documento.

En pocas palabras: el RAG **permite que un modelo de lenguaje responda basándose en tus documentos**, no solo en su conocimiento interno.

---

## ⚙️ Funcionalidades del proyecto

La aplicación cuenta con **dos funcionalidades principales** accesibles desde la interfaz web:

### 🧩 1. Buscador inteligente

El usuario puede:

1. Escribir una **pregunta o consulta (prompt)**.  
2. Cargar un **documento en formato `.txt` o `.pdf`**.

El sistema realiza los siguientes pasos:

- **División en chunks (fragmentos) con solapamiento (overlap):**  
  El texto se divide para facilitar la búsqueda de información relevante sin perder contexto.
- **Generación de embeddings:**  
  Se crean representaciones vectoriales tanto de los chunks como de la pregunta del usuario.
- **Búsqueda semántica (similaridad coseno):**  
  Se identifican los fragmentos más similares al prompt.
- **Selección de contexto (Top-k):**  
  Se concatenan los fragmentos más relevantes.
- **Consulta al LLM vía API:**  
  El modelo recibe el contexto + el prompt, y genera una respuesta fundamentada.  
  Si la respuesta no está en el documento, el modelo debe informar de ello.

---

### 📝 2. Resumen automático de documentos

La nueva funcionalidad permite **resumir textos extensos** (en `.txt` o `.pdf`), incluso aquellos con más de **80 000 palabras**.

El proceso es el siguiente:

1. Se divide el documento en **chunks grandes** (p. ej., 10 000 palabras con solapamiento).  
2. Cada chunk se resume individualmente mediante el modelo de lenguaje.  
3. Los resúmenes parciales se combinan y se realiza un **meta-resumen global** que sintetiza toda la información manteniendo coherencia y eliminando redundancias.

De esta forma, el usuario obtiene un **resumen completo, coherente y compacto** incluso para documentos extensos.

---

## 🖥️ Interfaz

- La aplicación cuenta con un **frontend simple y limpio en Flask**, con dos formularios:
  - 🧠 Uno para **consultas y preguntas** sobre el contenido.
  - 📝 Otro para **resumir el documento completo**.
- Las respuestas y resúmenes se muestran en formato **Markdown renderizado**, permitiendo listas, tablas o fragmentos de código.
- Se gestionan los errores de forma clara (archivos no válidos, formato incorrecto, etc.).

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Flask (Python)  
- **Procesamiento de texto:** Chunking con overlap, embeddings semánticos  
- **Similitud:** Distancia coseno  
- **Modelos de lenguaje:** LLMs accesibles mediante API (por ejemplo, `openai/gpt-oss-20b:free`)  
- **Frontend:** Formularios HTML con plantillas Jinja2  
- **Lectura de documentos:** PyPDF2 para PDFs, lectura directa para TXT  
- **Markdown rendering:** Librería `markdown` de Python  
- **Formatos soportados:** `.txt` y `.pdf`

