import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from .models import Base, Query
from datetime import datetime, timedelta

DATABASE_URL = "sqlite:///../data/customer_service.db"

def init_db():
    """Initialize database"""
    os.makedirs("../data", exist_ok=True)
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def save_query(user_name, original_question, reformulated_query,
               answer, confidence_score, source_document, response_time_ms):
    """Save query to database"""
    session = get_session()
    query = Query(
        user_name=user_name,
        original_question=original_question,
        reformulated_query=reformulated_query,
        answer=answer,
        confidence_score=confidence_score,
        source_document=source_document,
        response_time_ms=response_time_ms
    )
    session.add(query)
    session.commit()
    session.close()

def get_statistics():
    """Get dashboard statistics"""
    session = get_session()

    # Total queries
    total_queries = session.query(Query).count()

    # Average confidence
    avg_confidence = session.query(func.avg(Query.confidence_score)).scalar() or 0

    # Queries by user
    user_stats = session.query(
        Query.user_name,
        func.count(Query.id).label('query_count'),
        func.avg(Query.confidence_score).label('avg_confidence')
    ).group_by(Query.user_name).all()

    # Most used documents
    doc_stats = session.query(
        Query.source_document,
        func.count(Query.id).label('usage_count')
    ).group_by(Query.source_document).all()

    # Low confidence queries
    low_confidence = session.query(Query).filter(
        Query.confidence_score < 70
    ).order_by(Query.timestamp.desc()).limit(10).all()

    # Average response time
    avg_response_time = session.query(func.avg(Query.response_time_ms)).scalar() or 0

    session.close()

    return {
        'total_queries': total_queries,
        'avg_confidence': round(avg_confidence, 1),
        'active_reps': len(user_stats),
        'avg_response_time': round(avg_response_time, 0),
        'user_stats': [
            {
                'name': stat[0],
                'query_count': stat[1],
                'avg_confidence': round(stat[2], 1)
            } for stat in user_stats
        ],
        'document_stats': [
            {
                'document': stat[0],
                'usage_count': stat[1]
            } for stat in doc_stats
        ],
        'low_confidence_queries': [q.to_dict() for q in low_confidence]
    }
