# Smart-document-assistant-17
# 🤖 Smart Document Assistant

An AI-powered Smart Document Assistant that enables users to upload documents, ask questions, summarize content, extract text from images, translate text, and interact with documents using Retrieval-Augmented Generation (RAG) and Small Language Models.

---

## 📌 Project Overview

Smart Document Assistant is an intelligent document processing system that helps users understand and analyze documents using Artificial Intelligence.

The application supports:

- 📄 PDF Upload
- 📁 Document Management
- 💬 AI Chat with Documents
- 📝 Document Summarization
- ✂️ OCR Text Extraction
- 🌐 Multi-language Translation
- 🖼️ Image Processing
- 📷 Camera OCR
- 🔐 User Login & Registration

---

## 🚀 Features

- Secure Login & Registration
- Interactive Dashboard
- Upload PDF Documents
- AI-powered Question Answering
- Retrieval-Augmented Generation (RAG)
- FAISS Vector Database
- OCR for Images
- Document Summarization
- Text Translation
- Image Upload Support
- Camera Capture Support
- Modern Streamlit UI

---

## 🛠️ Technologies Used

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- FastAPI
- Python

### AI & Machine Learning
- Qwen 2.5
- Sentence Transformers
- FAISS
- LangChain
- Hugging Face Transformers

### OCR
- EasyOCR
- Tesseract OCR

---

## 📂 Project Structure

```
smart-document-assistant/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── style.css
│   └── chat_history.json
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── database/
│   ├── uploads/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ System Architecture

```
User
   │
   ▼
Frontend (Streamlit)
   │
   ▼
FastAPI Backend
   │
   ├── Upload API
   ├── Query API
   ├── OCR API
   ├── Translation API
   └── Summary API
          │
          ▼
Retriever (FAISS)
          │
          ▼
Embeddings
          │
          ▼
Qwen Small Language Model
          │
          ▼
Generated Response
```

---

## 🔄 Workflow

1. User Login
2. Upload Document
3. Text Extraction
4. Text Chunking
5. Embedding Generation
6. Store in FAISS
7. Ask Question
8. Retrieve Relevant Chunks
9. Generate AI Response
10. Display Answer

---

## 📸 Modules

- Dashboard
- My Documents
- AI Chat
- Summarize
- Extract Text
- Translate
- Image
- Camera

---

## ▶️ Installation

### Clone Repository

```bash
git clone https://github.com/veerakumari810/Smart-document-assistant-17.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
cd backend
uvicorn main:app --reload
```

### Run Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 📈 Future Enhancements

- LoRA Fine-tuned Chatbot
- Voice Assistant
- Chat History
- Multi-document Chat
- Cloud Deployment
- Mobile Application

---

## 👩‍💻 Developer

**Achanta Veera Kumari**

Final Year B.Tech (Artificial Intelligence & Data Science)

---

## 📜 License

This project is developed for educational and academic purposes.
