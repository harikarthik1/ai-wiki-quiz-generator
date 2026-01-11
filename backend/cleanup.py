from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Quiz

RETENTION_DAYS = 7

def delete_old_quizzes():
    db: Session = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
        deleted = db.query(Quiz).filter(Quiz.created_at < cutoff).delete()
        db.commit()
        print(f"[CLEANUP] Deleted {deleted} old quizzes")
    finally:
        db.close()
