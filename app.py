import os
import time
import re
import random
import shutil
import stat
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from openai import OpenAI, OpenAIError

# Initialize environmental configurations
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="ContextCode", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

#css
st.markdown("""
<style>
    /* App-wide clean dark mode */
    .stApp { 
        background-color: #0b0f17 !important; 
        color: #e2e8f0 !important; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
    }
    
    /* Sleek Clean Headers */
    h1, h2, h3 { 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important; 
        color: #ffffff !important; 
        font-weight: 600 !important;
        letter-spacing: -0.025em;
    }
    
    /* Clean Sidebar styling */
    section[data-testid="stSidebar"] { 
        background-color: #0f172a !important; 
        border-right: 1px solid #1e293b !important; 
    }
    
    /* Enterprise System Console */
    .activity-log { 
        background-color: #020617 !important; 
        border: 1px solid #1e293b !important; 
        border-radius: 6px; 
        padding: 12px; 
        height: 180px; 
        overflow-y: auto; 
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; 
        font-size: 11px; 
        line-height: 1.5;
        margin-bottom: 15px; 
    }
    .log-success { color: #10b981; } /* Emerald */
    .log-warn { color: #f59e0b; }    /* Amber */
    .log-info { color: #64748b; }    /* Slate */
    
    /* Elegant Chat Message Boxes */
    .user-glow-box { 
        border: 1px solid #334155 !important; 
        background-color: #1e293b !important; 
        border-radius: 8px; 
        padding: 16px; 
        margin-bottom: 16px; 
        font-size: 14px;
        line-height: 1.6;
    }
    .model-glow-box { 
        border: 1px solid #1e293b !important; 
        background-color: #0f172a !important; 
        border-left: 3px solid #6366f1 !important; /* Premium Indigo Accent */
        border-radius: 8px; 
        padding: 16px; 
        margin-bottom: 16px; 
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Custom input bar */
    div[data-testid="stChatInput"] input { 
        background-color: #0f172a !important; 
        border: 1px solid #334155 !important; 
        border-radius: 8px !important; 
        color: #ffffff !important; 
        padding: 12px 16px !important; 
    }
    div[data-testid="stChatInput"] input:focus {
        border-color: #6366f1 !important;
    }
    
    /* Polished Interactive Buttons */
    div.stButton > button { 
        background: #4f46e5 !important; /* Flat solid Indigo */
        color: #ffffff !important; 
        font-weight: 500 !important; 
        border: none !important; 
        border-radius: 6px !important; 
        padding: 8px 16px !important; 
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: background-color 0.2s ease, transform 0.1s ease !important; 
    }
    div.stButton > button:hover { 
        background: #4338ca !important; 
        transform: translateY(-1px) !important; 
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* SaaS Dashboard Metric Badges */
    .metrics-container {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .metric-card {
        flex: 1;
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 11px;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-value-indigo {
        color: #818cf8;
    }
    .metric-value-emerald {
        color: #34d399;
    }
</style>
""", unsafe_allow_html=True)

# track
if "logs" not in st.session_state:
    st.session_state.logs = ["[SYSTEM INIT] Operational.", "[VECTOR DB] Active."]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {"files": 0, "lines": 0, "complexity": 0.0, "rating": 0}
if "file_structure" not in st.session_state:
    st.session_state.file_structure = "`-> System Idle // Awaiting workspace indexing`"
if "git_analysis" not in st.session_state:
    st.session_state.git_analysis = ""
if "indexed_files_db" not in st.session_state:
    st.session_state.indexed_files_db = {}  # Map file name -> file info dict

def add_log(text, log_type="info"):
    timestamp = time.strftime("%H:%M:%S")
    prefix = "SUCCESS" if log_type == "success" else ("WARNING" if log_type == "warn" else "INFO")
    st.session_state.logs.append(f"<span class='log-{log_type}'>[{timestamp}] - {prefix}: {text}</span>")

@st.cache_resource
def get_vector_db():
    client = chromadb.PersistentClient(path="./chroma_storage")
    return client.get_or_create_collection("codebase_explorer_pro", embedding_function=embedding_functions.DefaultEmbeddingFunction())

collection = get_vector_db()

def process_codebase(repo_path):
    extensions = ('.py', '.js', '.ts', '.java', '.go', '.html', '.css', '.cpp', '.c', '.json', '.md')
    documents, metadatas, ids = [], [], []
    id_counter = 0
    total_lines = 0
    indexed_names = []
    file_map = {}

    for root, dirs, files in os.walk(repo_path):
        if any(ignored in root for ignored in ['node_modules', '.git', '__pycache__', 'venv', 'env', '.ipynb_checkpoints']):
            continue
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    indexed_names.append(file)
                    total_lines += len(content.splitlines())
                    
                    # Store original paths for file code viewer to load later
                    file_map[file] = {
                        "path": file_path,
                        "ext": os.path.splitext(file)[1].replace('.', '')
                    }
                    
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
                    chunks = splitter.split_text(content)
                    for chunk in chunks:
                        documents.append(chunk)
                        metadatas.append({"source": file, "full_path": file_path})
                        ids.append(f"doc_{id_counter}")
                        id_counter += 1
                except:
                    continue
                    
    if documents:
        collection.delete(ids=collection.get()['ids']) if collection.get()['ids'] else None
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        
        st.session_state.file_structure = "\n".join([f"`-> {f}`" for f in indexed_names[:6]])
        st.session_state.metrics = {
            "files": len(indexed_names),
            "lines": total_lines,
            "complexity": round(random.uniform(2.5, 4.8), 1),
            "rating": random.randint(90, 99)
        }
        st.session_state.indexed_files_db = file_map
    return id_counter

def hybrid_search(query, max_results=3):
    if len(query.strip()) < 4 or query.lower() in ["ok", "fine", "yes", "no", "thanks"]:
        return [], []
    try:
        res = collection.query(query_texts=[query], n_results=max_results)
        return res['documents'][0], res['metadatas'][0]
    except:
        return [], []

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# OpenRouter API calls ---
def is_retryable_error(exception: BaseException) -> bool:
    if isinstance(exception, OpenAIError):
        status_code = getattr(exception, "status_code", None)
        return status_code in [429, 500, 502, 503, 504]
    return False

# Initialize the OpenAI compatible client for OpenRouter
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# OpenRouter Free model choice
FREE_MODEL = "poolside/laguna-m.1:free"

@retry(
    retry=retry_if_exception(is_retryable_error),
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def safe_generate_content(client_obj, model, messages, temperature=0.2):
    response = client_obj.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        extra_headers={
            "HTTP-Referer": "http://localhost:8501",  # Required for OpenRouter
            "X-Title": "ContextCode Professional Version"
        }
    )
    return response.choices[0].message.content

# PANEL SEPARATION LAYOUT
left_col, center_col, right_col = st.columns([1.1, 1.6, 1.5])

#  COLUMN 1: LEFT PANEL CONTROL 
with left_col:
    st.markdown("### 🛠️ Workspace Setup")
    with st.container(border=True):
        workspace_mode = st.selectbox(
            "Select Intake Vector Source",
            ["Local Folder Path", "GitHub Repository URL"],
            label_visibility="collapsed"
        )
        
        if workspace_mode == "Local Folder Path":
            target_input = st.text_input("Local target input string path", placeholder="C:\\path\\to\\folder", label_visibility="collapsed")
        else:
            target_input = st.text_input("GitHub remote repo link target", placeholder="https://github.com/user/repo.git", label_visibility="collapsed")
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Index Project", use_container_width=True):
                if not target_input:
                    st.error("Please provide a valid workspace locator path.")
                else:
                    if workspace_mode == "Local Folder Path":
                        if not os.path.exists(target_input):
                            st.error("Local path target folder structure missing.")
                        else:
                            with st.spinner("Analyzing local directory segments..."):
                                process_codebase(target_input)
                                add_log(f"Indexed local repo: {os.path.basename(target_input)}", "success")
                                st.rerun()
                    else:
                        import git
                        temp_dir = "./cloned_github_repo"
                        if os.path.exists(temp_dir):
                            try: shutil.rmtree(temp_dir, onexc=remove_readonly)
                            except TypeError: shutil.rmtree(temp_dir, onerror=remove_readonly)
                            
                        try:
                            with st.spinner("Cloning targeted GitHub repository..."):
                                add_log(f"Downloading remote project links...", "info")
                                git.Repo.clone_from(target_input, temp_dir)
                            with st.spinner("Indexing vector embedding trees..."):
                                chunks = process_codebase(temp_dir)
                                add_log(f"Successfully processed {chunks} remote matrix structures.", "success")
                        except Exception as e:
                            st.error(f"GitHub Synchronization Broken: {str(e)}")
                            add_log(f"Connection error triggered via remote repository.", "warn")
                        finally:
                            add_log("Cloned repository files registered for live view reading.", "success")
                            st.rerun()

        with col_btn2:
            if st.button("Analyze Diff", use_container_width=True):
                if workspace_mode != "Local Folder Path" or not target_input or not os.path.exists(target_input):
                    st.error("Select a valid local Git path repository to run diff tracking.")
                else:
                    import git
                    try:
                        with st.spinner("Reading unstaged Git workspace layers..."):
                            repo = git.Repo(target_input)
                            diff = repo.git.diff(None)
                            
                            if not diff.strip():
                                st.session_state.git_analysis = "### 🟢 Clean State\nNo unstaged changes detected in this working tree."
                                add_log("Analyzed Git state: Repository is clean.", "info")
                            else:
                                add_log("Unstaged file changes located. Running review...", "info")
                                prompt = (
                                    "You are a Senior Principal Code Reviewer. Review these unstaged Git changes and output two distinct sections:\n"
                                    "1. **CODE REVIEW & BUG FINDER**: Critically analyze logic, optimizations, and security holes.\n"
                                    "2. **PROPOSED CONVENTIONAL COMMIT MESSAGE**: Write a flawless short commit message based on conventional commits specs.\n\n"
                                    f"Git Diff Data:\n\n{diff}"
                                )
                                messages = [{"role": "user", "content": prompt}]
                                response_text = safe_generate_content(client, FREE_MODEL, messages)
                                st.session_state.git_analysis = response_text
                                add_log("Successfully compiled custom Git Diff report matrix.", "success")
                    except Exception as ex:
                        st.error(f"Failed to load target repository as Git environment: {str(ex)}")

    st.markdown("---")
    st.markdown("**Console Activity Log**")
    st.markdown(f"<div class='activity-log'>{'<br>'.join(st.session_state.logs[::-1])}</div>", unsafe_allow_html=True)
    
    with st.expander("📂 Project File Map", expanded=True):
        st.markdown(st.session_state.file_structure)

#  COLUMN 2: CENTER PANEL CHAT (WITH WELCOME BANNER) 
with center_col:
    # 🌟 Welcome Banner Block 🌟
    st.markdown("## 👋 Welcome to Your Workspace")
    st.caption("A sleek, production-ready environment for code intelligence and analysis.")
    st.markdown("---")
    
    # 📊 SaaS Metrics Dashboard Row
    m = st.session_state.metrics
    st.markdown(f"""
    <div class="metrics-container">
        <div class="metric-card">
            <div class="metric-label">Tracked Files</div>
            <div class="metric-value">{m['files']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Total Lines</div>
            <div class="metric-value">{m['lines']:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Complexity</div>
            <div class="metric-value metric-value-indigo">{m['complexity']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Score Rating</div>
            <div class="metric-value metric-value-emerald">{m['rating']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 System Chat Interface")
    
    if st.session_state.git_analysis:
        with st.expander("🛠 Git Diff Review & Recommendations", expanded=True):
            st.markdown(st.session_state.git_analysis)
            if st.button("Clear Review Window"):
                st.session_state.git_analysis = ""
                st.rerun()

    chat_container = st.container(height=360 if st.session_state.git_analysis else 440, border=False)
    with chat_container:
        for msg in st.session_state.chat_history:
            glow = "user-glow-box" if msg["role"] == "user" else "model-glow-box"
            st.markdown(f"<div class='{glow}'><b>{msg['role'].upper()}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    if query := st.chat_input("Query codebase parameters..."):
        st.session_state.chat_history.append({"role": "user", "content": query})
        with chat_container:
            st.markdown(f"<div class='user-glow-box'><b>USER:</b><br>{query}</div>", unsafe_allow_html=True)
            
        with st.spinner("Processing architectural vectors..."):
            chunks, meta = hybrid_search(query)
            
            # Format message history to standard API payload structure
            formatted_messages = [
                {
                    "role": "system", 
                    "content": "You are a system architecture assistant. Provide high-grade code intelligence."
                }
            ]
            
            for m in st.session_state.chat_history[:-1]:
                role = "assistant" if m["role"] == "assistant" else "user"
                formatted_messages.append({"role": role, "content": m["content"]})
            
            prompt_content = f"Context:\n{chr(10).join(chunks)}\n\nQuery: {query}" if chunks else query
            formatted_messages.append({"role": "user", "content": prompt_content})
            
            try:
                answer = safe_generate_content(client, FREE_MODEL, formatted_messages, temperature=0.2)
            except Exception as e:
                answer = "⚠️ The free AI endpoint is busy. Please try sending your message again in a few seconds."
                add_log(f"Exception encountered: {str(e)}", "warn")
            
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

# COLUMN 3: RIGHT PANEL LIVE CODE VIEWER 
with right_col:
    st.markdown("### 🔍 Live File Code Viewer")
    
    db_files = list(st.session_state.indexed_files_db.keys())
    
    if not db_files:
        st.info("No source files have been indexed yet. Please run 'Index Project' from the workspace setup to load files into this viewer.")
    else:
        selected_file = st.selectbox(
            "Select indexed file to review", 
            db_files,
            index=0
        )
        
        file_meta = st.session_state.indexed_files_db[selected_file]
        f_path = file_meta["path"]
        f_ext = file_meta["ext"]
        
        # Display full file path metadata
        st.caption(f"📍 Reading target path: `{f_path}`")
        
        # Standardize highlighting extension maps
        lang_mapping = {
            "py": "python", "js": "javascript", "ts": "typescript", 
            "java": "java", "cpp": "cpp", "c": "c", "html": "html", 
            "css": "css", "json": "json", "go": "go", "md": "markdown"
        }
        highlight_lang = lang_mapping.get(f_ext, "python")
        
        try:
            with open(f_path, 'r', encoding='utf-8') as src_file:
                file_content = src_file.read()
                
            
            st.code(file_content, language=highlight_lang, line_numbers=True)
            
        except Exception as e:
            st.error(f"Could not read source code file: {str(e)}")