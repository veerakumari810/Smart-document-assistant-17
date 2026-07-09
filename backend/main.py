import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router
from api.query import router as query_router

# మీ ప్రాజెక్ట్ లోని వెక్టార్ స్టోర్ మరియు LLM సర్వీస్‌లను ఇంపోర్ట్ చేసుకుంటున్నాం
from services.vector_store import FAISSVectorStore
from services.llm_service import QwenLLMService

app = FastAPI(title="Smart Document Assistant Backend")

# CORS permissions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")

# సర్వీసెస్ ఇనిషియలైజేషన్
vector_store = FAISSVectorStore()
llm_service = QwenLLMService()


@app.post("/api/summarize")
async def summarize_document():
    try:
        # 1. లోకల్ డిస్క్ నుండి FAISS ఇండెక్స్ మరియు చంక్స్ ని లోడ్ చేయడం
        index_loaded = vector_store.load_index()
        
        if not index_loaded:
            return {"summary": "⚠️ FAISS ఇండెక్స్ ఫైల్ లోడ్ కాలేదు. దయచేసి మొదట ఒక PDF అప్‌లోడ్ చేయండి."}
            
        if not hasattr(vector_store, "chunks") or not vector_store.chunks:
            return {"summary": "⚠️ ఇండెక్స్ లోడ్ అయింది కానీ 'vector_store.chunks' ఖాళీగా ఉంది."}

        # 2. డాక్యుమెంట్‌లోని మొదటి 8 చంక్స్ ని తీసుకొని కాంటెక్స్ట్ బిల్డ్ చేయడం
        full_document_text = "\n".join(vector_store.chunks[:8]) 

        # 3. AI సమ్మరీ కోసం స్ట్రక్చర్డ్ ప్రాంప్ట్
        question_directive = (
            "Generate a highly structured, informative, and detailed summary based ONLY on the document text provided below. "
            "Do not give generic answers or system details. You must output the response using the following exact format:\n\n"
            "### 📌 Key Overview\n(Provide a brief introduction of what the document is about)\n\n"
            "### 📑 Main Core Topics\n* (Detailed Point 1 from document)\n* (Detailed Point 2 from document)\n\n"
            "### 💡 Critical Takeaways & Conclusion\n(Summary of final thoughts)\n\n"
            f"--- DOCUMENT CONTENT START ---\n{full_document_text}\n--- DOCUMENT CONTENT END ---"
        )

        # 4. మీ చాట్ ప్యానెల్ (api/query.py) లాగే QwenLLMService ద్వారా సమ్మరీ జనరేట్ చేయడం
        ai_response = llm_service.generate_answer(question_directive, [full_document_text])
        
        if ai_response and ai_response.strip():
            return {"summary": ai_response}
        
        return {"summary": "⚠️ LLM సర్వీస్ నుండి రెస్పాన్స్ ఖాళీగా వచ్చింది."}

    except Exception as e:
        # 🌟 పాత ఫాల్‌బ్యాక్ టెక్స్ట్ లూప్ ని పూర్తిగా బ్రేక్ చేసి, అసలైన ఎర్రర్ ని స్క్రీన్ మీదే చూపిస్తుంది
        error_message = f"❌ BACKEND EXCEPTION: {str(e)}"
        print(f"\n{error_message}\n")  # మీ టెర్మినల్ లో కూడా ప్రింట్ అవుతుంది
        return {"summary": error_message}


@app.get("/")
def read_root():
    return {"status": "FastAPI Server is running successfully!"}


# విండోస్ మల్టీప్రాసెసింగ్ క్రాష్ అవ్వకుండా ఉండటానికి సేఫ్ రన్ సెటప్
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)