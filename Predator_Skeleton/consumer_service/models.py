from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql+mysqlconnector://root:password@mysql:3306/quotes_db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    author = Column(String(100))
    tags = Column(String(200))

Base.metadata.create_all(engine)
