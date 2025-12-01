import os
import asyncio
import logging
from typing import Optional
from pyrogram import Client
from pyrogram.types import Message
from utils import format_size, format_time, create_progress_bar
from config import UPLOAD_CHUNK_SIZE

logger = logging.getLogger(__name__)


class UploadProgressTracker:
    """Track upload progress with enhanced display"""
    
    def __init__(self, progress_msg: Message, filename: str):
        self.progress_msg = progress_msg
        self.filename = filename
        self.last_update = 0
        self.start_time = asyncio.get_event_loop().time()
        self.last_percent = -1
    
    async def progress_callback(self, current: int, total: int):
        """Callback for upload progress"""
        try:
            percent = (current / total) * 100 if total > 0 else 0
            
            # Update every 4% for speed
            if int(percent) - self.last_percent >= 4:
                self.last_percent = int(percent)
                
                elapsed = asyncio.get_event_loop().time() - self.start_time
                speed = current / elapsed if elapsed > 0 else 0
                eta = int((total - current) / speed) if speed > 0 else 0
                
                bar = create_progress_bar(percent)
                
                await self.progress_msg.edit_text(
                    f"📤 **Uploading...**\n\n"
                    f"{bar}\n\n"
                    f"📦 {format_size(current)} / {format_size(total)}\n"
                    f"⚡ {format_size(int(speed))}/s\n"
                    f"⏱️ ETA: {format_time(eta)}"
                )
        except Exception as e:
            logger.debug(f"Upload progress error: {e}")


async def upload_video(
    client: Client,
    chat_id: int,
    video_path: str,
    caption: str,
    progress_msg: Message,
    thumb_path: Optional[str] = None,
    duration: int = 0,
    width: int = 1280,
    height: int = 720
) -> bool:
    """Upload video with progress tracking"""
    try:
        tracker = UploadProgressTracker(progress_msg, os.path.basename(video_path))
        
        await client.send_video(
            chat_id=chat_id,
            video=video_path,
            caption=caption,
            supports_streaming=True,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_path,
            progress=tracker.progress_callback
        )
        
        logger.info(f"Video uploaded: {video_path}")
        return True
        
    except Exception as e:
        logger.error(f"Video upload error: {e}")
        return False


async def upload_photo(
    client: Client,
    chat_id: int,
    photo_path: str,
    caption: str,
    progress_msg: Message
) -> bool:
    """Upload photo with progress tracking"""
    try:
        tracker = UploadProgressTracker(progress_msg, os.path.basename(photo_path))
        
        await client.send_photo(
            chat_id=chat_id,
            photo=photo_path,
            caption=caption,
            progress=tracker.progress_callback
        )
        
        logger.info(f"Photo uploaded: {photo_path}")
        return True
        
    except Exception as e:
        logger.error(f"Photo upload error: {e}")
        return False


async def upload_document(
    client: Client,
    chat_id: int,
    document_path: str,
    caption: str,
    progress_msg: Message
) -> bool:
    """Upload document with progress tracking"""
    try:
        tracker = UploadProgressTracker(progress_msg, os.path.basename(document_path))
        
        await client.send_document(
            chat_id=chat_id,
            document=document_path,
            caption=caption,
            progress=tracker.progress_callback
        )
        
        logger.info(f"Document uploaded: {document_path}")
        return True
        
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        return False
