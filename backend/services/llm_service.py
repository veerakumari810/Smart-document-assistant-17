import requests

class QwenLLMService:
    def __init__(self):
        # Local Ollama API URL
        self.api_url = "http://127.0.0.1:11434/api/generate"

    def generate_answer(self, question: str, context: list) -> str:
        """
        Takes the document context and user question, sends it to Ollama Qwen model,
        and returns the generated response.
        """
        context_str = "\n---\n".join(context)
        
        prompt = f"""You are a helpful AI Assistant. Answer the user question strictly using the provided document context.
If the answer is not in the context, say "I cannot find the answer in the document."

Context:
{context_str}

Question: {question}
Answer:"""

        payload = {
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # 🌟 timeout ని 180 సెకన్లకు పెంచాం (3 నిమిషాలు)
            response = requests.post(self.api_url, json=payload, timeout=180)
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Ollama Server Error: Status Code {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Error: Ollama Model took too long to respond (Read Timeout)."
        except Exception as e:
            return f"❌ EXACT_NETWORK_ERROR_IS: {str(e)}"