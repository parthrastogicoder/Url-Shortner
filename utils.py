import random
import string
from typing import Optional

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url: str) -> bool:
    """Basic URL validation"""
    return url.startswith(('http://', 'https://'))

def create_short_url(short_code: str, base_url: str = "http://localhost:8000") -> str:
    """Create the full short URL"""
    return f"{base_url}/{short_code}"
