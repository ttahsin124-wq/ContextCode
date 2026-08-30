
# 🧠 ContextCode

**AI-powered codebase intelligence — index, chat with, and review your code, right in the browser.**

ContextCode is a sleek, dark-themed Streamlit application that turns any local folder or GitHub repository into a searchable, chat-ready knowledge base. It indexes your source files into a vector database, lets you ask natural-language questions about your codebase, reviews your uncommitted Git changes with AI, and gives you a live syntax-highlighted file viewer — all in one three-panel dashboard.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python"/> <img src="https://img.shields.io/badge/Streamlit-1.29%2B-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"/> <img src="https://img.shields.io/badge/ChromaDB-0.5.0-purple?style=for-the-badge&logo=chroma" alt="ChromaDB"/> <img src="https://img.shields.io/badge/OpenRouter-API-orange?style=for-the-badge" alt="OpenRouter"/> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/> </p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Workspace Indexing** | Index a local folder *or* clone and index a remote GitHub repository directly from the UI. |
| 🔍 **Semantic Codebase Search** | Uses vector embeddings (ChromaDB) to retrieve the most relevant code chunks for any query. |
| 💬 **AI Chat Interface** | Ask questions about your code in plain English and get context-aware answers powered by an LLM via OpenRouter. |
| 🛠 **Git Diff Analyzer** | Automatically reviews unstaged Git changes, flags bugs/security issues, and drafts a Conventional Commit message. |
| 📊 **Live Metrics Dashboard** | Tracks indexed file count, total lines of code, average complexity, and a code quality score. |
| 🖥 **Live Code Viewer** | Browse and view any indexed file with full syntax highlighting and line numbers. |
| 📜 **System Activity Log** | A console-style live log of every indexing, search, and analysis event. |
| 🎨 **Custom Dark UI** | A polished, hand-styled dark theme built with custom CSS on top of Streamlit. |

---

## 🏗️ Architecture Overview

The app is organized into a **three-column dashboard layout**:

```
┌───────────────────┬────────────────────────────┬──────────────────────┐
│   LEFT PANEL       │       CENTER PANEL         │     RIGHT PANEL      │
│  Workspace Setup   │     Metrics + AI Chat      │   Live Code Viewer   │
│                    │                            │                      │
│ • Local / GitHub   │ • Files / Lines /          │ • File selector      │
│   source selector  │   Complexity / Score       │ • Syntax-highlighted │
│ • Index Project    │ • Chat interface with      │   source code        │
│ • Analyze Diff     │   RAG-powered answers      │                      │
│ • Activity log     │ • Git diff review panel    │                      │
│ • File map         │                            │                      │
└───────────────────┴────────────────────────────┴──────────────────────┘
```

### How indexing & retrieval work

1. **Walk the repo** — `process_codebase()` recursively scans the target folder, skipping `node_modules`, `.git`, `__pycache__`, `venv`, `env`, and `.ipynb_checkpoints`.
2. **Filter by extension** — only `.py .js .ts .java .go .html .css .cpp .c .json .md` files are processed.
3. **Chunk the content** — each file is split into overlapping chunks using LangChain's `RecursiveCharacterTextSplitter` (chunk size 1200, overlap 150).
4. **Embed & store** — chunks are embedded with ChromaDB's default embedding function and stored in a persistent local vector collection (`codebase_explorer_pro`).
5. **Retrieve on query** — `hybrid_search()` queries the vector store for the top matching chunks for any chat message.
6. **Generate an answer** — retrieved chunks + chat history are sent to an LLM through OpenRouter, and the response streams back into the chat panel.

---

## 🧰 Tech Stack

- **[Streamlit](https://streamlit.io/)** — UI framework and app server
- **[ChromaDB](https://www.trychroma.com/)** — persistent local vector database for semantic search
- **[LangChain Text Splitters](https://python.langchain.com/)** — recursive character-based chunking
- **[OpenAI Python SDK](https://github.com/openai/openai-python)** — used as an OpenAI-compatible client
- **[OpenRouter](https://openrouter.ai/)** — LLM gateway/provider (free-tier model)
- **[Tenacity](https://github.com/jd/tenacity)** — automatic retries with exponential backoff for API calls
- **[GitPython](https://gitpython.readthedocs.io/)** — cloning repos and reading Git diffs
- **python-dotenv** — environment variable management

---

## 📦 Requirements

- Python **3.9+**
- Git (installed and available on your system `PATH`, required for the GitHub-repo and diff-analysis features)
- An **OpenRouter API key** ([get one here](https://openrouter.ai/keys))

### Python dependencies

```
streamlit
chromadb
langchain-text-splitters
python-dotenv
tenacity
openai
GitPython
```

Save these into a `requirements.txt` file, or install directly:

```bash
pip install streamlit chromadb langchain-text-splitters python-dotenv tenacity openai GitPython
```

---

## ⚙️ Setup & Installation

1. **Clone this project** (or place `app.py` in your working directory).

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root with your OpenRouter API key:

   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

5. Open your browser at **http://localhost:8501** — the app should be live! 🎉

---

## 🚀 Usage Guide

### 1. Index a workspace
- In the **left panel**, choose **Local Folder Path** or **GitHub Repository URL**.
- Enter the path (e.g. `C:\path\to\folder`) or a repo URL (e.g. `https://github.com/user/repo.git`).
- Click **Index Project** to scan, chunk, and embed the codebase.

### 2. Chat with your codebase
- Head to the **center panel** and type a question into the chat box (e.g. *"Where is the retry logic implemented?"*).
- ContextCode retrieves relevant code chunks and generates a grounded, context-aware answer.

### 3. Review your Git changes
- With a local Git repository indexed, click **Analyze Diff**.
- The app reads your unstaged changes and returns:
  - A **Code Review & Bug Finder** report (logic issues, optimizations, security concerns)
  - A **Proposed Conventional Commit Message**

### 4. Browse indexed files
- In the **right panel**, select any indexed file from the dropdown to view its full source with syntax highlighting.

### 5. Monitor activity
- The **Console Activity Log** at the bottom of the left panel timestamps every indexing, search, and error event in real time.

---

## 📊 Dashboard Metrics

| Metric | Description |
|---|---|
| **Tracked Files** | Number of source files successfully indexed |
| **Total Lines** | Combined line count across all indexed files |
| **Avg Complexity** | A representative complexity score for the indexed codebase |
| **Score Rating** | An overall quality score (%) for the indexed project |

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Yes | Your API key for OpenRouter, used to authenticate LLM chat completions |

---

## 🎨 UI/UX Highlights

- Full **dark-mode** interface with a custom indigo accent palette
- Distinct, color-coded **chat bubbles** for user vs. AI messages
- A terminal-style **activity log console** with color-coded log levels (success / warning / info)
- SaaS-style **metric cards** for at-a-glance project stats
- Fully **responsive three-column layout** for a true "workspace" feel

---
## 🎥 Watch the Demo

<p align="center">
  <a href="https://youtu.be/cpCOdoXYnG0" target="_blank">
    <img src="Screenshot 2026-08-30 124811.png" alt="ContextCode Demo" width="800"/>
  </a>
  <br/>
  <em>👆 Click the image above to watch the full demo on YouTube</em>
</p>

---

## ⚠️ Known Limitations

- The **GitHub Repository** mode clones repos into a local `./cloned_github_repo` directory, which is wiped and re-cloned on each run.
- **Diff Analysis** only works with a locally indexed Git repository (not remote-cloned repos).
- Vector storage is persisted locally in `./chroma_storage` — indexing a new project will clear and replace the existing vector collection.
- The default LLM (`poolside/laguna-m.1:free` via OpenRouter) is a free-tier model and may occasionally be rate-limited or busy; retries are handled automatically but may still fail under heavy load.

---

## 🗺️ Roadmap Ideas

- [ ] Support multiple concurrently indexed projects
- [ ] Add persistent chat history across sessions
- [ ] Support additional file types and custom ignore patterns
- [ ] Add a model picker for choosing between different OpenRouter LLMs
- [ ] Export chat sessions and diff reviews as Markdown/PDF reports

---

## 📄 License

This project currently has no explicit license. Add a `LICENSE` file (MIT, Apache 2.0, etc.) if you plan to share or distribute it.

---

## 🙌 Acknowledgements

Built with ❤️ using Streamlit, ChromaDB, LangChain, and OpenRouter.

> *ContextCode — turn any codebase into a conversation.*
