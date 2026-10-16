# 📄 Linguistic PDF Bot

An intelligent, full-stack **PDF-powered conversational voice assistant** built with FastAPI, LangGraph, and React. Upload PDFs to build a personal knowledge base, then interact with your documents through natural voice conversations — powered by RAG (Retrieval-Augmented Generation), real-time ASR, and neural TTS.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎙️ **Voice-First Interaction** | Real-time speech-to-text (Groq Whisper) and text-to-speech (Murf AI) for hands-free PDF querying |
| 📄 **PDF Knowledge Ingestion** | Upload PDFs that are chunked, embedded, and stored in Qdrant for semantic retrieval |
| 🤖 **LangGraph Agentic RAG** | Multi-step reasoning agent with tool-use — autonomously searches your documents to answer questions |
| 🧠 **Session Memory** | Conversation context persists across turns using LangGraph's memory checkpointing |
| 🔐 **User Authentication** | Clerk-powered auth with per-user document isolation and personalized personas |
| 🗄️ **Supabase Backend** | User profiles, custom personas, and session management stored in Supabase |
| ⚡ **Real-time WebSocket** | Low-latency streaming pipeline for voice → transcription → LLM → TTS → playback |
| 🎯 **Interruptible Turns** | Users can interrupt bot responses mid-speech for natural conversation flow |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React + Vite)              │
│  ┌──────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │ Clerk    │  │ Voice Input   │  │ Animated UI          │  │
│  │ Auth     │  │ (VAD)         │  │ (Pulsing/Blob Anim)  │  │
│  └──────────┘  └───────┬───────┘  └──────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │ WebSocket
┌─────────────────────────┼───────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────┐  ┌───────┴───────┐  ┌──────────────────────┐  │
│  │ Groq     │  │ LangGraph     │  │ Murf TTS             │  │
│  │ Whisper  │  │ Agent + RAG   │  │ (Neural Voice)       │  │
│  │ (ASR)    │  │ + Tools       │  │                      │  │
│  └──────────┘  └───────┬───────┘  └──────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────┴─────────────────────────────────┐  │
│  │              Qdrant Vector DB (PDF Embeddings)         │  │
│  │              + Supabase (User Data & Sessions)         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Linguistic-PDF-Bot/
├── agentic_chatbot/               # Python backend
│   ├── app.py                     # FastAPI application entry point
│   ├── main.py                    # Uvicorn server launcher
│   ├── config.py                  # Environment variables & model config
│   ├── websocket_handler.py       # WebSocket connection & message routing
│   ├── llm_service.py             # LangGraph agent graph construction
│   ├── rag_service.py             # Qdrant vector search & RAG tool
│   ├── document_service.py        # PDF upload, parsing & chunking pipeline
│   ├── audio_services.py          # Groq ASR & Murf TTS integration
│   ├── auth.py                    # Clerk JWT authentication middleware
│   ├── custom_supabase.py         # Supabase client for user/session data
│   ├── custom_endpoints.py        # REST API routes for persona management
│   ├── requirements.txt           # Python dependencies
│   └── pyproject.toml             # Project metadata & build config
│
├── frontend/                      # React frontend (Vite)
│   ├── src/                       # Source code (pages, hooks, utils)
│   ├── components/                # Reusable UI components
│   ├── context/                   # React context providers
│   ├── lib/                       # Utility libraries
│   ├── public/                    # Static assets
│   ├── index.html                 # HTML entry point
│   ├── package.json               # Node.js dependencies
│   └── vite.config.js             # Vite build configuration
│
├── README.md                      # This file
└── CONTRIBUTING.md                # Contribution guidelines
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker (for Qdrant) or Qdrant Cloud account
- API keys: Groq, Murf AI, Gemini, Clerk, Supabase

### 1. Clone the Repository

```bash
git clone https://github.com/wrathog12/Linguistic-PDF-Bot.git
cd Linguistic-PDF-Bot
```

### 2. Backend Setup

```bash
cd agentic_chatbot
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
MURF_API_KEY=your_murf_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file:

```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key
VITE_BACKEND_URL_WEBSOCKET=ws://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

The app will be available at **http://localhost:5173**

### 4. Qdrant Vector Database

Start Qdrant locally with Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or configure a Qdrant Cloud endpoint in your environment.

---

## 💡 Usage

### Authenticated Users
1. Sign in via Clerk authentication
2. Upload PDF documents through the upload interface
3. Click **"Start"** to begin a voice conversation
4. Ask questions about your uploaded documents — the agent will search your knowledge base
5. Session summaries are automatically saved for conversation continuity

### Anonymous Users
- Click **"Start"** without signing in for general conversational AI
- Full voice capabilities work, but no PDF knowledge base or session persistence

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React, Vite, Clerk Auth |
| **Backend** | FastAPI, Python 3.12 |
| **LLM** | Gemini 2.0 Flash (via OpenAI-compatible API) |
| **Agent Framework** | LangGraph (StateGraph + ToolNode) |
| **ASR** | Groq Whisper Large v3 Turbo |
| **TTS** | Murf AI (Neural Voices) |
| **Embeddings** | Nomic Embed Text v1.5 (HuggingFace) |
| **Vector DB** | Qdrant (Cosine Similarity) |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Clerk |

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| WebSocket connection errors | Ensure backend is running on port 8000 |
| Groq API errors | Verify API key and check usage limits |
| Murf TTS failures | Confirm Murf API key and account status |
| Qdrant connection refused | Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant` |
| Supabase issues | Double-check URL and anon key in `.env` |
| Clerk auth not working | Verify publishable key in frontend `.env` |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
