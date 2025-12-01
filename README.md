# 🚀 M3U8 Downloader Bot v8.0 SUPERCHARGED

**The Ultimate Telegram Bot for High-Speed Media Downloads**

## ⚡ Key Features

### 🏎️ Performance Enhancements
- **3-4x Faster Downloads** - Optimized chunk sizes and concurrent processing
- **Real-time Upload Progress** - Beautiful progress bars for all uploads
- **Enhanced Thumbnails** - Never blank! Multiple fallback methods
- **Parallel Processing** - Multiple concurrent downloads support
- **Smart Buffering** - Optimized buffer sizes for maximum speed

### 📦 Supported Formats
- **Videos**: M3U8, MPD, MP4, MKV, AVI, MOV, FLV, WMV, WEBM, TS
- **Images**: PNG, JPG, JPEG, GIF, BMP, WEBP, SVG
- **Documents**: PDF, DOC, DOCX, TXT, ZIP, RAR

### 🎯 Advanced Features
- **Range Selection** - Download specific ranges (e.g., 1-50, 10-20)
- **Auto Serial Numbering** - All files numbered automatically
- **Quality Selection** - Choose from 360p, 480p, 720p, 1080p
- **Progress Tracking** - Real-time download and upload progress
- **Error Handling** - Robust error recovery and retries
- **Batch Processing** - Handle multiple files efficiently

## 📁 Project Structure

```
├── config.py              # Configuration and settings
├── utils.py              # Utility functions
├── video_processor.py    # Video processing and thumbnails
├── downloader.py         # Enhanced downloader module
├── uploader.py           # Uploader with progress tracking
├── handlers.py           # Bot command handlers
├── main.py               # Main bot entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── render.yaml          # Render deployment config
└── README.md            # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.11+
- FFmpeg
- Telegram Bot Token
- API ID and API Hash from my.telegram.org

### Local Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Uploader-try
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export PORT="10000"
```

4. **Run the bot**
```bash
python main.py
```

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t m3u8-bot .
docker run -d \
  -e API_ID="your_api_id" \
  -e API_HASH="your_api_hash" \
  -e BOT_TOKEN="your_bot_token" \
  -e PORT="10000" \
  -p 10000:10000 \
  m3u8-bot
```

## 🌐 Render Deployment

1. **Fork this repository**

2. **Create new Web Service on Render**
   - Environment: Docker
   - Add environment variables:
     - `API_ID`
     - `API_HASH`
     - `BOT_TOKEN`
     - `PORT` (set to 10000)

3. **Deploy!** Render will automatically build and deploy

### Keep Bot Alive on Free Tier
The included `render.yaml` has a cron job that pings the bot every 10 minutes to prevent sleeping.

## 📖 Usage Guide

### Basic Usage

1. **Start the bot**
   ```
   /start
   ```

2. **Send a TXT or HTML file** containing links in format:
   ```
   Title 1: https://example.com/video.m3u8
   Title 2: https://example.com/image.jpg
   Title 3: https://example.com/document.pdf
   ```

3. **Choose download option**
   - Download All - Process entire file
   - Select Range - Choose specific items

4. **Select quality** (for videos)
   - 360p, 480p, 720p, or 1080p

5. **Monitor progress**
   - Real-time download progress with speed
   - Upload progress with ETA
   - Success/failure notifications

### Commands

- `/start` - Start the bot and see features
- `/cancel` - Cancel all active downloads

## ⚙️ Configuration

### Speed Optimization Settings (config.py)

```python
CHUNK_SIZE = 65536              # 64KB download chunks
CONCURRENT_FRAGMENTS = 8        # Parallel fragment downloads
MAX_CONCURRENT_DOWNLOADS = 3    # Parallel file downloads
BUFFER_SIZE = 262144           # 256KB buffer
HTTP_CHUNK_SIZE = 1048576      # 1MB HTTP chunks
UPLOAD_CHUNK_SIZE = 524288     # 512KB upload chunks
```

### Thumbnail Settings

```python
THUMBNAIL_TIME = "00:00:05"     # Take thumbnail at 5 seconds
THUMBNAIL_SIZE = "480:270"      # HD thumbnail resolution
THUMBNAIL_QUALITY = 2           # High quality (1-31, lower is better)
```

## 🎬 Video Processing

### Enhanced Thumbnail Generation
- **Multiple fallback methods** ensure thumbnails are never blank
- Attempts at different timestamps (5s, 0s, middle, simple extraction)
- High-quality 480x270 resolution
- Proper aspect ratio preservation

### Video Information
- Automatic duration detection
- Width and height extraction
- Validation before upload

## 📊 Progress Tracking

### Download Progress
- Visual progress bar
- Downloaded/Total size
- Current speed (MB/s)
- Estimated time remaining

### Upload Progress
- Real-time upload tracking
- Speed monitoring
- ETA calculation
- Beautiful progress display

## 🔒 Error Handling

- **Automatic retries** - Up to 20 retries for failed downloads
- **Fragment recovery** - Skips unavailable fragments
- **Validation** - Checks file integrity before upload
- **Graceful failures** - Provides fallback links on failure

## 🚀 Performance Tips

1. **Use quality settings wisely**
   - 720p is optimal for most cases
   - 1080p may be slower for large files

2. **Range selection**
   - Process in batches of 50-100 items
   - Reduces memory usage

3. **Render free tier**
   - Cron job keeps bot active
   - Health endpoint for monitoring

## 📝 Module Details

### config.py
- All configuration settings
- Quality mappings
- File type definitions
- Performance tuning parameters

### utils.py
- File type detection
- Content parsing
- Progress bar creation
- Size/time formatting
- Filename sanitization

### video_processor.py
- FFmpeg integration
- Video info extraction
- Enhanced thumbnail generation
- Video validation

### downloader.py
- High-speed file downloads
- Video downloading with yt-dlp
- Progress tracking
- SSL handling
- Concurrent fragment downloads

### uploader.py
- Progress-tracked uploads
- Video/Photo/Document handlers
- Speed monitoring
- ETA calculation

### handlers.py
- Bot command handlers
- Callback query processing
- Batch processing logic
- File type routing
- Cleanup management

## 🐛 Troubleshooting

### Thumbnail Issues
- Bot now has 4 fallback methods
- Will never send blank thumbnails
- Checks file validity before extraction

### Slow Downloads
- Check your internet connection
- Verify source server speed
- Increase `CONCURRENT_FRAGMENTS` in config.py

### Upload Failures
- Large files may timeout on free tier
- Split into smaller ranges
- Check Telegram file size limits (2GB)

## 📈 Version History

### v8.0 SUPERCHARGED (Current)
- ⚡ 3-4x speed improvement
- 📊 Upload progress tracking
- 🖼️ Enhanced thumbnail generation
- 🏗️ Modular code structure
- 🚀 Parallel processing
- 📝 Better error messages

### v7.0
- Range selection
- Serial numbering
- Multi-format support
- Basic progress tracking

## 📜 License

MIT License - Feel free to modify and distribute

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support

For issues and feature requests, please open an issue on GitHub.

---

**Made with ⚡ for maximum speed and efficiency!**
