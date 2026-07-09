import streamlit as st
import requests

# --- CONFIG & BACKEND ---
BACKEND_URL = "http://127.0.0.1:8000"

st.markdown('<div class="section-title">📝 AI Document Summarizer</div>', unsafe_allow_html=True)

# Session state initialization
if "ai_summary_result" not in st.session_state:
    st.session_state.ai_summary_result = ""

# Two columns layout
col1, col2 = st.columns([4, 6])

with col1:
    st.markdown('<div class="glass-panel" style="min-height: 400px;">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick AI Summary")
    st.write("Click the button below to have the AI model analyze your document and generate a concise summary.")
    
    if st.session_state.get("pdf_uploaded", False):
        st.info(f"📄 Active File: {st.session_state.filename}")
        
        if st.button("Generate AI Summary ⚡", use_container_width=True, type="primary"):
            with st.spinner("Qwen Model is analyzing the document..."):
                try:
                    # Simplified prompt for better compatibility with local Qwen models
                    prompt_text = (
                        "Provide a clear and concise summary of this document. "
                        "Highlight the main core topics, core objectives, and key technical details mentioned."
                    )
                    
                    res = requests.post(f"{BACKEND_URL}/api/query", json={"question": prompt_text}, timeout=150)
                    
                    if res.status_code == 200:
                        st.session_state.ai_summary_result = res.json().get("answer", "No summary generated.")
                        st.toast("Summary generated successfully! 🎉")
                        st.rerun()
                    else:
                        st.error(f"❌ Backend Error: Code {res.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Backend connection failed: {str(e)}")
    else:
        st.warning("⚠️ Please upload a document on the home page first.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-panel" style="background: rgba(0, 255, 255, 0.03); border: 1px solid rgba(0, 255, 255, 0.15); min-height: 400px;">', unsafe_allow_html=True)
    
    if st.session_state.ai_summary_result:
        st.markdown(st.session_state.ai_summary_result)
        st.markdown('</div>', unsafe_allow_html=True) 
        
        # --- 📥 Download Button ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Summary as Text File",
            data=st.session_state.ai_summary_result,
            file_name=f"Summary_{st.session_state.get('filename', 'doc')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.markdown('<h3 style="color:rgba(255,255,255,0.4); text-align:center; padding-top:150px;">Click "Generate AI Summary" button to start analysis.</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)