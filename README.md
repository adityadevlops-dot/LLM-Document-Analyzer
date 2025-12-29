# 📄 LLM Document Analyzer

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)

An **AI-powered document analysis tool** that allows users to upload PDFs, DOCX, or TXT files and ask questions in natural language.  
Built with **Streamlit**, **FAISS**, and **SentenceTransformers**, it uses **LLMs** for context-aware answers.

---

## 🚀 Features

- 📁 Upload multiple **PDF, DOCX, or TXT files**  
- ✂ Automatic **text extraction & chunking**  
- ⚡ **Vector search** with FAISS for fast semantic retrieval  
- 🤖 **Ask questions** directly from the documents  
- 🖥 Clean **Streamlit interface**  
- 🗂 Chat history & expandable answers  
- 🧹 Clear all files & history with one click  

---

## 🧠 Architecture

Document → Text Extraction → Chunking → Embeddings → FAISS Vector Store
↓
Question → Semantic Search → LLM Answer


---

## 🛠 Tech Stack

- **Python 3.12**  
- **Streamlit** – Frontend  
- **FAISS** – Vector search  
- **Sentence-Transformers** – Embeddings  
- **pypdf / python-docx** – Document parsing  
- **AI Pipe / OpenRouter / OpenAI API** – LLM for answers  

---

## 🏗 Installation

1. Clone the repo:
```bash
git clone https://github.com/aditya2488/LLM-Document-Analyzer.git
cd LLM-Document-Analyzer

2.Create a virtual environment and activate:
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3.install dependencies:
pip install -r requirements.txt

4.Add your LLM API key in .env
OPENAI_API_KEY=<your_api_key_here>

▶ Usage

Run the Streamlit app:

streamlit run app.py


Steps:

Upload your PDF, DOCX, or TXT files via sidebar

Wait for the document(s) to process

Type your question in the input box

Click Ask to get answers

View chat history in expandable sections


🧑‍💻 Author
Aditya – Developed as a resume-ready project using modern NLP and LLM tools.

