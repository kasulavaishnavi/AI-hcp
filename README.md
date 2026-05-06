AI-First CRM HCP Module
Overview
AI-powered CRM system for Healthcare Professional (HCP) interaction logging using conversational AI and structured forms.

The application allows users to:
- Log HCP interactions using natural language
- Extract structured interaction data using AI
- Edit interactions
- Generate follow-up suggestions
- Summarize interactions
- Reset and submit records

The project uses LangGraph for workflow orchestration and Groq LLM for AI-based entity extraction.

Tech Stack
Frontend
- React.js
- Redux Toolkit
- CSS

Backend
- Python
- FastAPI
- LangGraph
- Groq LLM
- SQLite

Features
- Conversational AI interaction logging
- Structured CRM interaction form
- AI-based field extraction
- AI-generated follow-up suggestions
- Interaction summarization
- Edit, reset, and submit functionality
- Redux state management
- SQLite database integration

LangGraph Workflow
User Input
   ↓
LangGraph Agent Node
   ↓
Groq LLM Extraction
   ↓
Tool Routing Node
   ↓
CRM Tool Execution

AI Tools
Log Interaction Tool
Edit Interaction Tool
Summarize Interaction Tool
Suggest Follow-up Tool
Reset Interaction Tool
Submit Interaction Tool

Run Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

Create .env file:
GROQ_API_KEY=your_api_key

Backend runs on:
http://127.0.0.1:8000

--Run Frontend
cd frontend
npm install
npm start

Frontend runs on:
http://localhost:3000
