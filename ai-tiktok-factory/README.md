# 🎬 AI TikTok Video Factory (Vertical 9:16)

Hệ thống tự động hóa 100% quy trình sản xuất video ngắn TikTok, YouTube Shorts và Facebook Reels chuẩn kích thước dọc **1080x1920 (30 FPS)** bằng Python & FFmpeg.

Chuyên tạo nội dung tiếng Việt chất lượng cao về:
- 💡 **Kiến thức AI** (AI Agent là gì? RAG là gì?)
- ⭐ **Review công cụ AI** (ChatGPT, Claude, Midjourney...)
- ⚖️ **So sánh AI** (ChatGPT vs Gemini...)
- 💼 **Bán sản phẩm & Dịch vụ AI hợp pháp** (Khóa học, tư vấn, setup tự động hóa doanh nghiệp, prompt pack - tuyệt đối không bán tài khoản lậu).

---

## 🌟 Tính Năng Nổi Bật

1. **Pipeline 6 bước tự động khép kín**:
   - `[1/6]` Sinh kịch bản TikTok tiếng Việt tự nhiên, có Hook 3s đầu, Main content, Result và CTA.
   - `[2/6]` Phân rã kịch bản thành các Scene trực quan với headline & visual keywords.
   - `[3/6]` Tạo Voice-over tự nhiên bằng Microsoft Edge Neural TTS (miễn phí, không cần API key) hoặc OpenAI / ElevenLabs.
   - `[4/6]` Tạo phụ đề phrase-level (2-4 từ), highlight từ khóa neon, canh lề an toàn (Safe-zone) tránh UI TikTok.
   - `[5/6]` Visual Engine phong cách Dark Tech: gradient nền công nghệ cao, cyber grid, neural network nodes, card thông tin hiện đại và chuyển động Ken Burns zoom mượt mà.
   - `[6/6]` Render video cuối cùng bằng FFmpeg: ghép âm thanh, tự động mix nhạc nền (ducking 10%, fade in/out), và thanh tiến trình động (Progress bar) ở chân video.

2. **Cấu trúc Output tiêu chuẩn cho mỗi video**:
   ```
   output/<slug>/
   ├── script.txt       # Lời thoại đầy đủ
   ├── scenes.json      # Dữ liệu timeline từng phân cảnh
   ├── voice.mp3        # File giọng đọc chất lượng cao
   ├── subtitles.srt    # File phụ đề chuẩn SRT
   └── final.mp4        # Video hoàn chỉnh 1080x1920 H.264
   ```

---

## 🛠️ Yêu Cầu Hệ Thống & Cài Đặt

### 1. Cài đặt Python (3.10 trở lên)
- **Windows**: Tải installer từ [python.org](https://www.python.org/downloads/) (nhớ tích chọn **"Add Python to PATH"**).
- **macOS**: `brew install python`
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install -y python3 python3-pip python3-venv`

### 2. Cài đặt FFmpeg
- **Windows**:
  ```powershell
  winget install Gyan.FFmpeg
  ```
  *(Hệ thống cũng tự động tích hợp fallback qua thư viện `imageio-ffmpeg` nếu chưa cài FFmpeg toàn cục)*.
- **macOS**:
  ```bash
  brew install ffmpeg
  ```
- **Linux**:
  ```bash
  sudo apt install -y ffmpeg
  ```

---

## 🚀 Cài Đặt Dự Án

### Bước 1: Clone hoặc tải mã nguồn
```bash
cd ai-tiktok-factory
```

### Bước 2: Tạo môi trường ảo (Khuyên dùng)
- **Windows**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Bước 3: Cài đặt thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình File `.env`
Sao chép file mẫu:
```bash
cp .env.example .env
```
Nội dung file `.env`:
```env
# AI Script Generator: offline | openai | gemini
AI_PROVIDER=offline
AI_API_KEY=
AI_MODEL=gpt-4o-mini

# Text-to-Speech: edge-tts | openai | elevenlabs | gtts
TTS_PROVIDER=edge-tts
TTS_API_KEY=

# Giọng đọc tiếng Việt (Mặc định Edge TTS miễn phí 100%):
# - vi-VN-HoaiMyNeural (Giọng Nữ chuẩn miền Nam/Trung)
# - vi-VN-NamMinhNeural (Giọng Nam chuẩn miền Bắc)
VOICE_ID=vi-VN-HoaiMyNeural

# Thông số video
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
VIDEO_FPS=30

# Phụ đề & Âm nhạc
SUBTITLE_FONT_SIZE=68
SUBTITLE_BOTTOM_MARGIN=420
MUSIC_VOLUME=0.10
```

> [!TIP]
> Bạn có thể sử dụng ngay mà **không cần bất kỳ API key nào**! Mặc định `AI_PROVIDER=offline` dùng bộ template kịch bản tối ưu sẵn và `TTS_PROVIDER=edge-tts` sử dụng giọng đọc neural miễn phí của Microsoft.

---

## 💻 Hướng Dẫn Sử Dụng

### 1. Chế độ Tương tác (Interactive CLI)
Chạy lệnh đơn giản:
```bash
python main.py
```
Giao diện sẽ hiển thị:
```
============================================================
              AI TIKTOK VIDEO FACTORY (9:16)
        Automated Vietnamese AI Video Production
============================================================

Chủ đề video:
> 5 công cụ AI dân văn phòng nên biết

Loại video:
1. Kiến thức (Education)
2. Review (Đánh giá công cụ)
3. So sánh (Comparison)
4. Bán hàng / Dịch vụ (Sales)
> 1

Thời lượng:
1. 30 giây
2. 45 giây
3. 60 giây
> 1

CTA:
> Follow kênh để cập nhật công cụ AI mỗi ngày!
```

### 2. Chế độ Tự động hóa / Dòng lệnh (CLI Flags)
Dành cho chạy batch hoặc tích hợp automation:
```bash
# Video kiến thức 30s
python main.py --topic "AI Agent là gì và ứng dụng thực tế?" --type education --duration 30 --auto

# Video review công cụ 45s
python main.py --topic "ChatGPT Plus có đáng dùng không?" --type review --duration 45 --auto

# Video so sánh 30s
python main.py --topic "ChatGPT vs Claude 3.5 Sonnet" --type comparison --duration 30 --auto

# Video giới thiệu dịch vụ AI 30s
python main.py --topic "Dịch vụ tự động hóa quy trình AI cho doanh nghiệp" --type sales --duration 30 --cta "Liên hệ tư vấn miễn phí" --auto
```

---

## 📂 Quản Lý Tài Nguyên (Assets)

Bạn có thể tùy biến tài nguyên bằng cách thêm file vào thư mục `assets/`:
- `assets/music/`: Đặt file nhạc nền `background.mp3` (hệ thống tự động điều chỉnh âm lượng 10% và fade in/out).
- `assets/fonts/`: Đặt font chữ Unicode (`.ttf` / `.otf`) tùy thích.
- `assets/images/`: Thêm ảnh minh họa nếu muốn sử dụng thay cho đồ họa lập trình.
- `assets/videos/`: Thêm video footage nếu có.

---

## 🔧 Xử Lý Sự Cố (Troubleshooting)

| Vấn đề | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| `FFmpeg không được tìm thấy` | Chưa cài đặt hoặc chưa nạp biến môi trường | Chạy `pip install imageio-ffmpeg` hoặc khởi động lại terminal sau khi `winget install Gyan.FFmpeg`. |
| `UnicodeEncodeError trên Windows` | Bảng mã console mặc định là cp1252 | Hệ thống đã tự động cấu hình `sys.stdout.reconfigure(encoding='utf-8')`. Đảm bảo chạy bản Python 3.10+. |
| `Lỗi kết nối Edge-TTS` | Mất mạng hoặc bị chặn cổng | Kiểm tra kết nối mạng Internet. Edge-TTS cần kết nối để tải giọng đọc neural. |
| `Chữ phụ đề bị lỗi font tiếng Việt` | Thiếu font hỗ trợ Unicode có dấu | Hệ thống tự động trỏ đến font Segoe UI / Arial có sẵn trên Windows hoặc nạp từ `assets/fonts/arialbd.ttf`. |

---

## 📜 Giấy Phép & Đạo Đức Nội Dung

- Dự án tuân thủ tiêu chuẩn cộng đồng TikTok và quy tắc quảng bá dịch vụ AI hợp pháp.
- Tuyệt đối nghiêm cấm sử dụng template `sales` để quảng bá tài khoản lậu, crack hoặc dịch vụ vi phạm bản quyền.
