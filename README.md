# Project Gutenberg Book Search API

A Flask-based REST API for searching and retrieving books from Project Gutenberg. The API provides comprehensive search capabilities with multiple filter criteria and pagination support.

## Features

- Search books by multiple criteria:
  - Book IDs (Project Gutenberg ID numbers)
  - Language
  - Mime-type (download formats)
  - Topic (searches in subjects and bookshelves)
  - Author
  - Title
- Results ordered by download count (popularity)
- Pagination support (25 books per page)
- Comprehensive book metadata including:
  - Title
  - Author information
  - Genre
  - Language
  - Subjects
  - Bookshelves
  - Download links

## Tech Stack

- Python 3.10
- Flask 2.3.3
- SQLAlchemy 1.4.23
- PostgreSQL 13
- Docker & Docker Compose

## Setup

### Prerequisites
- Docker and Docker Compose
- Project Gutenberg database dump file (`gutendex.dump`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/BookSearch.git
cd BookSearch
```

2. Run the application:
```bash
./run.sh
```

The script will:
- Build and start the Docker containers
- Import the database dump
- Start the Flask API

The API will be available at `http://localhost:5000`

## API Usage

### Endpoint

`GET /api/v1/books`

### Query Parameters

- `book_ids`: Comma-separated list of Project Gutenberg book IDs
- `language`: Comma-separated list of language codes (e.g., en,fr)
- `mime_type`: Comma-separated list of mime types (e.g., text/plain,text/html)
- `topic`: Topic to filter by (searches in subjects and bookshelves)
- `author`: Author name (supports partial matches)
- `title`: Book title (supports partial matches)
- `page`: Page number for pagination

### Example Requests

```bash
# Search by title
curl "http://localhost:5000/api/v1/books?title=Alice"

# Search by language and topic
curl "http://localhost:5000/api/v1/books?language=en,fr&topic=fiction"

# Search with pagination
curl "http://localhost:5000/api/v1/books?author=Shakespeare&page=2"
```

### Example Response

```json
{
  "total_books": 42,
  "page": 1,
  "total_pages": 2,
  "books": [
    {
      "id": 11,
      "title": "Alice's Adventures in Wonderland",
      "author": {
        "name": "Lewis Carroll",
        "birth_year": 1832,
        "death_year": 1898
      },
      "genre": "Fiction",
      "language": "en",
      "subjects": ["Fantasy", "Children's literature"],
      "bookshelves": ["Children's Literature"],
      "download_links": [
        {
          "mime_type": "text/plain",
          "url": "https://www.gutenberg.org/ebooks/11.txt.utf-8"
        }
      ]
    }
  ]
}
```

## Development

### Project Structure
```
BookSearch/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── database/
│   │   └── db.py
│   └── app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run.sh
```

### Running Tests
```bash
# TODO: Add test instructions
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
