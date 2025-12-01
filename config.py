import os
from pathlib import Path

# Bot Configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
PORT = int(os.getenv("PORT", "10000"))

# Directory Configuration
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Quality Settings
QUALITY_MAP = {
    "360p": "360",
    "480p": "480", 
    "720p": "720",
    "1080p": "1080",
}

# Supported File Types
SUPPORTED_TYPES = {
    'video': ['.m3u8', '.mpd', '.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.ts'],
    'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
}

# Download Settings for Speed Optimization
CHUNK_SIZE = 65536  # 64KB chunks for better speed
CONCURRENT_FRAGMENTS = 8  # Increased from 4
MAX_CONCURRENT_DOWNLOADS = 3  # Parallel downloads
BUFFER_SIZE = 262144  # 256KB buffer
HTTP_CHUNK_SIZE = 1048576  # 1MB chunks

# Upload Settings
UPLOAD_CHUNK_SIZE = 524288  # 512KB for faster uploads
MAX_RETRIES = 20  # Increased retries
FRAGMENT_RETRIES = 20
CONNECTION_TIMEOUT = 2400  # 40 minutes

# Thumbnail Settings
THUMBNAIL_TIME = "00:00:05"  # 5 seconds into video
THUMBNAIL_SIZE = "480:270"  # Better quality thumbnail
THUMBNAIL_QUALITY = 2  # High quality
