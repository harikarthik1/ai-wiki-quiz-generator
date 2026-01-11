from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String)
    sections = Column(JSON)
    quiz_data = Column(JSON, nullable=False)
    related_topics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
