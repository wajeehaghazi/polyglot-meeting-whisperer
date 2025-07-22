# 🌐 Polyglot Meeting Whisperer

Polyglot Meeting Whisperer is a real-time meeting assistant that captures microphone audio in chunks, transcribes it, translates it, summarizes it, generates questions and extracts & explains buzz keywords — all using AI agents.

## 🧠 Project Overview

```mermaid
graph LR
    A[Frontend] -->|Audio Stream| B[WebSocket]
    B --> C[Backend]
    C -->|Transcribed Data| A
    C -->|Translated Content| A
    C -->|Meeting Insights| A
```

### ✨ Core Features
- 🎧 **Real-time Audio Transcription**
- 🌍 **Multilingual Translation**
- 📝 **AI-Powered Summarization**
- 🔑 **Keyword Extraction & Explanation**
- ❓ **Intelligent Question Generation**

## 👥 Team Members
| Name                   | Role               |
|------------------------|--------------------|
| Abbas Al-Kaisi         | AI + Full Stack Lead |
| Gabriel Calderon       | Project Lead       |
| Wajeeha Ghazi          | UI-UX Designer     |
| Khadeeja               | Documentation Lead |
| Muhammad Faizan Soomro | Full Stack + AI Lead |
| Muhammad Jasim         | AI Specialist      |
| Muhammad Abdullah Bilal| Frontend Developer |
| Fawad Malik            | AI Specialist      |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Groq API key

### Installation
1. Clone the repository:
```bash
git clone https://github.com/wajeehaghazi/polyglot-meeting-whisperer.git
cd polyglot-meeting-whisperer
```

2. Set up backend component:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Backend .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

4. Run the system:
```bash
# In separate terminals:
# Terminal 1 - Start backend
python websocket_server.py

# Terminal 2 - Start frontend
python -m http.server
```

## 🌟 Key Features Deep Dive

### 🤖 AI-Powered Processing Pipeline
```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    Frontend->>Backend: Audio Chunk (5s)
    Backend->>Whisper: Transcribe audio
    Whisper->>Backend: Raw text
    Backend->>Llama3: Process text
    Llama3->>Backend: Insights (translation/summary/etc)
    Backend->>Frontend: Processed data
```

### ⚡ Real-Time Performance
- 5-second audio chunk processing
- Parallel agent execution
- WebSocket streaming
- Low-latency responses (200-500ms)

### 📊 Data Flow Architecture
```mermaid
graph TD
    A[Microphone] --> B[Frontend]
    B -->|WebSocket| C[Backend]
    C --> D[Transcription Agent]
    C --> E[Translation Agent]
    C --> F[Keyword Agent]
    C --> G[Summary Agent]
    C --> H[Question Agent]
    D --> I((Whisper))
    E --> J((Llama3))
    F --> K((Llama3))
    G --> L((Llama3))
    H --> M((Llama3))
    I --> N[Frontend]
    J --> N
    K --> N
    L --> N
    M --> N
```

## 📜 License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
