from fastapi import APIRouter
from pydantic import BaseModel
import pickle
import os
import glob
from services.vector_store import FAISSVectorStore
from services.embeddings import EmbeddingService
from services.llm_service import QwenLLMService

router = APIRouter()
vector_store = FAISSVectorStore()
embed_service = EmbeddingService()
llm_service = QwenLLMService()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_document(request_data: QueryRequest):
    try:
        question = request_data.question
        print(f"\n[BACKEND LOG] Received Question: '{question}'")
        
        if not question:
            return {"answer": "Please enter a valid question.", "response": "Please enter a valid question."}

        # 1. FAISS ఇండెక్స్ లోడ్ చేయడం
        index_loaded = vector_store.load_index()
        if not index_loaded:
            msg = "No active document found in pipeline. Please upload a PDF first."
            return {"answer": msg, "response": msg}

        # 🌟 [CRITICAL FIX] ఒకవేళ మెమరీలో chunks లేకపోతే, మీ ప్రాజెక్ట్ ఫోల్డర్ లోని pkl ఫైల్స్ నుండి లోడ్ చేయడం
        if not hasattr(vector_store, "chunks") or not vector_store.chunks:
            print("[BACKEND LOG] Chunks missing in memory. Searching for local backup files...")
            
            # మీ ప్రాజెక్ట్ లో ఉండే అన్ని రకాల pkl ఫైల్స్ చెక్ చేస్తుంది (faiss_store.pkl, vector_store.pkl, chunks.pkl ఏదైనా సరే)
            possible_paths = ["faiss_store.pkl", "vector_store.pkl", "chunks.pkl", "services/faiss_store.pkl"]
            pkl_path = None
            
            for path in possible_paths:
                if os.path.exists(path):
                    pkl_path = path
                    break
            
            # ఒకవేళ పైన ఉన్న పేర్లు కాకుండా వేరే ఏదైనా .pkl ఫైల్ ఉంటే దాన్ని వెతుకుతుంది
            if not pkl_path:
                pkl_files = glob.glob("*.pkl")
                if pkl_files:
                    pkl_path = pkl_files[0]

            if pkl_path:
                with open(pkl_path, "rb") as f:
                    saved_data = pickle.load(f)
                    
                    # pkl ఫైల్ ఫార్మాట్ బట్టి డేటా ని ఎక్స్‌ట్రాక్ట్ చేయడం
                    if isinstance(saved_data, dict):
                        if "chunks" in saved_data:
                            vector_store.chunks = saved_data["chunks"]
                        elif "all_text_chunks" in saved_data:
                            vector_store.chunks = saved_data["all_text_chunks"]
                    elif isinstance(saved_data, list):
                        vector_store.chunks = saved_data
                        
                print(f"[BACKEND LOG] Success! Loaded {len(vector_store.chunks)} chunks safely from '{pkl_path}'.")
            else:
                print("[BACKEND LOG] ERROR: No .pkl backup file found on disk!")

        # 2. ఎంబెడ్డింగ్ అండ్ వెక్టార్ సెర్చ్
        query_embedding = embed_service.get_embeddings([question])
        distances, indices = vector_store.index.search(query_embedding, k=4) # k=4 కి పెంచాము ఎక్కువ కాంటెక్స్ట్ కోసం
        
        context = []
        if hasattr(vector_store, "chunks") and vector_store.chunks:
            for idx in indices[0]:
                if idx != -1 and idx < len(vector_store.chunks):
                    context.append(vector_store.chunks[idx])
        else:
            print("[BACKEND LOG] CRITICAL: vector_store.chunks is STILL EMPTY. Context cannot be built.")

        if not context:
            msg = "I could not find any relevant information in the uploaded document."
            return {"answer": msg, "response": msg}

        # 3. లోకల్ Qwen మోడల్ కి డేటా పంపి ఆన్సర్ తెప్పించడం
        print(f"[BACKEND LOG] Context found! Sending {len(context)} text chunks to Qwen...")
        answer = llm_service.generate_answer(question, context)
        print(f"[BACKEND LOG] Generated Answer Successfully!")
        
        return {
            "answer": answer,
            "response": answer,
            "text": answer,
            "output": answer,
            "result": answer
        }

    except Exception as e:
        err_msg = f"Backend Error processing your request: {str(e)}"
        print(f"[BACKEND LOG] EXCEPTION OCCURRED: {str(e)}")
        return {"answer": err_msg, "response": err_msg}