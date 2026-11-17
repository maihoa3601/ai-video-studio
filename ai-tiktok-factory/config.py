"""
Configuration settings for AI TikTok Video Factory.
Loads environment variables and sets defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
CONFIG_FILE_PATH = Path(__file__).resolve()
BASE_DIR = CONFIG_FILE_PATH.parent

# Load .env file from project root
load_dotenv(BASE_DIR / ".env")

# Video Settings
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", "30"))

# Channel / Branding Settings
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "AI Master")

# AI Script Generation Settings
AI_PROVIDER = os.getenv("AI_PROVIDER", "offline").lower()  # "offline", "openai", "gemini"
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

# TTS Settings
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge-tts").lower()  # "edge-tts", "openai", "elevenlabs", "gtts"
TTS_API_KEY = os.getenv("TTS_API_KEY", "")
# Default Vietnamese voice: vi-VN-HoaiMyNeural (female) or vi-VN-NamMinhNeural (male)
VOICE_ID = os.getenv("VOICE_ID", "vi-VN-HoaiMyNeural")

# Asset Directories
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
VIDEOS_DIR = ASSETS_DIR / "videos"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"

# Output & Temp Directories
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Ensure runtime directories exist
for path in [IMAGES_DIR, VIDEOS_DIR, MUSIC_DIR, FONTS_DIR, OUTPUT_DIR, TEMP_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Subtitle Styling Settings
SUBTITLE_FONT_SIZE = int(os.getenv("SUBTITLE_FONT_SIZE", "68"))
SUBTITLE_FONT_COLOR = os.getenv("SUBTITLE_FONT_COLOR", "#FFFFFF")
SUBTITLE_HIGHLIGHT_COLOR = os.getenv("SUBTITLE_HIGHLIGHT_COLOR", "#FFE600")  # Neon yellow
SUBTITLE_BG_COLOR = os.getenv("SUBTITLE_BG_COLOR", "rgba(0, 0, 0, 0.75)")
# Margin from bottom to avoid TikTok UI overlay (captions, music icon, buttons)
SUBTITLE_BOTTOM_MARGIN = int(os.getenv("SUBTITLE_BOTTOM_MARGIN", "420"))

# Audio Settings
MUSIC_VOLUME = float(os.getenv("MUSIC_VOLUME", "0.10"))  # 10% volume for background music
