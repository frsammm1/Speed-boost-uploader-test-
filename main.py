import logging
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT
from handlers import setup_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot client
app = Client(
    "m3u8_supercharged_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=8,  # Increased workers for parallel processing
    sleep_threshold=60
)

# Web server for health checks
web_app = web.Application()

async def health_check(request):
    return web.Response(text="OK - Bot v8.0 SUPERCHARGED Running!")

async def stats(request):
    return web.Response(text="M3U8 Bot - Enhanced Speed & Progress Tracking")

web_app.router.add_get("/", health_check)
web_app.router.add_get("/health", health_check)
web_app.router.add_get("/stats", stats)


async def main():
    """Main bot initialization"""
    try:
        # Start web server
        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        logger.info(f"✅ Web server started on port {PORT}")
        
        # Setup bot handlers
        setup_handlers(app)
        
        # Start bot
        await app.start()
        logger.info("🚀 Bot v8.0 SUPERCHARGED started successfully!")
        logger.info("⚡ Features: 3-4x Speed, Upload Progress, Enhanced Thumbnails")
        
        # Keep bot running
        await idle()
        
    except Exception as e:
        logger.error(f"Bot startup error: {e}")
        raise
    finally:
        try:
            await app.stop()
            logger.info("Bot stopped")
        except:
            pass


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 Starting M3U8 Downloader Bot v8.0 SUPERCHARGED")
    logger.info("⚡ Enhanced Speed | 📊 Upload Progress | 🖼️ Better Thumbnails")
    logger.info("=" * 60)
    
    try:
        app.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
