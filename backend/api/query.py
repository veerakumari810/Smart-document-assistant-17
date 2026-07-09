from fastapi import APIRouter
from pydantic import BaseModel
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
            return {"answer": "Please enter a valid question.", "response": "Please enter a valid question.", "text": "Please enter a valid question."}

        # 1. FAISS ఇండెక్స్ లోడ్ చేయడం
        index_loaded = vector_store.load_index()
        if not index_loaded:
            msg = "No active document found in pipeline. Please upload a PDF first."
            return {"answer": msg, "response": msg, "text": msg, "result": msg}

        # 2. ఎంబెడ్డింగ్ అండ్ వెక్టార్ సెర్చ్
        query_embedding = embed_service.get_embeddings([question])
        distances, indices = vector_store.index.search(query_embedding, k=3)
        
        context = []
        for idx in indices[0]:
            if idx != -1 and idx < len(vector_store.chunks):
                context.append(vector_store.chunks[idx])

        if not context:
            msg = "I could not find any relevant information in the uploaded document."
            return {"answer": msg, "response": msg, "text": msg, "result": msg}

        # 3. లోకల్ Qwen 2.5 కి పంపి ఆన్సర్ తెప్పించడం
        answer = llm_service.generate_answer(question, context)
        print(f"[BACKEND LOG] Generated Answer Successfully!")
        
        # ఫ్రంటెండ్ ఏ కీ వెతికినా దొరికేలా అన్నింటినీ పంపుతున్నాం
        return {
            "answer": answer,
            "response": answer,
            "text": answer,
            "output": answer,
            "result": answer
        }

    except Exception as e:
        err_msg = f"Backend Error processing your request: {str(e)}"
        return {"answer": err_msg, "response": err_msg, "text": err_msg, "result": err_msg}