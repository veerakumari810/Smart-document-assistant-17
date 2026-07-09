import streamlit as st

def show_docs_page():
    # సెర్చ్ బార్
    search_query = st.text_input("🔍 Search your documents...", placeholder="Type file name here...")
    
    st.markdown('<div class="glass-panel" style="padding: 20px; background: rgba(255,255,255,0.03); border-radius: 10px; margin-top: 15px;">', unsafe_allow_html=True)
    
    # app.py లో సెట్ చేసిన 'pdf_uploaded' వేరియబుల్‌ని ఇక్కడ సరిగ్గా చెక్ చేస్తున్నాం
    if st.session_state.get("pdf_uploaded", False):
        filename = st.session_state.get("filename", "Unknown_File.pdf")
        pages_count = st.session_state.get("pages_count", "1")
        
        # సెర్చ్ ఫిల్టర్
        if search_query.lower() in filename.lower() or search_query == "":
            file_ext = filename.split('.')[-1].upper() if '.' in filename else "PDF"
            file_icon = "📕" if file_ext == "PDF" else "📘"
            
            # అందమైన టేబుల్ డిజైన్
            st.markdown(f"""
            <style>
                .doc-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; color: white; }}
                .doc-table th {{ background-color: rgba(255, 255, 255, 0.08); color: #00FFFF !important; text-align: left; padding: 12px; font-weight: 600; border-bottom: 2px solid rgba(255, 255, 255, 0.1); }}
                .doc-table td {{ padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 14px; color: white !important; }}
                .status-badge {{ background: rgba(16, 185, 129, 0.2); color: #10B981; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
            </style>
            <table class="doc-table">
                <tr>
                    <th>File Name</th>
                    <th>Type</th>
                    <th>Pages</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td>{file_icon} {filename}</td>
                    <td><span style="background: #ef4444; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; color: white;">{file_ext}</span></td>
                    <td>{pages_count} Pages</td>
                    <td><span class="status-badge">✅ Processed & Active</span></td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # క్విక్ యాక్షన్ బటన్స్
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 Start AI Chat with this File", use_container_width=True):
                    st.session_state.active_tab = "Chat"
                    st.rerun()
            with col2:
                if st.button("📝 View Summary of this File", use_container_width=True):
                    st.session_state.active_tab = "Summarize"
                    st.rerun()
        else:
            st.warning("⚠️ No results found for your search.")
    else:
        st.info("💡 ప్రస్తుతం ఎలాంటి డాక్యుమెంట్లు అప్‌లోడ్ కాలేదు. దయచేసి సైడ్‌బార్‌ (Sidebar) లో ఉన్న 'Upload PDF Document' ఆప్షన్ ద్వారా ఒక ఫైల్‌ను అప్‌లోడ్ చేయండి.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# పేజీ రన్ అవ్వడానికి ఫంక్షన్‌ని కాల్ చేయాలి
show_docs_page()