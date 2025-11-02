from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Setting Up database
DATABASE_URL = "sqlite:///./analysis_log.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    #Defining columns
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    raw_resume_text = Column(Text)
    raw_job_text = Column(Text)
    gaps_analysis = Column(JSON)
    response_to_resume = Column(JSON)

def get_database():
    """
    This function creates a database session for each API request
    and ensures its closed after
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Creating database
Base.metadata.create_all(bind=engine)