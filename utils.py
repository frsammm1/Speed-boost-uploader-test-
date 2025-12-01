import re
import os
import logging
from typing import List, Dict
from config import SUPPORTED_TYPES

logger = logging.getLogger(__name__)

def get_file_type(url: str) -> str:
    """Determine file type from URL"""
    url_lower = url.lower()
    
    for ftype, extensions in SUPPORTED_TYPES.items():
        if any(ext in url_lower for ext in extensions):
            return ftype
    
    return 'unknown'


def parse_content(text: str) -> List[Dict]:
    """Parse content and identify all supported file types"""
    lines = text.strip().split('\n')
    items = []
    
    for line in lines:
        if ':' in line and ('http://' in line or 'https://' in line):
            parts = line.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                url = parts[1].strip()
                
                file_type = get_file_type(url)
                
                if file_type != 'unknown':
                    items.append({
                        'title': title, 
                        'url': url, 
                        'type': file_type
                    })
    
    return items


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def format_time(seconds: int) -> str:
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def sanitize_filename(filename: str, max_length: int = 50) -> str:
    """Sanitize filename for safe file system usage"""
    safe = re.sub(r'[^\w\s-]', '', filename)
    return safe[:max_length].strip()


def create_progress_bar(percent: float, length: int = 20) -> str:
    """Create a visual progress bar"""
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percent:.1f}%"
