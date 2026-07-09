import os
from fastapi import APIRouter, UploadFile, File
from services.pdf_loader import PDFLoaderService
from services.text_splitter import TextSplitterService
from services.embeddings import EmbeddingService
from services.vector_store import FAISSVectorStore

router = APIRouter()
embed_service = EmbeddingService()
vector_store = FAISSVectorStore()

UPLOAD_DIR = "database/uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🌟 అప్‌లోడ్ అయిన డాక్యుమెంట్ టెక్స్ట్‌ని తాత్కాలికంగా దాచడానికి గ్లోబల్ వేరియబుల్
LATEST_TEXT = ""

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global LATEST_TEXT
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 1. Save File to local database/uploads
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    # 2. Extract Text
    extracted_text = PDFLoaderService.extract_text(file_path)
    LATEST_TEXT = extracted_text  # 🌟 ఇక్కడ టెక్స్ట్‌ని వేరియబుల్‌లో సేవ్ చేస్తున్నాం
    
    # 3. Create Chunks
    chunks = TextSplitterService.split_text(extracted_text)
    
    # 4. Generate Embeddings & Save to FAISS
    if chunks:
        embeddings = embed_service.get_embeddings(chunks)
        vector_store.add_documents(chunks, embeddings)
        
    return {
        "status": "success",
        "filename": file.filename,
        "chunks_processed": len(chunks)
    }