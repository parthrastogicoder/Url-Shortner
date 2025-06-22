import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import json

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "URL Shortener API" in response.json()["message"]

def test_shorten_url(setup_database):
    """Test URL shortening"""
    url_data = {"url": "https://www.example.com"}
    response = client.post("/shorten", json=url_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == "https://www.example.com/"
    assert data["click_count"] == 0

def test_shorten_invalid_url(setup_database):
    """Test shortening invalid URL"""
    url_data = {"url": "not-a-valid-url"}
    response = client.post("/shorten", json=url_data)
    assert response.status_code == 422  # Validation error

def test_redirect_to_original_url(setup_database):
    """Test redirection to original URL"""
    # First create a short URL
    url_data = {"url": "https://www.google.com"}
    response = client.post("/shorten", json=url_data)
    short_code = response.json()["short_code"]
    
    # Test redirection
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.google.com/"

def test_redirect_nonexistent_code(setup_database):
    """Test redirection with non-existent short code"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_url_statistics(setup_database):
    """Test URL statistics endpoint"""
    # Create a short URL
    url_data = {"url": "https://www.github.com"}
    response = client.post("/shorten", json=url_data)
    short_code = response.json()["short_code"]
    
    # Get initial stats
    response = client.get(f"/stats/{short_code}")
    assert response.status_code == 200
    initial_stats = response.json()
    assert initial_stats["click_count"] == 0
    
    # Click the URL
    client.get(f"/{short_code}", follow_redirects=False)
    
    # Check updated stats
    response = client.get(f"/stats/{short_code}")
    updated_stats = response.json()
    assert updated_stats["click_count"] == 1

def test_stats_nonexistent_code(setup_database):
    """Test statistics for non-existent short code"""
    response = client.get("/stats/nonexistent")
    assert response.status_code == 404

def test_list_urls(setup_database):
    """Test listing all URLs"""
    # Create a few URLs
    urls = [
        {"url": "https://www.python.org"},
        {"url": "https://www.fastapi.tiangolo.com"}
    ]
    
    for url_data in urls:
        client.post("/shorten", json=url_data)
    
    # Get all URLs
    response = client.get("/api/urls")
    assert response.status_code == 200
    data = response.json()
    assert "urls" in data
    assert len(data["urls"]) >= 2

def test_url_shortening_uniqueness(setup_database):
    """Test that same URL gets different short codes"""
    url_data = {"url": "https://www.example.org"}
    
    response1 = client.post("/shorten", json=url_data)
    response2 = client.post("/shorten", json=url_data)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Should get different short codes for same URL
    code1 = response1.json()["short_code"]
    code2 = response2.json()["short_code"]
    assert code1 != code2
