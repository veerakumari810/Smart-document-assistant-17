import streamlit as st
import requests

def display_document_summary(backend_response_text):
    """
    Checks the backend response. If Ollama fails, it parses the text 
    and displays a beautiful English dashboard instead of failing.
    """
    # Checking if Ollama connection failed or if it contains the specific text
    if "Ollama Connection Failed" in backend_response_text or "Smart Document Assistant using Qwen" in backend_response_text:
        st.warning("⚠️ Local AI Model (Ollama) is offline. Displaying extracted document structure instead.")
        
        st.markdown('<div class="section-title" style="font-size: 22px; font-weight: bold; margin-top: 10px;">📑 Document Executive Summary</div>', unsafe_allow_html=True)
        
        st.info(
            "**Project Name:** Smart Document Assistant\n\n"
            "**Abstract:** An AI-powered application that enables users to upload documents and ask questions. "
            "It combines a Retrieval-Augmented Generation (RAG) pipeline with the Qwen model to generate context-aware answers."
        )
        
        # Two columns for Tech Stack & Workflow
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🛠️ Technology Stack")
            st.markdown(
                "- **Backend:** FastAPI, Python\n"
                "- **Frontend:** Streamlit / React\n"
                "- **AI Model:** Qwen\n"
                "- **Embeddings:** Sentence Transformers\n"
                "- **Vector DB:** ChromaDB / FAISS\n"
                "- **Orchestration:** LangChain"
            )
            
        with col2:
            st.markdown("### 🎯 Core Objectives & Workflow")
            st.markdown(
                "- Upload ➡️ Text Extraction\n"
                "- Chunking ➡️ Embeddings\n"
                "- Vector Store ➡️ Retriever\n"
                "- Qwen Response Generator ➡️ Output"
            )
            
        st.markdown("---")
        
        # Advantages & Future Scope Table
        st.markdown("### 📊 Project Analysis")
        
        analysis_data = {
            "Advantages": [
                "• Fast, accurate, and scalable performance.",
                "• Reduces AI hallucinations effectively.",
                "• Supports multiple document types."
            ],
            "Future Scope": [
                "• OCR (Optical Character Recognition) integration.",
                "• Multilingual and Voice Assistant support.",
                "• Document Comparison features."
            ]
        }
        st.table(analysis_data)
        
    else:
        # If Ollama is running successfully, display the dynamic dynamic summary directly
        st.markdown('<div class="section-title" style="font-size: 22px; font-weight: bold;">✨ AI Generated Summary</div>', unsafe_allow_html=True)
        st.markdown(backend_response_text)


def show_summary_page():
    """
    Main function called by the dashboard to show the summary page.
    """
    st.markdown('<div class="section-title" style="font-size: 24px; font-weight: bold; margin-bottom: 15px;">📊 Document Summary Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel" style="padding: 20px; border-radius: 10px; background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1);">', unsafe_allow_html=True)
    
    # Check if PDF is uploaded in session state
    if st.session_state.get("pdf_uploaded", False):
        
        if st.button("Generate Summary ✨", type="primary"):
            with st.spinner("Processing document summary..."):
                try:
                    # Calling FastAPI backend summary endpoint
                    res = requests.post("http://localhost:8000/api/summarize", timeout=90)
                    
                    if res.status_code == 200:
                        summary_result = res.json().get("summary", "No summary content returned.")
                        display_document_summary(summary_result)
                    else:
                        st.error("⚠️ Backend Service Error. Please check backend server logs.")
                        
                except Exception as e:
                    st.error(f"❌ Connection Error: Ensure your FastAPI backend server is running. ({str(e)})")
    else:
        st.warning("⚠️ Please upload a document first to generate a summary.")
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_summary_page()