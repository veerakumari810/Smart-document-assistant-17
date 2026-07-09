import requests

class QwenLLMService:
    def __init__(self):
        # ఇక్కడ మళ్లీ 127.0.0.1 పెట్టి చూద్దాం, ఎందుకంటే ఎర్రర్ మెసేజ్ క్లియర్ గా వస్తుంది
        self.api_url = "http://127.0.0.1:11434/api/generate"

    def generate_answer(self, question: str, context: list) -> str:
        context_str = "\n---\n".join(context)
        prompt = f"Context:\n{context_str}\n\nQuestion: {question}\nAnswer:"
        payload = {"model": "qwen2.5:3b", "prompt": prompt, "stream": False}
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Ollama Server Error: Status Code {response.status_code}"
        except Exception as e:
            # 🌟 ఇక్కడ మనం 'Smart Document Assistant' టెక్స్ట్ ని పంపట్లేదు!
            # కేవలం అసలైన ఎర్రర్ ఏంటో మాత్రమే స్క్రీన్ మీద చూపిస్తున్నాం.
            return f"❌ EXACT_NETWORK_ERROR_IS: {str(e)}"