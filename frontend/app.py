import streamlit as st
import requests
import os

# --- 1. CONFIG & BACKEND URL ---
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Document Assistant", page_icon="🤖", layout="wide")

# 🌟 సైడ్‌బార్ లోని పాత ఆటో-నావిగేషన్ టెక్స్ట్‌ను హైడ్ చేయడానికి CSS
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

def load_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "users_db" not in st.session_state: st.session_state.users_db = {"admin": "admin123"}
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login" 
if "pdf_uploaded" not in st.session_state: st.session_state.pdf_uploaded = False
if "filename" not in st.session_state: st.session_state.filename = ""
if "active_tab" not in st.session_state: st.session_state.active_tab = "Dashboard"
if "pages_count" not in st.session_state: st.session_state.pages_count = "0"
if "workspace_answer" not in st.session_state: st.session_state.workspace_answer = ""

try:
    if hasattr(st, "query_params"):
        params = st.query_params
        if "tab" in params:
            st.session_state.active_tab = params["tab"]
except:
    pass

# --- AUTH ACTIONS ---
def run_login(u, p):
    if u in st.session_state.users_db and st.session_state.users_db[u] == p:
        st.session_state.logged_in = True
        st.session_state.username = u
        st.toast(f"Welcome back, {u}! 🎉")
        st.rerun()
    else:
        st.error("❌ Invalid Username or Password")

def run_register(u, p, cp):
    if not u or not p:
        st.error("❌ Username and Password cannot be empty")
    elif u in st.session_state.users_db:
        st.error("❌ Username already exists! Try logging in.")
    elif p != cp:
        st.error("❌ Passwords do not match!")
    else:
        st.session_state.users_db[u] = p
        st.toast("🎯 Registration Successful! Please Login.")
        st.session_state.auth_mode = "login"
        st.rerun()

# --- AUTHENTICATION LAYER ---
if not st.session_state.logged_in:
    # లాగిన్ స్క్రీన్‌లో ఉన్నప్పుడు సైడ్‌బార్ కనిపించకుండా హైడ్ చేస్తుంది
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-mode"></div>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        if st.session_state.auth_mode == "login":
            with st.form("auth_form"):
                st.markdown('<div class="avatar-box"><div class="avatar-circle"><svg viewBox="0 0 24 24"><path d="M12,12A5,5 0 0,1 7,7A5,5 0 0,1 12,2A5,5 0 0,1 17,7A5,5 0 0,1 12,12M12,14C17.33,14 28,16.67 28,22V24H-4V22C-4,16.67 6.67,14 12,14Z" /></svg></div></div>', unsafe_allow_html=True)
                st.markdown('<h3 style="text-align:center; color:white; margin-top:0; margin-bottom:20px;">Account Login</h3>', unsafe_allow_html=True)
                u_val = st.text_input("Username", value="admin")
                p_val = st.text_input("Password", type="password", value="admin123")
                
                if st.form_submit_button("LOGIN"): 
                    run_login(u_val, p_val)
            
            st.markdown('<div style="text-align:center; margin-top:15px; font-size:13px; color:rgba(255,255,255,0.7);">Don\'t have an account? </div>', unsafe_allow_html=True)
            if st.button("Create an Account (Register) 🚀", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()

        elif st.session_state.auth_mode == "register":
            with st.form("register_form"):
                st.markdown('<div class="avatar-box"><div class="avatar-circle" style="background: #00FFFF;"><svg viewBox="0 0 24 24"><path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div></div>', unsafe_allow_html=True)
                st.markdown('<h3 style="text-align:center; color:white; margin-top:0; margin-bottom:20px;">Register New Account</h3>', unsafe_allow_html=True)
                reg_u = st.text_input("Choose Username")
                reg_p = st.text_input("Create Password", type="password")
                reg_cp = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("REGISTER NOW"):
                    run_register(reg_u, reg_p, reg_cp)
            
            st.markdown('<div style="text-align:center; margin-top:15px; font-size:13px; color:rgba(255,255,255,0.7);">Already have an account?</div>', unsafe_allow_html=True)
            if st.button("Back to Login 🏠", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- SIDEBAR MENU ---
    with st.sidebar:
        st.markdown("""
        <div class="brand-box">
            <span style="font-size:28px;">🤖</span>
            <div class="brand-title">Smart Document<br><span style="font-size:13px; color:rgba(255,255,255,0.6);">Assistant Workspace</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:11px; color:rgba(255,255,255,0.5); font-weight:700; margin-left:5px;'>MAIN MENU</p>", unsafe_allow_html=True)
        
        if st.button("🏠 Dashboard", key="btn_dash", use_container_width=True, type="primary" if st.session_state.active_tab == "Dashboard" else "secondary"):
            st.session_state.active_tab = "Dashboard"
            st.rerun()
            
        if st.button("📁 My Documents", key="btn_docs", use_container_width=True, type="primary" if st.session_state.active_tab == "Docs" else "secondary"):
            st.session_state.active_tab = "Docs"
            st.rerun()
            
        if st.button("💬 AI Chat", key="btn_chat", use_container_width=True, type="primary" if st.session_state.active_tab == "Chat" else "secondary"):
            st.session_state.active_tab = "Chat"
            st.rerun()
            
        if st.button("📝 Summarize", key="btn_sum", use_container_width=True, type="primary" if st.session_state.active_tab == "Summarize" else "secondary"):
            st.session_state.active_tab = "Summarize"
            st.rerun()
            
        if st.button("✂️ Extract Text", key="btn_ext", use_container_width=True, type="primary" if st.session_state.active_tab == "Extract" else "secondary"):
            st.session_state.active_tab = "Extract"
            st.rerun()
            
        if st.button("🌐 Translate", key="btn_trans", use_container_width=True, type="primary" if st.session_state.active_tab == "Translate" else "secondary"):
            st.session_state.active_tab = "Translate"
            st.rerun()
            
        if st.button("🖼️ Image", key="btn_img", use_container_width=True, type="primary" if st.session_state.active_tab == "Image" else "secondary"):
            st.session_state.active_tab = "Image"
            st.rerun()
            
        if st.button("📷 Camera", key="btn_cam", use_container_width=True, type="primary" if st.session_state.active_tab == "Camera" else "secondary"):
            st.session_state.active_tab = "Camera"
            st.rerun()

        st.markdown("<br><p style='font-size:11px; color:rgba(255,255,255,0.5); font-weight:700; margin-left:5px;'>MANAGEMENT</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
        
        if uploaded_file is not None and not st.session_state.pdf_uploaded:
            with st.spinner("Uploading & Processing PDF with Embeddings..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    res = requests.post(f"{BACKEND_URL}/api/upload", files=files, timeout=60)
                    
                    if res.status_code == 200:
                        res_data = res.json()
                        st.session_state.pdf_uploaded = True
                        st.session_state.filename = uploaded_file.name
                        st.session_state.pages_count = str(res_data.get("pages_processed", res_data.get("num_pages", "1")))
                        st.session_state.workspace_answer = "" 
                        st.toast("📄 PDF Uploaded & Processed Successfully! 🎉")
                        st.rerun()
                    else:
                        st.error(f"❌ Backend Error: Code {res.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Connection Exception: {str(e)}")

        if st.session_state.pdf_uploaded:
            st.markdown(f"<div style='background:rgba(0,255,255,0.1); padding:10px; border-radius:8px; border:1px solid rgba(0,255,255,0.3); font-size:12px; margin-bottom:10px; color:white;'>Selected: 📄 {st.session_state.filename[:18]}...</div>", unsafe_allow_html=True)
            if st.button("🗑️ Remove Active File", use_container_width=True):
                st.session_state.pdf_uploaded = False
                st.session_state.filename = ""
                st.session_state.pages_count = "0"
                st.session_state.workspace_answer = ""
                st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.auth_mode = "login"
            st.rerun()

    # --- MAIN CONTENT LAYER ---
    top_left, top_right = st.columns([8, 2])
    with top_left:
        st.markdown(f"<h1 style='font-size:32px; font-weight:700; margin:0;'>{st.session_state.active_tab} Panel</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:rgba(255,255,255,0.6); margin-top:2px;'>Welcome back, <b>{st.session_state.username}</b>!</p>", unsafe_allow_html=True)
    with top_right:
        st.markdown("<div style='text-align:right; margin-top:10px;'><span style='background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:20px; font-size:13px; border:1px solid rgba(255,255,255,0.2); color:white;'>👑 Premium Account</span></div>", unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.15; margin:15px 0;'>", unsafe_allow_html=True)

    # --- ROUTER CONTROL ---
    if st.session_state.active_tab == "Dashboard":
        doc_count = "1" if st.session_state.pdf_uploaded else "0"
        chats_count = "1" if st.session_state.pdf_uploaded else "0"
        p_count = st.session_state.pages_count
        status_text = "Online" if st.session_state.pdf_uploaded else "Awaiting File"

        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-premium-card"><div class="m-icon">📂</div><div class="m-info"><div class="m-label">Total Documents</div><div class="m-count">{doc_count}</div><div class="m-sub">↑ Active</div></div></div>
            <div class="metric-premium-card"><div class="m-icon">💬</div><div class="m-info"><div class="m-label">AI Chats</div><div class="m-count">{chats_count}</div><div class="m-sub">↑ Active sessions</div></div></div>
            <div class="metric-premium-card"><div class="m-icon">📄</div><div class="m-info"><div class="m-label">Pages Processed</div><div class="m-count">{p_count}</div><div class="m-sub">↑ Total info</div></div></div>
            <div class="metric-premium-card"><div class="m-icon">⚡</div><div class="m-info"><div class="m-label">System Status</div><div class="m-count">{status_text}</div><div class="m-sub" style="color:#00FFFF !important;">Qwen-2.5 Core</div></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Quick Actions Quick Panel</div>', unsafe_allow_html=True)
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
            if st.session_state.pdf_uploaded:
                st.markdown(f"""
                <table>
                    <tr><th style="color:#00FFFF !important;">File Name</th><th style="color:#00FFFF !important;">Extension</th><th style="color:#00FFFF !important;">Size</th><th style="color:#00FFFF !important;">Status</th></tr>
                    <tr><td style="color:white !important;">📕 {st.session_state.filename}</td><td><span style="background:#ef4444; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:700; color:white;">PDF</span></td><td style="color:white !important;">Active</td><td style="color:#00FFFF !important;">Active Pipeline</td></tr>
                </table>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:rgba(255,255,255,0.4); text-align:center; padding: 20px 0;'>No documents uploaded yet.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_br:
            st.markdown('<div class="section-title">✨ AI Fast Assistant Workspace</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            if st.session_state.pdf_uploaded:
                user_q = st.text_input("Ask a quick question from the active document:", placeholder="e.g. Summarize introduction...")
                if st.button("Ask Assistant 🚀") and user_q:
                    with st.spinner("Thinking..."):
                        try:
                            res = requests.post(f"{BACKEND_URL}/api/query", json={"question": user_q}, timeout=60)
                            if res.status_code == 200:
                                st.session_state.workspace_answer = res.json().get("answer", "No answer found.")
                            else:
                                st.error("Error from Backend Service.")
                        except:
                            st.error("Backend Disconnected.")
                if st.session_state.workspace_answer:
                    st.info(st.session_state.workspace_answer)
            else:
                st.markdown("<p style='color:rgba(255,255,255,0.4); text-align:center; padding: 20px 0;'>Upload a PDF to activate workspace.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- PAGES ROUTING ---
    elif st.session_state.active_tab == "Docs":
        if os.path.exists("pages/my_documents.py"):
            exec(open("pages/my_documents.py", encoding="utf-8").read())
        else:
            st.error("pages/my_documents.py ఫైల్ దొరకలేదు!")

    elif st.session_state.active_tab == "Chat":
        if os.path.exists("pages/ai_chat.py"):
            exec(open("pages/ai_chat.py", encoding="utf-8").read())
        else:
            st.error("pages/ai_chat.py ఫైల్ దొరకలేదు!")

    elif st.session_state.active_tab == "Summarize":
        # 🌟 పాత 'pages/summarize.py' ని కొత్త ఫైల్ 'pages/summary.py' కి ఇక్కడ అప్‌డేట్ చేసాం
        if os.path.exists("pages/summary.py"):
            exec(open("pages/summary.py", encoding="utf-8").read())
        else:
            st.error("pages/summary.py ఫైల్ దొరకలేదు!")

    elif st.session_state.active_tab == "Extract":
        if os.path.exists("pages/extract_text.py"):
            exec(open("pages/extract_text.py", encoding="utf-8").read())

    elif st.session_state.active_tab == "Translate":
        if os.path.exists("pages/translate.py"):
            exec(open("pages/translate.py", encoding="utf-8").read())

    elif st.session_state.active_tab == "Image":
        if os.path.exists("pages/image.py"):
            exec(open("pages/image.py", encoding="utf-8").read())

    elif st.session_state.active_tab == "Camera":
        if os.path.exists("pages/camera.py"):
            exec(open("pages/camera.py", encoding="utf-8").read())