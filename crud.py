from sqlalchemy.orm import Session
from database import URLModel
from models import URLCreate
from utils import generate_short_code
from typing import Optional

def create_short_url(db: Session, url_data: URLCreate) -> URLModel:
    """Create a new short URL entry"""
    # Generate unique short code
    short_code = generate_short_code()
    while get_url_by_short_code(db, short_code):
        short_code = generate_short_code()
    
    # Create new URL entry
    db_url = URLModel(
        original_url=str(url_data.url),
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_code(db: Session, short_code: str) -> Optional[URLModel]:
    """Get URL by short code"""
    return db.query(URLModel).filter(URLModel.short_code == short_code).first()

def get_url_by_id(db: Session, url_id: int) -> Optional[URLModel]:
    """Get URL by ID"""
    return db.query(URLModel).filter(URLModel.id == url_id).first()

def increment_click_count(db: Session, url_model: URLModel) -> URLModel:
    """Increment click count for a URL"""
    url_model.click_count += 1
    db.commit()
    db.refresh(url_model)
    return url_model

def get_all_urls(db: Session, skip: int = 0, limit: int = 100):
    """Get all URLs with pagination"""
    return db.query(URLModel).offset(skip).limit(limit).all()
