from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Query(Base):
    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_name = Column(String(100))
    original_question = Column(String(1000))
    reformulated_query = Column(String(500))
    answer = Column(String(5000))
    confidence_score = Column(Integer)
    source_document = Column(String(200))
    response_time_ms = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'user_name': self.user_name,
            'original_question': self.original_question,
            'reformulated_query': self.reformulated_query,
            'answer': self.answer,
            'confidence_score': self.confidence_score,
            'source_document': self.source_document,
            'response_time_ms': self.response_time_ms
        }
