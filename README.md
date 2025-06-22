# 🔗 URL Shortener

A clean and scalable URL shortener web application built with **FastAPI** and **SQLite**. This project demonstrates modern Python web development practices with a focus on clean architecture and separation of concerns.

## ✨ Features

- 🚀 **Shorten long URLs** with randomly generated short codes
- 🔄 **Redirect to original URLs** using short codes
- 📊 **Track click statistics** for each shortened URL
- 🗄️ **SQLite database** for persistent storage
- 🔌 **RESTful API** with comprehensive endpoints
- ✅ **Input validation** with Pydantic models
- 🧪 **Comprehensive test suite** with pytest
- 📝 **Auto-generated API documentation**

## 🏗️ Project Structure

```
.
├── main.py            # FastAPI app with routing
├── models.py          # Pydantic models for validation
├── database.py        # SQLite database setup and models
├── crud.py            # Database operations (Create, Read, Update, Delete)
├── utils.py           # Utility functions (URL code generator)
├── test_main.py       # Comprehensive test suite
├── requirements.txt   # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parthrastogicoder/Url-Shortner.git
   cd Url-Shortner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 API Endpoints

### POST /shorten
Create a short URL from a long URL.

**Request:**
```json
{
  "url": "https://www.example.com/very/long/path/to/resource"
}
```

**Response:**
```json
{
  "id": 1,
  "original_url": "https://www.example.com/very/long/path/to/resource",
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "created_at": "2024-01-01T12:00:00",
  "click_count": 0
}
```

### GET /{short_code}
Redirect to the original URL using the short code.

**Example:** `GET /abc123` → Redirects to original URL

### GET /stats/{short_code}
Get statistics for a shortened URL.

**Response:**
```json
{
  "id": 1,
  "original_url": "https://www.example.com/very/long/path/to/resource",
  "short_code": "abc123",
  "created_at": "2024-01-01T12:00:00",
  "click_count": 5
}
```

### GET /api/urls
List all shortened URLs with pagination.

**Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest test_main.py -v
```

### Test Coverage

The test suite covers:
- ✅ URL shortening functionality
- ✅ URL redirection
- ✅ Statistics tracking
- ✅ Input validation
- ✅ Error handling
- ✅ Edge cases

## 🏛️ Architecture

### Clean Architecture Principles

1. **Separation of Concerns**
   - `main.py`: API routing and HTTP handling
   - `models.py`: Data validation and serialization
   - `database.py`: Database models and connection
   - `crud.py`: Database operations
   - `utils.py`: Business logic utilities

2. **Dependency Injection**
   - Database sessions injected via FastAPI's Depends
   - Easy to mock for testing

3. **Input Validation**
   - Pydantic models ensure data integrity
   - Automatic API documentation generation


### Development Commands

```bash
# Install in development mode
pip install -e .

# Run with auto-reload for development
uvicorn main:app --reload

# Format code
black .

# Type checking
mypy .

# Run linter
flake8 .
```

## 🚀 Deployment

### Local Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Production Deployment (Render)

1. **Create a `Procfile`:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy to Render:**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔐 Security Considerations

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- Rate limiting (can be added with slowapi)
- HTTPS in production (handled by deployment platform)

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Validation:** Pydantic
- **Testing:** pytest
- **Documentation:** Auto-generated with FastAPI



## 👨‍💻 Author

**Parth Rastogi** - [@parthrastogicoder](https://github.com/parthrastogicoder)

---

