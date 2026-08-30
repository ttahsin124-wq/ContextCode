🚀 ContextCode – AI-Powered Code Intelligence & Workspace Analysis
ContextCode is a sleek, professional-grade Streamlit application that transforms your codebase into an intelligent, conversational workspace. Powered by ChromaDB vector storage and OpenRouter’s free LLM (poolside/laguna-m.1), it lets you chat with your code, analyze Git diffs, and explore every file in real-time—all from a polished, dark‑themed dashboard.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python"/> <img src="https://img.shields.io/badge/Streamlit-1.29%2B-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"/> <img src="https://img.shields.io/badge/ChromaDB-0.5.0-purple?style=for-the-badge&logo=chroma" alt="ChromaDB"/> <img src="https://img.shields.io/badge/OpenRouter-API-orange?style=for-the-badge" alt="OpenRouter"/> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/> </p>
✨ Features
🔍 Smart Code Indexing – Recursively parse .py, .js, .ts, .java, .go, .html, .css, .cpp, .c, .json, .md files, chunk them intelligently, and store embeddings in ChromaDB.

💬 Chat with Your Codebase – Ask natural-language questions; the app retrieves relevant code snippets and feeds them to the LLM for context‑aware answers.

🛠 Git Diff Analysis – Point to a local Git repository, analyze unstaged changes, and get a professional code review plus a conventional‑commit message suggestion.

📂 Live File Viewer – Browse any indexed file directly in the UI with syntax highlighting and line numbers.

📊 Dashboard Metrics – Track number of files, total lines, average complexity, and a quality rating at a glance.

📝 Activity Log – Real‑time console logs keep you informed about indexing, cloning, and analysis steps.

⚡ Production‑ready UI – Dark, enterprise‑grade design with a responsive layout and elegant chat bubbles.

🖼️ Screenshots
Add your own screenshots here (place them in a screenshots/ folder and reference them).

Dashboard & Chat	File Viewer
https://screenshots/dashboard.png	https://screenshots/fileviewer.png
📦 Installation
1. Clone the Repository
bash
git clone https://github.com/ttahsin124-wq/ContextCode.git
cd ContextCode
2. Create & Activate a Virtual Environment
bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
If you don’t have requirements.txt yet, install the essential packages:

bash
pip install streamlit chromadb langchain-text-splitters python-dotenv tenacity openai GitPython
4. Set Up Environment Variables
Create a .env file in the project root with your OpenRouter API key:

env
OPENROUTER_API_KEY=your-api-key-here
Get your free API key from OpenRouter.

🚀 Usage
Start the app with:

bash
streamlit run app.py
🔧 Workflow
Index a Codebase

Choose Local Folder Path or GitHub Repository URL.

Enter the path/URL and click Index Project.

The app will parse, chunk, and embed your files into ChromaDB.

Chat with the Code

Type your query (e.g., “Find all database connection functions”).

The system retrieves relevant code chunks and generates a context‑aware response.

Analyze Git Diffs

Select Local Folder Path and provide a Git‑tracked local path.

Click Analyze Diff to get an AI‑powered code review and commit message suggestion.

View Source Files

In the right panel, pick any indexed file to see its content with syntax highlighting.

📁 Project Structure
text
ContextCode/
├── app.py                 # Main application
├── .env                   # Environment variables (ignored)
├── .gitignore             # Ignored files
├── chroma_storage/        # ChromaDB persistent storage (ignored)
├── cloned_github_repo/    # Temporary clone destination (ignored)
└── README.md
🧠 How It Works
Indexing: Files are read, chunked via RecursiveCharacterTextSplitter, and stored in ChromaDB with metadata.

Retrieval: On a user query, the collection is queried for the most relevant chunks (hybrid search).

LLM Integration: The retrieved context is combined with the conversation history and sent to the OpenRouter API (free model poolside/laguna-m.1:free). The response is streamed back to the chat.

Git Diff: A local Git repository’s unstaged changes are diffed and passed to the LLM for analysis.

🛠 Dependencies
Streamlit – UI framework

ChromaDB – Vector database

LangChain Text Splitters – Chunking

OpenAI Python Client – OpenRouter API client

Tenacity – Retry logic for API calls

GitPython – Git operations

python-dotenv – Environment variable management

🔒 Security
API Key: Stored in .env and never committed to the repository (already in .gitignore).

Temporary Clones: GitHub repositories are cloned locally and cleaned up after indexing.

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgements
OpenRouter for providing free LLM access.

ChromaDB for the vector database.

Streamlit for making Python app development a breeze.

Happy Coding! 👨‍💻👩‍💻

this is tghe text but this is not giving newline or correct space or any thing ..can you provide me full in correct
We need to produce a properly formatted README.md file with Markdown syntax, not plain text. The user said the text doesn't have newlines or spaces; they want a correct Markdown README. We should format it with proper headings, bullet lists, code blocks, etc. Based on the prior conversation, we already provided a Markdown README. The user is showing a text file that seems to be a copy-paste of the README content but without proper formatting. They want "full in correct" meaning properly formatted.

We should provide a complete README.md file content in a code block that they can copy and paste into a file named README.md. We'll reuse the one we wrote earlier, but ensure it's well-formatted and includes all sections. We might also add a few things like badges, installation instructions, etc. We can also add a note about the .env and .gitignore as per their project.

We'll deliver a full Markdown block with proper syntax. We'll also include instructions for creating the .env file, and a note about the required API key.

Let's produce that. Also note the user's project uses OpenRouter with a free model, so we mention that.

We'll include the license as MIT, even though no LICENSE file exists yet; we can mention that.

We'll also mention that they should add a LICENSE file if they want.

I'll produce a comprehensive README.md with all necessary sections.

Let's do that.

🚀 ContextCode – AI-Powered Code Intelligence & Workspace Analysis
ContextCode is a sleek, professional-grade Streamlit application that transforms your codebase into an intelligent, conversational workspace. Powered by ChromaDB vector storage and OpenRouter’s free LLM (poolside/laguna-m.1:free), it lets you chat with your code, analyze Git diffs, and explore every file in real-time—all from a polished, dark‑themed dashboard.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python"/> <img src="https://img.shields.io/badge/Streamlit-1.29%2B-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"/> <img src="https://img.shields.io/badge/ChromaDB-0.5.0-purple?style=for-the-badge&logo=chroma" alt="ChromaDB"/> <img src="https://img.shields.io/badge/OpenRouter-API-orange?style=for-the-badge" alt="OpenRouter"/> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/> </p>
✨ Features
🔍 Smart Code Indexing – Recursively parse .py, .js, .ts, .java, .go, .html, .css, .cpp, .c, .json, .md files, chunk them intelligently, and store embeddings in ChromaDB.

💬 Chat with Your Codebase – Ask natural‑language questions; the app retrieves relevant code snippets and feeds them to the LLM for context‑aware answers.

🛠 Git Diff Analysis – Point to a local Git repository, analyze unstaged changes, and get a professional code review plus a conventional‑commit message suggestion.

📂 Live File Viewer – Browse any indexed file directly in the UI with syntax highlighting and line numbers.

📊 Dashboard Metrics – Track number of files, total lines, average complexity, and a quality rating at a glance.

📝 Activity Log – Real‑time console logs keep you informed about indexing, cloning, and analysis steps.

⚡ Production‑ready UI – Dark, enterprise‑grade design with a responsive layout and elegant chat bubbles.

🖼️ Screenshots
Add your own screenshots here (place them in a screenshots/ folder and reference them).

Dashboard & Chat	File Viewer
https://screenshots/dashboard.png	https://screenshots/fileviewer.png
📦 Installation
1. Clone the Repository
bash
git clone https://github.com/ttahsin124-wq/ContextCode.git
cd ContextCode
2. Create & Activate a Virtual Environment
bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
If you don’t have requirements.txt yet, install the essential packages:

bash
pip install streamlit chromadb langchain-text-splitters python-dotenv tenacity openai GitPython
4. Set Up Environment Variables
Create a .env file in the project root with your OpenRouter API key:

env
OPENROUTER_API_KEY=your-api-key-here
Get your free API key from OpenRouter.

🚀 Usage
Start the app with:

bash
streamlit run app.py
🔧 Workflow
Index a Codebase

Choose Local Folder Path or GitHub Repository URL.

Enter the path/URL and click Index Project.

The app will parse, chunk, and embed your files into ChromaDB.

Chat with the Code

Type your query (e.g., “Find all database connection functions”).

The system retrieves relevant code chunks and generates a context‑aware response.

Analyze Git Diffs

Select Local Folder Path and provide a Git‑tracked local path.

Click Analyze Diff to get an AI‑powered code review and commit message suggestion.

View Source Files

In the right panel, pick any indexed file to see its content with syntax highlighting.

📁 Project Structure
text
ContextCode/
├── app.py                 # Main application
├── .env                   # Environment variables (ignored by Git)
├── .gitignore             # Ignored files list
├── chroma_storage/        # ChromaDB persistent storage (ignored)
├── cloned_github_repo/    # Temporary clone destination (ignored)
└── README.md              # This file
🧠 How It Works
Indexing: Files are read, chunked via RecursiveCharacterTextSplitter, and stored in ChromaDB with metadata.

Retrieval: On a user query, the collection is queried for the most relevant chunks (hybrid search).

LLM Integration: The retrieved context is combined with the conversation history and sent to the OpenRouter API (free model poolside/laguna-m.1:free). The response is streamed back to the chat.

Git Diff: A local Git repository’s unstaged changes are diffed and passed to the LLM for analysis.

🛠 Dependencies
Streamlit – UI framework

ChromaDB – Vector database

LangChain Text Splitters – Chunking

OpenAI Python Client – OpenRouter API client

Tenacity – Retry logic for API calls

GitPython – Git operations

python-dotenv – Environment variable management

🔒 Security
API Key: Stored in .env and never committed to the repository (already in .gitignore).

Temporary Clones: GitHub repositories are cloned locally and cleaned up after indexing.

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgements
OpenRouter for providing free LLM access.

ChromaDB for the vector database.

Streamlit for making Python app development a breeze.

Happy Coding! 👨‍💻👩‍💻
