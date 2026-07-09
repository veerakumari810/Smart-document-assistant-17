import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown('<div class="section-title">📊 System Dashboard</div>', unsafe_allow_html=True)

doc_count = "1" if st.session_state.get("pdf_uploaded", False) else "0"
chats_count = "1" if st.session_state.get("pdf_uploaded", False) else "0"
pages_count = st.session_state.get("pages_count", "0")
status_text = "Online" if st.session_state.get("pdf_uploaded", False) else "Awaiting File"

st.markdown(f"""
<div class="metrics-grid">
    <div class="metric-premium-card"><div class="m-icon">📂</div><div class="m-info"><div class="m-label">Total Documents</div><div class="m-count">{doc_count}</div><div class="m-sub">↑ Active</div></div></div>
    <div class="metric-premium-card"><div class="m-icon">💬</div><div class="m-info"><div class="m-label">AI Chats</div><div class="m-count">{chats_count}</div><div class="m-sub">↑ Active sessions</div></div></div>
    <div class="metric-premium-card"><div class="m-icon">📄</div><div class="m-info"><div class="m-label">Pages Processed</div><div class="m-count">{pages_count}</div><div class="m-sub">↑ Total info</div></div></div>
    <div class="metric-premium-card"><div class="m-icon">⚡</div><div class="m-info"><div class="m-label">System Status</div><div class="m-count">{status_text}</div><div class="m-sub" style="color:#00FFFF !important;">Qwen-2.5 Core</div></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Quick Actions Panel</div>', unsafe_allow_html=True)
st.markdown("""
<div class="action-grid">
    <div class="action-item-card"><div class="a-icon">📤</div><div class="a-title">Upload</div><div class="a-desc">PDF, DOCX files</div></div>
    <div class="action-item-card"><div class="a-icon">💬</div><div class="a-title">AI Chat</div><div class="a-desc">Deep analysis</div></div>
    <div class="action-item-card"><div class="a-icon">📝</div><div class="a-title">Summarize</div><div class="a-desc">Layout summary</div></div>
    <div class="action-item-card"><div class="a-icon">✂️</div><div class="a-title">Extract Text</div><div class="a-desc">OCR raw strings</div></div>
    <div class="action-item-card"><div class="a-icon">🌐</div><div class="a-title">Translate</div><div class="a-desc">Multi language</div></div>
</div>
""", unsafe_allow_html=True)

col_bl, col_br = st.columns([6, 4])
with col_bl:
    st.markdown('<div class="section-title">Recent Loaded Documents</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    if st.session_state.get("pdf_uploaded", False):
        st.markdown(f"""
        <table>
            <tr><th style="color:#00FFFF !important;">File Name</th><th style="color:#00FFFF !important;">Extension</th><th style="color:#00FFFF !important;">Size</th><th style="color:#00FFFF !important;">Status</th></tr>
            <tr><td style="color:white !important;">📕 {st.session_state.get("filename", "")}</td><td><span style="background:#ef4444; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:700; color:white;">PDF</span></td><td style="color:white !important;">Active</td><td style="color:#00FFFF !important;">Active Pipeline</td></tr>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:rgba(255,255,255,0.4); text-align:center; padding: 20px 0;'>No documents uploaded yet.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_br:
    st.markdown('<div class="section-title">✨ AI Fast Assistant Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    if st.session_state.get("pdf_uploaded", False):
        user_q = st.text_input("Ask a quick question from the active document:", placeholder="e.g. Summarize introduction...")
        
        if st.button("Ask Assistant 🚀") and user_q:
            with st.spinner("Processing dynamic answer..."):
                try:
                    rag_prompt = (
                        f"Context from uploaded document:\n"
                        f"You are a precise document assistant. Answer the user's question directly "
                        f"using short bullet points based ONLY on the context provided above.\n\n"
                        f"Question: {user_q}"
                    )
                    response = requests.post(f"{BACKEND_URL}/api/query", json={"question": rag_prompt}, timeout=90)
                    if response.status_code == 200:
                        st.session_state.workspace_answer = response.json().get("answer", "No response text found.")
                    else:
                        st.session_state.workspace_answer = f"Backend Error (Code: {response.status_code})"
                except Exception as e:
                    st.session_state.workspace_answer = f"Connection Failed: {str(e)}"
        
        if st.session_state.get("workspace_answer", ""):
            st.markdown("<hr style='opacity:0.1; margin:10px 0;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:white; font-size:14px; background:rgba(255,255,255,0.05); padding:10px; border-radius:6px;'>{st.session_state.workspace_answer}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:rgba(255,255,255,0.4); text-align:center; padding: 20px 0;'>Workspace locked. Upload a document to start.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)