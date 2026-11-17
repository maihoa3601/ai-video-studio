"""
FastAPI Server for AI Video Studio (AI Video Creator Web App).
Combines video/images with AI-synthesized voiceover, background music, and AI script generation.
"""

import os
import time
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import ai_service
import video_service

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
MUSIC_DIR = STATIC_DIR / "music"

# Ensure all working directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Video Studio", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and output directories
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")

class ScriptRequest(BaseModel):
    topic: str
    tone: str = "humorous"
    duration: int = 30
    api_provider: str = "gemini"
    api_key: Optional[str] = None
    custom_notes: Optional[str] = None

class PolishRequest(BaseModel):
    script: str
    api_provider: str = "gemini"
    api_key: Optional[str] = None

class PreviewVoiceRequest(BaseModel):
    text: str
    voice_type: str = "nam_hai_huoc"
    speed: float = 1.0
    pitch_style: str = "playful"

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>AI Video Studio</h1><p>Index file not found in static directory.</p>")

@app.get("/api/music-list")
async def get_music_list():
    """List available background music tracks."""
    tracks = []
    if MUSIC_DIR.exists():
        for f in MUSIC_DIR.glob("*.mp3"):
            tracks.append({
                "id": f.name,
                "name": f.stem.replace("_", " ").title(),
                "path": f"/static/music/{f.name}"
            })
    return {"tracks": tracks}

@app.post("/api/generate-script")
async def generate_script(req: ScriptRequest):
    """Generate script using AI (Gemini, OpenAI, or smart local generator)."""
    try:
        script = ai_service.generate_script_with_ai(
            topic=req.topic,
            tone=req.tone,
            target_duration=req.duration,
            api_provider=req.api_provider,
            api_key=req.api_key,
            custom_notes=req.custom_notes
        )
        return {"status": "success", "script": script}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/polish-script")
async def polish_script(req: PolishRequest):
    """Make existing script funnier and punchier."""
    try:
        polished = ai_service.polish_script_humor(
            script=req.script,
            api_key=req.api_key,
            api_provider=req.api_provider
        )
        return {"status": "success", "script": polished}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/preview-voice")
async def preview_voice(req: PreviewVoiceRequest):
    """Synthesize speech only for instant listening."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống!")
        
    ts = int(time.time() * 1000)
    audio_filename = f"preview_{ts}.mp3"
    audio_path = OUTPUTS_DIR / audio_filename
    
    try:
        duration = await video_service.synthesize_voice(
            text=req.text,
            output_audio=str(audio_path),
            voice_type=req.voice_type,
            speed=req.speed,
            pitch_style=req.pitch_style
        )
        return {
            "status": "success",
            "audio_url": f"/outputs/{audio_filename}",
            "duration": round(duration, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/render-video")
async def render_video(
    media_type: str = Form("video"),  # "video" or "images"
    script_text: str = Form(...),
    voice_type: str = Form("nam_hai_huoc"),
    speed: float = Form(1.0),
    pitch_style: str = Form("playful"),
    with_bgm: bool = Form(True),
    bgm_name: str = Form("cheerful_tiktok.mp3"),
    bgm_volume: float = Form(0.12),
    aspect_ratio: str = Form("keep"),
    use_sample_video: bool = Form(False),
    video_file: Optional[UploadFile] = File(None),
    image_files: Optional[List[UploadFile]] = File(None)
):
    """
    Main Video Creator Endpoint:
    1. Synthesizes voiceover from script_text.
    2. Blends background music (ducked).
    3. Merges with input video (seamless loop to match voice) OR image slideshow.
    """
    if not script_text.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập lời thoại / kịch bản!")

    ts = int(time.time() * 1000)
    
    # 1. Synthesize voice
    voice_path = OUTPUTS_DIR / f"voice_{ts}.mp3"
    try:
        voice_dur = await video_service.synthesize_voice(
            text=script_text,
            output_audio=str(voice_path),
            voice_type=voice_type,
            speed=speed,
            pitch_style=pitch_style
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo giọng nói AI: {e}")

    # 2. Mix with BGM
    final_audio_path = str(voice_path)
    if with_bgm and bgm_name:
        bgm_file = MUSIC_DIR / bgm_name
        if bgm_file.exists():
            mixed_audio = OUTPUTS_DIR / f"mixed_{ts}.mp3"
            try:
                final_audio_path = video_service.mix_audio_with_bgm(
                    voice_audio_path=str(voice_path),
                    bgm_path=str(bgm_file),
                    output_audio_path=str(mixed_audio),
                    bgm_volume=bgm_volume
                )
            except Exception as e:
                print(f"Warning: BGM mix failed ({e}), using raw voice.")
                final_audio_path = str(voice_path)

    # 3. Process Visual Media
    output_video_filename = f"video_ai_{ts}.mp4"
    output_video_path = OUTPUTS_DIR / output_video_filename

    try:
        if media_type == "video":
            source_video_path = None
            if use_sample_video:
                sample_p = UPLOADS_DIR / "sample_toc_that.mp4"
                if sample_p.exists():
                    source_video_path = sample_p
            elif video_file and video_file.filename:
                saved_video = UPLOADS_DIR / f"upload_{ts}_{video_file.filename}"
                with open(saved_video, "wb") as f:
                    shutil.copyfileobj(video_file.file, f)
                source_video_path = saved_video

            if not source_video_path or not os.path.exists(source_video_path):
                # Fallback to sample if available
                sample_p = UPLOADS_DIR / "sample_toc_that.mp4"
                if sample_p.exists():
                    source_video_path = sample_p
                else:
                    raise HTTPException(status_code=400, detail="Vui lòng tải lên file video!")

            video_service.create_video_from_video(
                video_input_path=str(source_video_path),
                audio_input_path=final_audio_path,
                output_video_path=str(output_video_path),
                aspect_ratio=aspect_ratio
            )

        elif media_type == "images":
            if not image_files or len(image_files) == 0:
                raise HTTPException(status_code=400, detail="Vui lòng chọn ít nhất 1 hình ảnh!")

            saved_images = []
            for idx, img in enumerate(image_files):
                if not img.filename:
                    continue
                img_path = UPLOADS_DIR / f"img_{ts}_{idx}_{img.filename}"
                with open(img_path, "wb") as f:
                    shutil.copyfileobj(img.file, f)
                saved_images.append(str(img_path))

            if not saved_images:
                raise HTTPException(status_code=400, detail="Không có ảnh hợp lệ nào được tải lên!")

            video_service.create_video_from_images(
                image_paths=saved_images,
                audio_input_path=final_audio_path,
                output_video_path=str(output_video_path),
                aspect_ratio=aspect_ratio if aspect_ratio in ["9:16", "16:9"] else "9:16"
            )

        final_dur = video_service.get_media_duration(str(output_video_path))
        file_size_mb = output_video_path.stat().st_size / (1024 * 1024)

        return {
            "status": "success",
            "video_url": f"/outputs/{output_video_filename}",
            "filename": output_video_filename,
            "duration": round(final_dur, 2),
            "size_mb": round(file_size_mb, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý video: {e}")

@app.get("/api/history")
async def get_history():
    """Retrieve previously rendered videos."""
    videos = []
    if OUTPUTS_DIR.exists():
        for f in sorted(OUTPUTS_DIR.glob("video_*.mp4"), key=os.path.getmtime, reverse=True):
            try:
                sz = round(f.stat().st_size / (1024 * 1024), 2)
                videos.append({
                    "filename": f.name,
                    "url": f"/outputs/{f.name}",
                    "size_mb": sz,
                    "time": time.strftime("%H:%M %d/%m/%Y", time.localtime(f.stat().st_mtime))
                })
            except:
                pass
    return {"history": videos[:15]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
