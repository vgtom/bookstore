from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://user:password@localhost:5432/gutenberg')

engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))