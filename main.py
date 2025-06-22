from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import get_db, create_tables
from models import URLCreate, URLResponse, URLStats
from utils import create_short_url
import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown

# Create FastAPI app
app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener built with FastAPI and SQLite",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "URL Shortener API",
        "endpoints": {
            "POST /shorten": "Create a short URL",
            "GET /{short_code}": "Redirect to original URL",
            "GET /stats/{short_code}": "Get URL statistics"
        }
    }

@app.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, request: Request, db: Session = Depends(get_db)):
    """Create a short URL"""
    try:
        # Create short URL in database
        db_url = crud.create_short_url(db, url_data)
        
        # Get base URL from request
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        
        # Return response
        return URLResponse(
            id=db_url.id,
            original_url=db_url.original_url,
            short_code=db_url.short_code,
            short_url=create_short_url(db_url.short_code, base_url),
            created_at=db_url.created_at,
            click_count=db_url.click_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create short URL: {str(e)}")

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect to original URL using short code"""
    db_url = crud.get_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    # Increment click count
    crud.increment_click_count(db, db_url)
    
    # Redirect to original URL
    return RedirectResponse(url=db_url.original_url, status_code=302)

@app.get("/stats/{short_code}", response_model=URLStats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    """Get statistics for a short URL"""
    db_url = crud.get_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return URLStats(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        created_at=db_url.created_at,
        click_count=db_url.click_count
    )

@app.get("/api/urls")
def list_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all URLs with pagination"""
    urls = crud.get_all_urls(db, skip=skip, limit=limit)
    return {"urls": urls, "count": len(urls)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
