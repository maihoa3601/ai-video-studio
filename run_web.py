"""
AI Video Studio Web Application Launcher.
Run with: python run_web.py
"""

import os
import sys
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web_app"

if str(WEB_DIR) not in sys.path:
    sys.path.insert(0, str(WEB_DIR))

os.chdir(str(WEB_DIR))

import uvicorn

if __name__ == "__main__":
    port = 8000
    url = f"http://localhost:{port}"
    print("=" * 60)
    print("🚀 AI VIDEO STUDIO (FINE-GRAINED AI VIDEO CREATOR) 🚀")
    print(f"👉 Đang khởi chạy web server tại: {url}")
    print("👉 Mở trình duyệt và truy cập đường dẫn trên để sử dụng giao diện!")
    print("=" * 60)
    
    # Try opening browser automatically
    try:
        webbrowser.open(url)
    except:
        pass

    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=False)
