from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler

from database import engine, get_db
from models import Base, Quiz
from scraper import scrape_wikipedia
from llm import generate_quiz_from_text, generate_related_topics
from utils import extract_json
from cleanup import delete_old_quizzes

app = FastAPI(title="AI Wikipedia Quiz Generator")


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_quizzes, "interval", days=1)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# ---------------- SCHEMAS ---------------- #

class UrlRequest(BaseModel):
    url: str

# ---------------- ROUTES ---------------- #

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.post("/generate-quiz")
def generate_quiz(data: UrlRequest, db: Session = Depends(get_db)):
    try:
        scraped = scrape_wikipedia(data.url)

        quiz_text = generate_quiz_from_text(scraped["content"])
        quiz_json = extract_json(quiz_text)

        topics_text = generate_related_topics(scraped["content"])
        related_topics = extract_json(topics_text)

        quiz = Quiz(
            url=data.url,
            title=scraped["title"],
            summary=scraped["summary"],
            sections=scraped["sections"],
            quiz_data=quiz_json,
            related_topics=related_topics
        )

        db.add(quiz)
        db.commit()
        db.refresh(quiz)

        return {
            "id": quiz.id,
            "url": quiz.url,
            "title": quiz.title,
            "summary": quiz.summary,
            "sections": quiz.sections,
            "quiz": quiz.quiz_data,
            "related_topics": quiz.related_topics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quizzes")
def get_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).order_by(Quiz.created_at.desc()).all()


@app.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": quiz.id,
        "url": quiz.url,
        "title": quiz.title,
        "summary": quiz.summary,
        "sections": quiz.sections,
        "quiz": quiz.quiz_data,
        "related_topics": quiz.related_topics
    }
