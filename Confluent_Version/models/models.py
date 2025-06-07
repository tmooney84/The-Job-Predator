from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os
# Define Base

Base = declarative_base()
class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    author = Column(String(100))
    tags = Column(String(200))
    
    def to_dict(self):
        return {
            'id' : self.id,
            'text' : self.text,
            'author' : self.author,
            'tags' : self.tags
        }
    @staticmethod
    def build_engine():
        DATABASE_URL = os.environ["DATABASE_URL"]
        engine = create_engine(DATABASE_URL, echo=True)
        SessionFactory = sessionmaker(bind=engine)
        
        return SessionFactory
        
