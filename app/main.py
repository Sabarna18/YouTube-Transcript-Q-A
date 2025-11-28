import streamlit as st
import utils
from store import Store
from agents import Agent

# Page configuration
st.set_page_config(
    page_title="YouTube Transcript Analyzer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

SYSTEM_PROMPT = """You are an advanced AI-powered News Research Analyst designed to perform 
high-quality analysis on recent events, reports, and global news. Your role is 
to read the user's query, gather contextual signals, understand the domain of 
interest, and produce clear, accurate, well-structured insights.

### OBJECTIVES
1. Provide a well-reasoned, factual, and comprehensive analysis of the topic.
2. Summarize major developments, key actors, and implications.
3. Highlight trends, risks, and opportunities where relevant.
4. Maintain high factual accuracy and avoid assumptions.
5. Provide citations or source context if available.

### OUTPUT STYLE
- Professional and concise but highly informative.
- Use clear sectioning such as:
  - Executive Summary
  - Key Facts / Background
  - Latest Developments
  - Expert Analysis
  - Forecasts / What to Watch
  - Conclusion
- Avoid unnecessary storytelling.
- Avoid hallucinations; do not fabricate data or events.
- If information is insufficient, clearly state limitations.

### RESPONSE REQUIREMENTS
- Maintain an objective, unbiased tone.
- Include bullet points for readability where useful.
- Provide context that connects past events to present developments.
- Where applicable, give recommendations or actionable insights.

### USER QUERY
The user will provide a topic or question. 
Your task is to deliver a complete, research-grade answer that feels like a 
professional intelligence briefing.
Respond in the most accurate, structured, and reliable manner possible."""

# Custom CSS for premium professional styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 1.5rem;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 50%, #0f1419 100%);
        min-height: 100vh;
    }
    
    /* Enhanced Button Styles */
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 3.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        letter-spacing: 0.8px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white;
        border: none;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #c026d3 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Premium Header */
    .header-container {
        background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 25%, #6d28d9 50%, #7c3aed 75%, #8b5cf6 100%);
        padding: 4rem 3rem;
        border-radius: 28px;
        margin-bottom: 2.5rem;
        box-shadow: 0 25px 70px rgba(124, 58, 237, 0.5);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.15);
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: pulse 5s ease-in-out infinite;
    }
    
    .header-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef, #ec4899);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.8);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.15) rotate(180deg); opacity: 0.8; }
    }
    
    .header-title {
        color: #ffffff;
        font-size: 3.8rem;
        font-weight: 900;
        margin: 0;
        text-align: center;
        text-shadow: 0 6px 16px rgba(0,0,0,0.4);
        letter-spacing: -1.5px;
        position: relative;
        z-index: 1;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header-subtitle {
        color: #e9d5ff;
        font-size: 1.5rem;
        text-align: center;
        margin-top: 1rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-shadow: 0 3px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.8rem;
        padding-bottom: 1rem;
        border-bottom: 4px solid;
        border-image: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef) 1;
        letter-spacing: -0.5px;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 80px; }
    }
    
    /* Info Box Styles */
    .info-box {
        background: rgba(99, 102, 241, 0.12);
        backdrop-filter: blur(16px);
        border: 2px solid rgba(99, 102, 241, 0.35);
        border-left: 6px solid #6366f1;
        padding: 1.8rem;
        border-radius: 18px;
        margin: 1.2rem 0;
        color: #e0e7ff;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .info-box:hover {
        transform: translateY(-4px) translateX(4px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4);
        border-left-width: 10px;
        background: rgba(99, 102, 241, 0.18);
    }
    
    /* Success Box */
    .success-box {
        background: rgba(34, 197, 94, 0.15);
        backdrop-filter: blur(16px);
        border: 2px solid rgba(34, 197, 94, 0.4);
        border-left: 6px solid #22c55e;
        padding: 2rem;
        border-radius: 18px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
        animation: slideInLeft 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .success-box h4 {
        color: #86efac;
        font-weight: 900;
        font-size: 1.4rem;
        margin: 0 0 0.8rem 0;
        letter-spacing: -0.5px;
    }
    
    .success-box p {
        color: #bbf7d0;
        font-weight: 600;
        font-size: 1.08rem;
        margin: 0;
        line-height: 1.7;
    }
    
    /* Enhanced Input Styles */
    .stTextInput>div>div>input {
        border-radius: 14px;
        border: 2px solid rgba(99, 102, 241, 0.3);
        padding: 1.2rem 1.5rem;
        font-size: 1.08rem;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        color: #f1f5f9;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8b5cf6;
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.25), 0 8px 24px rgba(139, 92, 246, 0.3);
        transform: translateY(-2px);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Select Box */
    .stSelectbox>div>div>div {
        border-radius: 14px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        color: #f1f5f9;
        border: 2px solid rgba(99, 102, 241, 0.3);
        font-weight: 600;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stSelectbox>div>div>div:hover {
        border-color: #8b5cf6;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    /* Answer Box */
    .answer-box {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
        border: 2px solid rgba(99, 102, 241, 0.35);
        border-left: 6px solid #6366f1;
        color: #f1f5f9;
        font-size: 1.12rem;
        line-height: 1.9;
        font-weight: 500;
        animation: fadeInScale 0.6s ease-out;
    }
    
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Query History Styles */
    .history-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        margin-top: 2rem;
    }
    
    .history-item {
        background: rgba(51, 65, 85, 0.6);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(99, 102, 241, 0.25);
        border-left: 5px solid #8b5cf6;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .history-item:hover {
        background: rgba(51, 65, 85, 0.8);
        border-left-width: 8px;
        transform: translateX(6px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
    }
    
    .history-question {
        color: #c7d2fe;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .history-answer {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 500;
        padding-left: 1.8rem;
        border-left: 3px solid rgba(99, 102, 241, 0.3);
        margin-top: 0.8rem;
    }
    
    .history-timestamp {
        color: #94a3b8;
        font-size: 0.88rem;
        font-weight: 600;
        margin-top: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .clear-history-btn {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .clear-history-btn:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(239, 68, 68, 0.6);
    }
    
    /* Sidebar Styles */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 3px solid rgba(99, 102, 241, 0.3);
    }
    
    div[data-testid="stSidebar"] h3 {
        color: #c7d2fe;
        font-weight: 900;
        font-size: 1.4rem;
        letter-spacing: -0.5px;
    }
    
    div[data-testid="stSidebar"] h4 {
        color: #ddd6fe;
        font-weight: 800;
        font-size: 1.1rem;
    }
    
    .sidebar-info {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        padding: 1.5rem;
        border-radius: 14px;
        border: 2px solid rgba(99, 102, 241, 0.3);
        color: #cbd5e1;
        font-size: 0.98rem;
        line-height: 1.8;
        font-weight: 500;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-info b {
        color: #c7d2fe;
        font-weight: 800;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.6rem 1.3rem;
        border-radius: 25px;
        font-weight: 800;
        font-size: 0.95rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .status-success {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: 2px solid rgba(34, 197, 94, 0.5);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border: 2px solid rgba(245, 158, 11, 0.5);
    }
    
    /* Card Container */
    .card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 2rem;
        border: 2px solid rgba(99, 102, 241, 0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    /* Statistics Display */
    .stat-container {
        background: rgba(51, 65, 85, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid rgba(99, 102, 241, 0.3);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #cbd5e1;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        padding: 2.5rem;
        font-weight: 600;
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 2px solid rgba(99, 102, 241, 0.25);
        margin-top: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .footer p {
        margin: 0;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 1.1rem;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid rgba(99, 102, 241, 0.25);
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(51, 65, 85, 0.6);
        border-radius: 12px;
        font-weight: 700;
        color: #c7d2fe;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎥 YouTube Transcript Analyzer</h1>
        <p class="header-subtitle">AI-Powered Video Content Analysis with RAG Technology</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    st.markdown("#### 🤖 Embedding Model")
    options = {
        "Google Gemini": "models/gemini-embedding-001",
        "HuggingFace MPNet": "sentence-transformers/all-mpnet-base-v2"
    }
    
    option = st.selectbox(
        "Choose your embedding model:",
        list(options.keys()),
        help="Select the embedding model for vector representation"
    )
    embedding_model = options[option]
    
    st.markdown("---")
    st.markdown("#### 📊 System Status")
    if st.session_state.processed:
        st.markdown('<span class="status-badge status-success">✅ Video Processed</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-pending">⏳ Awaiting Input</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <div class="sidebar-info">
        <b>🚀 How it works:</b><br><br>
        1️⃣ Enter YouTube URL<br>
        2️⃣ Select embedding model<br>
        3️⃣ Process the video<br>
        4️⃣ Ask questions about content
        </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="section-header">📹 Video Input</p>', unsafe_allow_html=True)
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )
    
    process_btn = st.button("🚀 Process Video", type="primary", use_container_width=True)

with col2:
    st.markdown('<p class="section-header">ℹ️ Quick Tips</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
        <b style="font-size: 1.05rem;">✨ Supported URLs:</b><br><br>
        <span>🔗 Standard YouTube links<br>
        ⚡ Shortened youtu.be links<br>
        ⏱️ Videos with timestamps</span>
        </div>
    """, unsafe_allow_html=True)

# Initialize store and agent
store = Store()
agent = Agent()

# Process video
if process_btn:
    if not url:
        st.error("⚠️ Please enter a valid YouTube URL")
    else:
        with st.spinner("🔄 Processing video transcript..."):
            try:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🎬 Extracting transcript...")
                progress_bar.progress(20)
                transcript = utils.extract_transcript(url)
                
                status_text.text("🤖 Initializing models...")
                progress_bar.progress(40)
                groq_llm = agent.groq_model
                gemini_llm = agent.google_llm
                hf_embedding = store.hf_embedding
                google_embedding = store.google_embedding
                
                hf_directory = "hf_vectorstore"
                google_directory = "google_vectorstore"
                
                status_text.text("📄 Creating document chunks...")
                progress_bar.progress(60)
                document = utils.create_Documents(transcript)
                chunks = utils.split_documents(document)
                
                status_text.text("🔮 Building vector store...")
                progress_bar.progress(80)
                if embedding_model == "models/gemini-embedding-001":
                    vectorstore = store.create_vector_store(
                        documents=chunks,
                        embeddings=google_embedding,
                        directory=google_directory
                    )
                else:
                    vectorstore = store.create_vector_store(
                        documents=chunks,
                        embeddings=hf_embedding,
                        directory=hf_directory
                    )
                
                status_text.text("⚡ Finalizing retriever...")
                progress_bar.progress(100)
                retriever = store.create_retriever(vectorstore=vectorstore)
                
                # Store in session state
                st.session_state.vectorstore = vectorstore
                st.session_state.retriever = retriever
                st.session_state.processed = True
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.markdown("""
                    <div class="success-box">
                        <h4>✅ Processing Complete!</h4>
                        <p>
                        Your video has been successfully analyzed and indexed. You can now ask questions about the content.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error processing video: {str(e)}")

# Question-answering section
st.markdown("---")
st.markdown('<p class="section-header">💬 Ask Questions</p>', unsafe_allow_html=True)

if st.session_state.processed:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "Your Question",
            placeholder="What is this video about?",
            label_visibility="collapsed",
            key="question_input"
        )
    
    with col2:
        qs_btn = st.button("🔍 Ask", type="primary", use_container_width=True)
    
    if qs_btn:
        if not question:
            st.warning("⚠️ Please enter a question")
        else:
            with st.spinner("🤔 Generating answer..."):
                try:
                    enhanced_query = f"{SYSTEM_PROMPT}\n\n### USER QUERY:\n{question}\n\nBased on the provided sources, deliver a comprehensive intelligence briefing."
                    answer = agent.generate_answer(
                        retriever=st.session_state.retriever,
                        model=agent.groq_model,
                        question=enhanced_query
                    )
                    
                    st.markdown("### 📝 Answer")
                    st.markdown(f"""
                        <div class='answer-box'>
                        {answer}
                        </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error generating answer: {str(e)}")
else:
    st.markdown("""
        <div class="info-box">
        <b style="font-size: 1.1rem;">👆 Getting Started</b><br><br>
        <span>Please process a video first before asking questions. Enter a YouTube URL above and click the Process Video button.</span>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <p>⚡ Powered by RAG Technology | Built with Streamlit 🚀</p>
    </div>
""", unsafe_allow_html=True)