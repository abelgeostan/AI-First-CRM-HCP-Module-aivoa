# AI-Powered HCP Interaction Logging Assistant

An AI-powered CRM assistant for logging, editing, searching, and managing Healthcare Professional (HCP) interactions using natural language. The application uses a FastAPI backend powered by LangGraph and Groq LLM, with a React frontend.

---

## Features

- Log HCP interactions using natural language
- AI extracts structured information into a form
- Edit existing interaction logs
- Search interaction logs
- Soft delete interaction logs
- AI-generated follow-up suggestions
- Conversation memory using LangGraph

---

## Tech Stack

### Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Groq (Llama 3.1 8B Instant)
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker Compose
- uv

### Frontend

- React
- Redux Toolkit
- Tailwind CSS
- Axios
- Vite

---

# Project Structure

```
.
├── client/
├── server/
├── docker-compose.yml
└── README.md
```

---

# Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- uv

---

# Backend Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd Log-HCP-Interaction-Aivoaai
```

---

## 2. Configure Environment Variables

Inside the `server` directory:

```bash
cp .env.example .env
```

Update the values inside `.env`:

- `DATABASE_URL`
- `GROQ_API_KEY`

---

## 3. Install Dependencies

```bash
cd server

uv sync
```

---

## 4. Start PostgreSQL

```bash
docker compose up -d
```

---

## 5. Run Database Migrations

```bash
uv run alembic upgrade head
```

---

## 6. Start the Backend

```bash
uv run uvicorn main:app --reload
```

Backend:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Open another terminal.

```bash
cd client
```

Copy the environment file.

```bash
cp .env.example .env
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# API Endpoint

### POST

```
/api/chat
```

Example Request

```json
{
  "message": "Today I met Dr. Sarah Johnson. We discussed CardioPlus and I shared a brochure.",
  "thread_id": "session_001",
  "current_log_id": null
}
```

---

# Example Prompts

### Create Interaction

```
Today I met Dr. Sarah Johnson. We discussed CardioPlus for hypertension management. She was interested in the latest clinical trial results and I shared a product brochure.
```

### Edit Interaction

```
Change the interaction type to Call and update the sentiment to Positive.
```

### Search

```
Search for Sarah
```

### Delete

```
I want to delete an interaction log.
```

### Confirm Delete

```
confirm delete 1
```

---

# AI Capabilities

- Natural language interaction logging
- Structured information extraction
- Intelligent record editing
- Semantic search
- Follow-up recommendation generation
- Conversation memory with LangGraph

---

# Future Improvements

- User authentication
- Persistent conversation memory
- Dashboard & analytics
- Advanced filtering
- Export reports
- File attachments
