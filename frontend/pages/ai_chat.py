import streamlit as st
import requests

def show_chat_page():
    st.markdown('<div class="section-title">💬 Dedicated AI Chat Room</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel" style="padding: 20px;">', unsafe_allow_html=True)
    
    if st.session_state.get("pdf_uploaded", False):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.write(msg)
        
        if prompt := st.chat_input("Ask a question about your active document..."):
            st.session_state.chat_history.append(("user", prompt))
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing document..."):
                    try:
                        res = requests.post("http://localhost:8000/api/query", json={"question": prompt}, timeout=60)
                        if res.status_code == 200:
                            answer = res.json().get("answer", "I cannot find the answer.")
                        else:
                            answer = "⚠️ Backend Service Error. Please check backend server logs."
                    except Exception as e:
                        answer = f"❌ Connection Error: Ensure your FastAPI backend server is running."
                    
                    st.write(answer)
                    st.session_state.chat_history.append(("assistant", answer))
    else:
        st.warning("⚠️ Chat ప్రారంభించడానికి దయచేసి ముందుగా సైడ్‌బార్‌లో ఒక డాక్యుమెంట్‌ను అప్‌లోడ్ చేయండి.")
    st.markdown('</div>', unsafe_allow_html=True)

show_chat_page()