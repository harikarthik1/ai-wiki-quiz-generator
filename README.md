#  AI Wikipedia Quiz Generator

An end-to-end web application that accepts a Wikipedia article URL and automatically generates an interactive quiz using a Large Language Model (Gemini).  
The system scrapes Wikipedia HTML content, generates structured quiz questions, stores results in PostgreSQL, and provides a clean UI with history and quiz-taking functionality.

---

## 🚀 Tech Stack

### Frontend
- React (Vite)
- HTML, CSS, JavaScript

### Backend
- Python
- FastAPI
- SQLAlchemy
- APScheduler

### Database
- PostgreSQL

### AI / LLM
- Google Gemini (Free Tier)
- Prompt-based generation (JSON enforced)

### Scraping
- Requests
- BeautifulSoup (HTML scraping only, no Wikipedia API)

---

## ✨ Features

### 🔹 Generate Quiz (Tab 1)
- Accepts any valid Wikipedia article URL
- Scrapes article content
- Generates **5 quiz questions** with:
  - 4 options each
  - Correct answer
  - Explanation
  - Difficulty level (Easy / Medium / Hard)
- Interactive **Take Quiz mode**
- Score shown after submission

### 🔹 Past Quizzes (Tab 2)
- Lists all previously generated quizzes
- Stored in PostgreSQL
- View quiz details in a modal
- Reuses the same quiz UI

### 🔹 Data Retention
- Automatic cleanup of old quizzes
- Configurable retention period (default: 7 days)

---

## 🧠 LLM Prompt Design

### Quiz Generation Prompt
- Forces **strict JSON output**
- Enforces difficulty distribution:
  - 2 Easy
  - 2 Medium
  - 1 Hard
- Uses only scraped article content to minimize hallucination

### Related Topics Prompt
- Generates 3–5 related Wikipedia topics
- JSON array only

Prompts are implemented in `llm.py`.

---

## 🗄️ Database Schema

### Table: `quizzes`

| Column | Type |
|------|-----|
| id | Integer (PK) |
| url | String |
| title | String |
| summary | String |
| sections | JSON |
| quiz_data | JSON |
| related_topics | JSON |
| created_at | DateTime |

---

## 🔌 API Endpoints

### POST `/generate-quiz`
Generates a quiz for a Wikipedia URL.

**Request**
```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
