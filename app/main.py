import streamlit as st
from store import Store
from agents import Agent
import utils
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="YouTube Transcript Analyzer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Main background - Professional dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .main-header h1 {
        color: #f1f5f9;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: #94a3b8;
        margin: 0.75rem 0 0 0;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Info banner for user guidance */
    .info-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: #e0e7ff;
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    
    .info-banner h4 {
        color: #dbeafe;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .info-banner ul {
        margin: 0.5rem 0 0 1.25rem;
        padding: 0;
        color: #bfdbfe;
    }
    
    .info-banner li {
        margin: 0.4rem 0;
        font-size: 0.95rem;
    }
    
    /* Card containers */
    .card-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 800;
        color: #f1f5f9 !important;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Fix for all Streamlit labels - CRITICAL */
    label, .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #475569;
        background: #1e293b;
        font-size: 1rem;
        padding: 0.875rem;
        font-weight: 500;
        transition: all 0.3s ease;
        color: #f1f5f9 !important;
    }
    
    /* Selectbox - FIXED STYLING */
    .stSelectbox > div > div {
        background: #1e293b;
        border-radius: 12px;
        border: 2px solid #475569;
    }
    
    .stSelectbox > div > div > select,
    .stSelectbox > div > div > div {
        background: #1e293b !important;
        color: #f1f5f9 !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        
    }
    
    /* Selectbox dropdown options */
    .stSelectbox [data-baseweb="select"] {
        background: #1e293b !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: #1e293b !important;
        border-color: #475569 !important;
    }
    
    /* Placeholder text */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b !important;
        font-weight: 400;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.875rem 2rem;
        transition: all 0.3s ease;
        border: none;
        font-size: 1.05rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stButton > button:disabled {
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        box-shadow: none;
        cursor: not-allowed;
        opacity: 0.6;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        color: #d1fae5;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);
        color: #fecaca;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: #dbeafe;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    /* Answer box */
    .answer-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px solid #6366f1;
        padding: 1.75rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    }
    
    .answer-box h3 {
        color: #a5b4fc !important;
        margin-top: 0;
        font-weight: 800;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .answer-box p {
        color: #e2e8f0 !important;
        line-height: 1.8;
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* History card */
    .history-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .history-card:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }
    
    .history-timestamp {
        color: #94a3b8 !important;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .history-question {
        color: #a5b4fc !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .history-answer {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
        font-weight: 400;
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.875rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 0.5rem;
        margin-top: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-indigo {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
    }
    
    .badge-purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #475569 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        margin-top: 3rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Empty state text */
    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        color: #64748b;
    }
    
    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'processed_url' not in st.session_state:
    st.session_state.processed_url = ""
if 'current_embedding' not in st.session_state:
    st.session_state.current_embedding = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🎥 YouTube Transcript Analyzer</h1>
    <p>AI-Powered Video Q&A with RAG Technology</p>
</div>
""", unsafe_allow_html=True)

# User guide banner
st.markdown("""
<div class="info-banner">
    <h4>📖 How to Use This Application</h4>
    <ul>
        <li><strong>Step 1:</strong> Paste a YouTube video URL in the input field below</li>
        <li><strong>Step 2:</strong> Select an embedding model (Google or Hugging Face)</li>
        <li><strong>Step 3:</strong> Click "Process Video" to analyze the transcript</li>
        <li><strong>Step 4:</strong> Ask questions about the video content</li>
        <li><strong>Note:</strong> Processing may take 30-60 seconds depending on video length</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Process Video Section
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-icon">🎬</div>Process Video</div>', unsafe_allow_html=True)
    
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="url_input",
        disabled=st.session_state.get('processing', False),
        label_visibility="visible"
    )
    
    options = {
        "Google": "models/gemini-embedding-001",
        "Hugging Face": "sentence-transformers/all-mpnet-base-v2"
    }
    
    embedding_model = st.selectbox(
        "Embedding Model",
        list(options.keys()),
        key="embedding_select",
        disabled=st.session_state.get('processing', False),
        help="Choose the AI model for text embeddings"
    )
    
    if st.button("🎥 Process Video", key="process_btn", type="primary"):
        if not url.strip():
            st.markdown('<div class="error-box">⚠️ Please enter a YouTube URL</div>', unsafe_allow_html=True)
        else:
            st.session_state.processing = True
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Extract transcript
                status_text.markdown("🔄 Fetching video transcript...")
                progress_bar.progress(20)
                transcript = utils.extract_transcript(url)
                
                # Step 2: Create documents
                status_text.markdown("📄 Creating document chunks...")
                progress_bar.progress(40)
                document = utils.create_Documents(transcript)
                
                # Step 3: Split documents
                status_text.markdown("✂️ Splitting documents...")
                progress_bar.progress(60)
                chunks = utils.split_documents(document)
                
                # Step 4: Create embeddings and vector store
                status_text.markdown("🧠 Generating embeddings and building vector database...")
                progress_bar.progress(80)
                store = Store(embedding_model=options[embedding_model])
                vectorstore = store.create_vector_db(documents=chunks)
                
                # Step 5: Create retriever
                status_text.markdown("🔍 Initializing retriever...")
                progress_bar.progress(100)
                retriever = store.create_retriever(vectorstore=vectorstore)
                
                # Save to session state
                st.session_state.vectorstore = vectorstore
                st.session_state.retriever = retriever
                st.session_state.video_processed = True
                st.session_state.processed_url = url
                st.session_state.current_embedding = embedding_model
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.markdown('<div class="success-box">✅ Video processed successfully! You can now ask questions about the content.</div>', unsafe_allow_html=True)
                
                
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            finally:
                st.session_state.processing = False
    
    # Show processed video info
    if st.session_state.video_processed:
        st.markdown(f'<div class="info-box">✅ <strong>Processed Video:</strong> {st.session_state.processed_url[:50]}... | <strong>Model:</strong> {st.session_state.current_embedding}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Ask Question Section
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-icon">💬</div>Ask Question</div>', unsafe_allow_html=True)
    
    question = st.text_area(
        "Your Question",
        placeholder="What is this video about? What are the key takeaways?",
        height=140,
        key="question_input",
        disabled=not st.session_state.video_processed or st.session_state.get('querying', False),
        help="Ask any question about the video content"
    )
    
    if st.button("🚀 Ask Question", key="ask_btn", type="primary", disabled=not st.session_state.video_processed):
        if not question.strip():
            st.markdown('<div class="error-box">⚠️ Please enter a question</div>', unsafe_allow_html=True)
        else:
            st.session_state.querying = True
            
            with st.spinner("🤔 Analyzing video content and generating answer..."):
                try:
                    agent = Agent()
                    model = agent.groq_model
                    
                    answer = agent.generate_answer(
                        retriever=st.session_state.retriever,
                        model=model,
                        question=question
                    )
                    
                    # Display answer
                    st.markdown(f"""
                    <div class="answer-box">
                        <h3>💡 Answer:</h3>
                        <p>{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to history
                    history_entry = {
                        'id': len(st.session_state.query_history),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'video_url': st.session_state.processed_url,
                        'embedding_model': st.session_state.current_embedding,
                        'question': question,
                        'answer': answer,
                        'chunk_size': '512 tokens'
                    }
                    st.session_state.query_history.insert(0, history_entry)
                    
                    st.markdown('<div class="success-box">✅ Question answered successfully!</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                finally:
                    st.session_state.querying = False
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Query History Section
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-icon">📜</div>Query History</div>', unsafe_allow_html=True)
    
    if st.session_state.query_history:
        # Action buttons
        col_export, col_clear = st.columns(2)
        with col_export:
            json_data = json.dumps(st.session_state.query_history, indent=2)
            st.download_button(
                label="📥 Export",
                data=json_data,
                file_name=f"query_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json",
                use_container_width=True
            )
        with col_clear:
            if st.button("🗑️ Clear", key="clear_btn", use_container_width=True):
                st.session_state.query_history = []
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Display history
        for entry in st.session_state.query_history:
            st.markdown(f"""
            <div class="history-card">
                <div class="history-timestamp">🕒 {entry['timestamp']}</div>
                <div class="history-question">Q: {entry['question'][:100]}{"..." if len(entry['question']) > 100 else ""}</div>
                <div class="history-answer">A: {entry['answer'][:150]}{"..." if len(entry['answer']) > 150 else ""}</div>
                <div>
                    <span class="badge badge-indigo">{entry['embedding_model']}</span>
                    <span class="badge badge-purple">{entry['chunk_size']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <p style="font-size: 1rem; font-weight: 600; color: #64748b;">No queries yet</p>
            <p style="font-size: 0.9rem; color: #475569;">Process a video and ask questions to see history here</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit, LangChain, and RAG Technology<br>
    <span style="font-size: 0.85rem; opacity: 0.7;">Powered by AI • Designed for Excellence</span>
</div>
""", unsafe_allow_html=True)