# Urza - A "Magic: the Gathering" deck building strategy advisor

> **DISCLAIMER:** This project is currently in development and does not yet generate useful output. The architecture is still being implemented and refined.

A Magic: The Gathering deck-building advisory system that provides strategic recommendations using LLMs and agentic workflow architecture.

## Architecture

The system employs a multi-agent approach:

1. **StrategistAgent:** Analyzes queries, maintains conversation context, and provides MTG strategy recommendations
2. **QueryAgent:** Converts strategy recommendations into Scryfall search queries
3. **CardAdvisorWorkflow:** Orchestrates the entire process using a directed workflow

## Features

- Strategy recommendations based on user queries
- Dynamic query generation for card searches
- Stateful conversation with history management
- Retrieval-augmented generation (RAG) using a knowledge base of MTG rules and strategy
- Clean separation between frontend and backend systems

## Tech Stack

### Backend
- Python
- LangChain for LLM orchestration
- Google Generative AI (Gemini models)
- ChromaDB for vector storage
- FastAPI for REST endpoints
- Scryfall API integration for card data

### Frontend
- Next.js 15
- React 19
- TypeScript
- TailwindCSS
- React Markdown for rendering responses

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google AI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/mtg-strategy-advisor.git
cd mtg-strategy-advisor
```

2. Set up the backend
```bash
cd agentic_flow
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the `/agentic_flow` directory
```
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-1.5-flash-001
TEMPERATURE=0.7
KNOWLEDGE_BASE_DIR=knowledge_base
```

4. Set up the frontend
```bash
cd ../ui
npm install
```

5. Start the backend server
```bash
cd ../agentic_flow
python main.py
```

6. Start the frontend development server
```bash
cd ../ui
npm run dev
```

7. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
mtg-strategy-advisor/
├── agentic_flow/           # Backend
│   ├── agents/             # Agent implementations
│   ├── api/                # FastAPI endpoints
│   ├── prompts/            # LLM prompts
│   ├── services/           # External service integrations
│   ├── utils/              # Utility functions
│   ├── workflows/          # Agent orchestration
│   └── main.py             # Entry point
├── ui/                     # Frontend
│   ├── app/                # Next.js pages
│   │   ├── api/            # API routes
│   │   ├── page.tsx        # Main chat interface
│   │   └── layout.tsx      # App layout
│   └── public/             # Static assets
└── knowledge_base/         # MTG rules and strategy documents
```

## License

[MIT](LICENSE)