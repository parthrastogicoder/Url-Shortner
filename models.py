from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int
    
    model_config = {"from_attributes": True}

class URLStats(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    click_count: int
    
    model_config = {"from_attributes": True}
