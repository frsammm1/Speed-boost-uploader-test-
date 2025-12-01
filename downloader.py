import os
import ssl
import asyncio
import aiohttp
import aiofiles
import yt_dlp
import logging
from pathlib import Path
from typing import Optional, Dict
from pyrogram.types import Message
from config import (
    DOWNLOAD_DIR, CHUNK_SIZE, CONCURRENT_FRAGMENTS, 
    MAX_RETRIES, FRAGMENT_RETRIES, CONNECTION_TIMEOUT,
    HTTP_CHUNK_SIZE, BUFFER_SIZE
)
from utils import format_size, format_time, create_progress_bar

logger = logging.getLogger(__name__)


async def download_file(
    url: str, 
    filename: str, 
    progress_msg: Message, 
    user_id: int,
    active_downloads: Dict[int, bool]
) -> Optional[str]:
    """Universal file downloader with enhanced speed and progress tracking"""
    filepath = DOWNLOAD_DIR / filename
    
    try:
        # Enhanced SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Optimized connector for speed
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            limit=50,  # Increased connection limit
            limit_per_host=30,
            ttl_dns_cache=300,
            force_close=False,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=CONNECTION_TIMEOUT,
            connect=60,
            sock_read=120
        )
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"HTTP {response.status} for {url}")
                    return None
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                start_time = asyncio.get_event_loop().time()
                last_update = 0
                update_threshold = 512 * 1024  # Update every 512KB
                
                async with aiofiles.open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                        if not active_downloads.get(user_id, False):
                            if filepath.exists():
                                os.remove(filepath)
                            return None
                        
                        await f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress less frequently for speed
                        if downloaded - last_update >= update_threshold:
                            last_update = downloaded
                            try:
                                percent = (downloaded / total_size * 100) if total_size > 0 else 0
                                elapsed = asyncio.get_event_loop().time() - start_time
                                speed = downloaded / elapsed if elapsed > 0 else 0
                                
                                eta = int((total_size - downloaded) / speed) if speed > 0 else 0
                                bar = create_progress_bar(percent)
                                
                                await progress_msg.edit_text(
                                    f"📥 **Downloading...**\n\n"
                                    f"{bar}\n\n"
                                    f"📦 {format_size(downloaded)} / {format_size(total_size)}\n"
                                    f"⚡ {format_size(int(speed))}/s\n"
                                    f"⏱️ ETA: {format_time(eta)}"
                                )
                            except Exception as e:
                                logger.debug(f"Progress update error: {e}")
                
                if filepath.exists() and filepath.stat().st_size > 1024:
                    return str(filepath)
                return None
                
    except asyncio.TimeoutError:
        logger.error(f"Download timeout for {url}")
        return None
    except Exception as e:
        logger.error(f"File download error: {e}")
        return None


def download_video_sync(
    url: str, 
    quality: str, 
    output_path: str, 
    user_id: int,
    active_downloads: Dict[int, bool],
    download_progress: Dict[int, dict]
) -> bool:
    """Enhanced video downloader with optimized settings"""
    try:
        def progress_hook(d):
            if not active_downloads.get(user_id, False):
                raise Exception("Download cancelled by user")
            
            if d['status'] == 'downloading':
                try:
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded = d.get('downloaded_bytes', 0)
                    speed = d.get('speed', 0) or 0
                    eta = d.get('eta', 0)
                    
                    if total > 0:
                        percent = (downloaded / total) * 100
                        download_progress[user_id] = {
                            'percent': percent,
                            'downloaded': downloaded,
                            'total': total,
                            'speed': speed,
                            'eta': eta
                        }
                except Exception as e:
                    logger.debug(f"Progress hook error: {e}")
        
        # Optimized yt-dlp options for maximum speed
        ydl_opts = {
            'format': f'best[height<={quality}]/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            
            # Speed optimizations
            'concurrent_fragment_downloads': CONCURRENT_FRAGMENTS,
            'retries': MAX_RETRIES,
            'fragment_retries': FRAGMENT_RETRIES,
            'skip_unavailable_fragments': True,
            'buffersize': BUFFER_SIZE,
            'http_chunk_size': HTTP_CHUNK_SIZE,
            
            # Headers for better compatibility
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            
            # Fast post-processing
            'postprocessor_args': {
                'ffmpeg': ['-c', 'copy', '-movflags', '+faststart']
            },
            
            'progress_hooks': [progress_hook],
            'extractor_retries': MAX_RETRIES,
            'file_access_retries': MAX_RETRIES,
            
            # Additional speed settings
            'socket_timeout': 120,
            'hls_prefer_native': True,
            'external_downloader_args': ['-threads', '4'],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not active_downloads.get(user_id, False):
                return False
            
            logger.info(f"Starting download: {url}")
            ydl.download([url])
            logger.info(f"Download completed: {url}")
            return True
            
    except Exception as e:
        logger.error(f"Video download error: {e}")
        return False


async def update_video_progress(
    progress_msg: Message, 
    user_id: int,
    download_progress: Dict[int, dict],
    active_downloads: Dict[int, bool]
):
    """Update video download progress with enhanced display"""
    last_percent = -1
    
    while active_downloads.get(user_id, False) and user_id in download_progress:
        try:
            prog = download_progress[user_id]
            percent = prog.get('percent', 0)
            
            # Update every 3% or significant change
            if int(percent) - last_percent >= 3:
                last_percent = int(percent)
                
                downloaded = prog.get('downloaded', 0)
                total = prog.get('total', 0)
                speed = prog.get('speed', 0)
                eta = prog.get('eta', 0)
                
                bar = create_progress_bar(percent)
                
                await progress_msg.edit_text(
                    f"🎬 **Downloading Video**\n\n"
                    f"{bar}\n\n"
                    f"📦 {format_size(downloaded)} / {format_size(total)}\n"
                    f"⚡ {format_size(int(speed))}/s\n"
                    f"⏱️ ETA: {format_time(int(eta))}"
                )
                
        except Exception as e:
            logger.debug(f"Progress update error: {e}")
        
        await asyncio.sleep(2)


async def download_video(
    url: str,
    quality: str,
    filename: str,
    progress_msg: Message,
    user_id: int,
    active_downloads: Dict[int, bool],
    download_progress: Dict[int, dict]
) -> Optional[str]:
    """Download video with progress tracking and error handling"""
    temp_name = f"temp_{user_id}_{filename.replace('.mp4', '')}"
    output_path = str(DOWNLOAD_DIR / temp_name)
    
    try:
        download_progress[user_id] = {'percent': 0}
        
        await progress_msg.edit_text("🎬 Initializing download...")
        
        # Start progress updater
        progress_task = asyncio.create_task(
            update_video_progress(progress_msg, user_id, download_progress, active_downloads)
        )
        
        # Download video in executor
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(
            None,
            download_video_sync,
            url, quality, output_path, user_id, active_downloads, download_progress
        )
        
        # Cleanup progress
        if user_id in download_progress:
            del download_progress[user_id]
        
        try:
            progress_task.cancel()
        except:
            pass
        
        if not success or not active_downloads.get(user_id, False):
            return None
        
        await progress_msg.edit_text("✅ Download complete, processing...")
        
        # Find output file
        possible_files = []
        for ext in ['.mp4', '.mkv', '.webm', '.ts']:
            p = Path(output_path + ext)
            if p.exists() and p.stat().st_size > 10240:
                possible_files.append(p)
        
        # Check temp files
        for file in DOWNLOAD_DIR.glob(f"temp_{user_id}_*"):
            if file.is_file() and file.stat().st_size > 10240:
                possible_files.append(file)
        
        if not possible_files:
            logger.error(f"No output file found for {output_path}")
            return None
        
        # Get largest file (most complete)
        output_file = max(possible_files, key=lambda p: p.stat().st_size)
        final_path = DOWNLOAD_DIR / filename
        
        # Rename to final path
        if output_file != final_path:
            os.rename(output_file, final_path)
        else:
            final_path = output_file
        
        if final_path.exists() and final_path.stat().st_size > 10240:
            logger.info(f"Video ready: {final_path} ({format_size(final_path.stat().st_size)})")
            return str(final_path)
        
        return None
        
    except Exception as e:
        logger.error(f"Video download error: {e}")
        if user_id in download_progress:
            del download_progress[user_id]
        return None
