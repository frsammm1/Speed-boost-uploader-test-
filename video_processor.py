import os
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional
from config import THUMBNAIL_TIME, THUMBNAIL_SIZE, THUMBNAIL_QUALITY

logger = logging.getLogger(__name__)


def get_video_info(filepath: str) -> Dict:
    """Get video duration and dimensions with better error handling"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams',
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        
        if result.returncode != 0:
            logger.error(f"FFprobe failed: {result.stderr}")
            return {'duration': 0, 'width': 1280, 'height': 720}
        
        data = json.loads(result.stdout)
        
        # Get duration
        duration = int(float(data.get('format', {}).get('duration', 0)))
        
        # Get video stream
        video_stream = next(
            (s for s in data.get('streams', []) if s.get('codec_type') == 'video'), 
            {}
        )
        width = video_stream.get('width', 1280)
        height = video_stream.get('height', 720)
        
        # Validate dimensions
        if width <= 0 or height <= 0:
            width, height = 1280, 720
        
        logger.info(f"Video info: {width}x{height}, {duration}s")
        return {'duration': duration, 'width': width, 'height': height}
        
    except subprocess.TimeoutExpired:
        logger.error("FFprobe timeout")
        return {'duration': 0, 'width': 1280, 'height': 720}
    except json.JSONDecodeError as e:
        logger.error(f"FFprobe JSON error: {e}")
        return {'duration': 0, 'width': 1280, 'height': 720}
    except Exception as e:
        logger.error(f"FFprobe error: {e}")
        return {'duration': 0, 'width': 1280, 'height': 720}


def generate_thumbnail(video_path: str, thumb_path: str, video_duration: int = 0) -> bool:
    """Generate high-quality thumbnail from video with multiple fallback attempts"""
    try:
        # Determine best time for thumbnail
        if video_duration > 10:
            thumb_time = min(video_duration // 4, 10)  # 1/4 into video or 10s max
        else:
            thumb_time = 2
        
        thumb_time_str = f"00:00:{thumb_time:02d}"
        
        # Try primary method with hardware acceleration
        cmd = [
            'ffmpeg', '-ss', thumb_time_str,
            '-i', video_path,
            '-vframes', '1',
            '-vf', f'scale={THUMBNAIL_SIZE}:force_original_aspect_ratio=decrease',
            '-q:v', str(THUMBNAIL_QUALITY),
            thumb_path,
            '-y'
        ]
        
        logger.info(f"Generating thumbnail at {thumb_time_str}")
        result = subprocess.run(cmd, capture_output=True, timeout=45)
        
        # Check if thumbnail was created successfully
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 2048:
            logger.info(f"Thumbnail generated successfully: {os.path.getsize(thumb_path)} bytes")
            return True
        
        # Fallback 1: Try at 0 seconds
        logger.warning("Primary thumbnail failed, trying at 0s")
        cmd[1] = '00:00:00'
        result = subprocess.run(cmd, capture_output=True, timeout=45)
        
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 2048:
            logger.info("Thumbnail generated at 0s")
            return True
        
        # Fallback 2: Try middle of video
        if video_duration > 5:
            mid_time = video_duration // 2
            mid_str = f"00:00:{mid_time:02d}"
            logger.warning(f"Trying thumbnail at middle: {mid_str}")
            cmd[1] = mid_str
            result = subprocess.run(cmd, capture_output=True, timeout=45)
            
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 2048:
                logger.info("Thumbnail generated at middle")
                return True
        
        # Fallback 3: Simple extraction without seeking
        logger.warning("Trying simple extraction")
        simple_cmd = [
            'ffmpeg', '-i', video_path,
            '-vframes', '1',
            '-vf', f'scale={THUMBNAIL_SIZE}',
            '-q:v', '2',
            thumb_path,
            '-y'
        ]
        result = subprocess.run(simple_cmd, capture_output=True, timeout=45)
        
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 2048:
            logger.info("Thumbnail generated with simple method")
            return True
        
        logger.error("All thumbnail generation attempts failed")
        return False
        
    except subprocess.TimeoutExpired:
        logger.error("Thumbnail generation timeout")
        return False
    except Exception as e:
        logger.error(f"Thumbnail error: {e}")
        return False


def validate_video_file(filepath: str) -> bool:
    """Validate if video file is playable"""
    try:
        if not os.path.exists(filepath):
            return False
        
        if os.path.getsize(filepath) < 10240:  # Less than 10KB
            return False
        
        # Quick validation with ffprobe
        cmd = ['ffprobe', '-v', 'error', filepath]
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"Video validation error: {e}")
        return False
