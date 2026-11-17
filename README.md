# 🎬 AI Video Studio (Finexo Video AI Creator)

Nền tảng tạo và ghép video/hình ảnh với giọng đọc AI hài hước lôi cuốn, tự động đồng bộ thời lượng chuẩn xác và hòa âm nhạc nền mượt mà.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/maihoa3601/ai-video-studio)

---

## 🌟 Tính Năng Chính
- **Ghép Video & Tự Động Loop:** Tải lên video bất kỳ, hệ thống tự động loop mượt mà khớp chuẩn độ dài giọng đọc.
- **Ghép Chuỗi Hình Ảnh (Slideshow):** Tải nhiều hình ảnh, tự động chia đều thời lượng từng ảnh và xuất video dọc 9:16 hoặc 16:9.
- **Gọi API AI Viết Kịch Bản:** Tích hợp Google Gemini API, OpenAI GPT-4o hoặc AI Offline không cần Key.
- **Giọng Đọc AI & Tone Hài Hước:** Nam Minh lém lỉnh, Nữ trẻ trung, Hoạt hình Chipmunk meme, Bán hàng sôi nổi.
- **Nhạc Nền Thông Minh (BGM Ducking):** Nhạc nền TikTok vui nhộn, tự động giảm nhỏ âm lượng khi có tiếng nói.
- **Giao Diện Finexo UI Design:** Bố cục Bento Cards sang trọng, hiện đại, tối ưu mobile & desktop.

---

## 🚀 Cách Triển Khai (Deploy) Nhanh Nhất

### Cách 1: Deploy lên Render (Miễn phí 1-Click)
Bấm nút bên dưới để deploy tự động từ GitHub qua Docker:

👉 **[Deploy to Render](https://render.com/deploy?repo=https://github.com/maihoa3601/ai-video-studio)**

### Cách 2: Deploy lên Hugging Face Spaces (Miễn phí 16GB RAM)
1. Truy cập [Hugging Face Spaces](https://huggingface.co/spaces) -> **Create new Space**.
2. Đặt tên Space, chọn **Docker** (Blank).
3. Clone repo này hoặc push trực tiếp mã nguồn lên Hugging Face Space.

### Cách 3: Chạy trực tiếp trên máy cục bộ
```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Khởi chạy giao diện web
python run_web.py
```
Mở trình duyệt tại: `http://localhost:8000`
