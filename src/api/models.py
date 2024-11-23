from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for books and authors
books_book_authors = Table(
    'books_book_authors',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('author_id', Integer, ForeignKey('books_author.id'))
)

# Association table for books and bookshelves
books_book_bookshelves = Table(
    'books_book_bookshelves',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('bookshelf_id', Integer, ForeignKey('books_bookshelf.id'))
)

# Association table for books and subjects
books_book_subjects = Table(
    'books_book_subjects',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('subject_id', Integer, ForeignKey('books_subject.id'))
)

# Association table for books and languages
books_book_languages = Table(
    'books_book_languages',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('language_id', Integer, ForeignKey('books_language.id'))
)

class Book(Base):
    __tablename__ = 'books_book'

    id = Column(Integer, primary_key=True)
    download_count = Column(Integer, CheckConstraint('download_count >= 0'))
    gutenberg_id = Column(Integer, CheckConstraint('gutenberg_id >= 0'), nullable=False)
    media_type = Column(String(16), nullable=False)
    title = Column(String(1024))
    
    authors = relationship("Author", secondary=books_book_authors, backref="books")
    bookshelves = relationship("Bookshelf", secondary=books_book_bookshelves, backref="books")
    subjects = relationship("Subject", secondary=books_book_subjects, backref="books")
    languages = relationship("Language", secondary=books_book_languages, backref="books")
    formats = relationship("Format", backref="book")

class Author(Base):
    __tablename__ = 'books_author'

    id = Column(Integer, primary_key=True)
    birth_year = Column(SmallInteger)
    death_year = Column(SmallInteger)
    name = Column(String(128), nullable=False)

class Bookshelf(Base):
    __tablename__ = 'books_bookshelf'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

class Subject(Base):
    __tablename__ = 'books_subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

class Language(Base):
    __tablename__ = 'books_language'

    id = Column(Integer, primary_key=True)
    code = Column(String(4), nullable=False)

class Format(Base):
    __tablename__ = 'books_format'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)
    mime_type = Column(String(32), nullable=False)
    url = Column(String(256), nullable=False)