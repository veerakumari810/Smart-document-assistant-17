import streamlit as st
import requests
import json
import os

# --- CONFIG & BACKEND ---
BACKEND_URL = "http://127.0.0.1:8000"
HISTORY_FILE = "chat_history.json"

st.markdown('<div class="section-title">💬 AI Deep Analysis Chat</div>', unsafe_allow_html=True)

# --- 1. History Load & Save Functions ---
def load_chat_messages():
    """కేవలం మెసేజ్ హిస్టరీని మాత్రమే లోడ్ చేస్తుంది"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "messages" in data:
                    return data["messages"]
        except:
            return []
    return []

def save_chat_messages(messages):
    """మెసేజ్‌లను సేవ్ చేస్తుంది"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)

# --- 2. Session State Initialization ---
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = load_chat_messages()

# --- 3. UI Layout & Action Buttons ---
top_col, btn_col = st.columns([6, 4])

with top_col:
    # హోమ్ పేజీ సెషన్ స్టేట్ చెక్ చేయడం
    if st.session_state.get("pdf_uploaded", False):
        filename = st.session_state.get("filename", "Document")
        pages_count = st.session_state.get("pages_count", "—")
        st.markdown(f"🎯 Loaded Document: <b style='color:#00FFFF;'>📄 {filename}</b> ({pages_count} Pages)", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Note: No active document loaded. Please upload a document on the home page first.")

with btn_col:
    b_col1, b_col2 = st.columns(2)
    
    chat_download_text = ""
    if st.session_state.chat_messages:
        for msg in st.session_state.chat_messages:
            speaker = "👤 User" if msg["role"] == "user" else "🤖 AI Assistant"
            chat_download_text += f"{speaker}:\n{msg['content']}\n\n"
            chat_download_text += "-"*50 + "\n\n"
    
    with b_col1:
        if chat_download_text:
            st.download_button(
                label="📥 Download Chat",
                data=chat_download_text,
                file_name=f"Chat_History_{st.session_state.get('filename', 'analysis')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("📥 Download Chat", disabled=True, use_container_width=True)
            
    with b_col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.chat_messages = []
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.toast("Chat history cleared! 🧹")
            st.rerun()

st.markdown("<hr style='opacity:0.15; margin:15px 0;'>", unsafe_allow_html=True)

# --- 4. Render Previous Messages ---
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. Accept and Process New Input ---
if user_input := st.chat_input("Ask anything about the document..."):
    # యూజర్ మెసేజ్ స్క్రీన్‌పై చూపించి సేవ్ చేయడం
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    save_chat_messages(st.session_state.chat_messages)

    # అసిస్టెంట్ రెస్పాన్స్ ప్రాసెస్ చేయడం
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                # 💡 మీ బ్యాకెండ్ లాగ్ ప్రకారం కరెక్ట్ యుఆర్ఎల్ మరియు పేలోడ్ సెట్ చేశాను
                target_url = f"{BACKEND_URL}/api/query"
                payload = {"question": user_input}
                
                # ⚠️ 'timeout=None' పెట్టడం వల్ల 60 సెకన్ల పరిమితి తొలగిపోయింది!
                res = requests.post(target_url, json=payload, timeout=None)
                
                if res.status_code == 200:
                    ai_response = res.json().get("answer", "No answer found.")
                else:
                    ai_response = f"❌ Backend Error: Code {res.status_code}\n\nDetails: {res.text}"
            except Exception as e:
                ai_response = f"⚠️ Connection Error: {str(e)}"
            
            st.markdown(ai_response)
            
    # AI రెస్పాన్స్ హిస్టరీలో సేవ్ చేయడం
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
    save_chat_messages(st.session_state.chat_messages)
    st.rerun()