from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from api.models import (
    Book, Author, Subject, Bookshelf, Format, Language,
    books_book_authors, books_book_subjects, books_book_bookshelves, books_book_languages
)
from database.db import db_session

api = Blueprint('api', __name__)

BOOKS_PER_PAGE = 25

@api.route('/books', methods=['GET'])
def get_books():
    try:
        # Get query parameters
        book_ids = [int(id.strip()) for id in request.args.get('book_ids', '').split(',') if id.strip().isdigit()]
        languages = [lang.strip() for lang in request.args.get('language', '').split(',') if lang.strip()]
        mime_types = [mime.strip() for mime in request.args.get('mime_type', '').split(',') if mime.strip()]
        topics = [topic.strip() for topic in request.args.get('topic', '').split(',') if topic.strip()]
        authors = [author.strip() for author in request.args.get('author', '').split(',') if author.strip()]
        titles = [title.strip() for title in request.args.get('title', '').split(',') if title.strip()]
        
        try:
            page = max(1, int(request.args.get('page', 1)))
        except ValueError:
            page = 1

        # Build query
        query = db_session.query(Book).distinct()

        # Apply filters
        if book_ids:
            query = query.filter(Book.gutenberg_id.in_(book_ids))
        
        if languages:
            query = (query
                    .join(books_book_languages)
                    .join(Language)
                    .filter(Language.code.in_([lang.lower() for lang in languages])))
        
        if mime_types:
            query = query.join(Format).filter(Format.mime_type.in_(mime_types))
        
        if topics:
            topic_filters = []
            for topic in topics:
                topic_filter = or_(
                    Subject.name.ilike(f'%{topic}%'),
                    Bookshelf.name.ilike(f'%{topic}%')
                )
                topic_filters.append(topic_filter)
            
            query = (query
                    .join(books_book_subjects)
                    .join(Subject)
                    .join(books_book_bookshelves)
                    .join(Bookshelf)
                    .filter(or_(*topic_filters)))
        
        if authors:
            author_filters = []
            for author_name in authors:
                author_filters.append(Author.name.ilike(f'%{author_name}%'))
            
            query = (query
                    .join(books_book_authors)
                    .join(Author)
                    .filter(or_(*author_filters)))
        
        if titles:
            title_filters = []
            for title in titles:
                title_filters.append(Book.title.ilike(f'%{title}%'))
            query = query.filter(or_(*title_filters))

        # Order by download count
        query = query.order_by(Book.download_count.desc())

        # Get total count and calculate pages
        total_books = query.count()
        total_pages = (total_books + BOOKS_PER_PAGE - 1) // BOOKS_PER_PAGE

        # Apply pagination
        query = query.offset((page - 1) * BOOKS_PER_PAGE).limit(BOOKS_PER_PAGE)

        # Format response
        books = []
        for book in query.all():
            # Get the primary author (first one)
            author_data = None
            if book.authors:
                primary_author = book.authors[0]
                author_data = {
                    'name': primary_author.name,
                    'birth_year': primary_author.birth_year,
                    'death_year': primary_author.death_year
                }

            # Infer genre from subjects more comprehensively
            genre = None
            genre_keywords = {
                'Fiction': ['fiction', 'novel', 'story', 'stories'],
                'Poetry': ['poetry', 'poems', 'verse'],
                'Drama': ['drama', 'play', 'theater'],
                'Biography': ['biography', 'biographical', 'memoirs'],
                'History': ['history', 'historical'],
                'Science': ['science', 'scientific'],
                'Philosophy': ['philosophy', 'philosophical'],
                'Religion': ['religion', 'religious', 'theology'],
                'Reference': ['manual', 'guide', 'handbook', 'dictionary'],
                'Children': ['children', 'juvenile']
            }
            
            for subject in book.subjects:
                subject_lower = subject.name.lower()
                # First check for explicit genre mentions
                if '(literary genre)' in subject_lower:
                    genre = subject.name.split('(')[0].strip()
                    break
                # Then check for genre keywords
                for genre_name, keywords in genre_keywords.items():
                    if any(keyword in subject_lower for keyword in keywords):
                        genre = genre_name
                        break
                if genre:
                    break

            # Get language codes
            language_codes = [lang.code for lang in book.languages]
            primary_language = language_codes[0] if language_codes else None

            book_data = {
                'id': book.gutenberg_id,
                'title': book.title,
                'author': author_data,
                'genre': genre,
                'language': primary_language,
                'subjects': [subject.name for subject in book.subjects],
                'bookshelves': [shelf.name for shelf in book.bookshelves],
                'download_links': [
                    {
                        'mime_type': fmt.mime_type,
                        'url': fmt.url
                    } for fmt in book.formats
                ]
            }
            books.append(book_data)

        return jsonify({
            'total_books': total_books,
            'page': page,
            'total_pages': total_pages,
            'books': books
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400