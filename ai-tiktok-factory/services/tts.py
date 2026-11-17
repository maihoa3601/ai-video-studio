"""
Voice-over Text-to-Speech (TTS) Service.
Easily swappable TTS providers (Edge-TTS, OpenAI, ElevenLabs, gTTS).
Defaults to high-quality Microsoft Edge Vietnamese Neural Voices.
"""

import asyncio
import os
from pathlib import Path
from typing import Optional
import config
from utils.ffmpeg import get_audio_duration

async def _synthesize_edge_tts(text: str, output_file: str, voice: str):
    """Synthesize speech using edge-tts (free, neural, high quality) with retry mechanism."""
    import edge_tts
    cleaned_text = " ".join(text.split()).strip()
    
    last_err = None
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(cleaned_text, voice)
            await communicate.save(output_file)
            # Verify file was written and is non-empty
            if os.path.exists(output_file) and os.path.getsize(output_file) > 500:
                return
        except Exception as e:
            last_err = e
            await asyncio.sleep(1.0)
            
    if last_err:
        raise last_err

def _synthesize_openai(text: str, output_file: str, api_key: str, voice: str = "alloy"):
    """Synthesize speech using OpenAI TTS API."""
    import requests
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tts-1",
        "input": text,
        "voice": voice or "alloy"
    }
    res = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=payload, timeout=60)
    res.raise_for_status()
    with open(output_file, "wb") as f:
        f.write(res.content)

def _synthesize_elevenlabs(text: str, output_file: str, api_key: str, voice_id: str):
    """Synthesize speech using ElevenLabs API."""
    import requests
    v_id = voice_id or "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{v_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    res = requests.post(url, headers=headers, json=payload, timeout=60)
    res.raise_for_status()
    with open(output_file, "wb") as f:
        f.write(res.content)

def _synthesize_gtts(text: str, output_file: str):
    """Synthesize speech using gTTS as fallback."""
    from gtts import gTTS
    tts = gTTS(text=text, lang="vi", slow=False)
    tts.save(output_file)

def generate_voice(text: str, output_file: str, voice_id: Optional[str] = None) -> float:
    """
    Main TTS Interface.
    Synthesizes voice from text and saves to output_file.
    Returns: Duration in seconds (float).
    """
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    provider = (config.TTS_PROVIDER or "edge-tts").lower()
    selected_voice = voice_id or config.VOICE_ID or "vi-VN-HoaiMyNeural"

    success = False
    error_log = []

    # 1. Edge-TTS Provider (Default, zero cost, studio quality)
    if provider == "edge-tts":
        try:
            asyncio.run(_synthesize_edge_tts(text, str(out_path), selected_voice))
            success = True
        except Exception as e:
            error_log.append(f"Edge-TTS error: {e}")

    # 2. OpenAI Provider
    elif provider == "openai":
        if not config.TTS_API_KEY:
            raise ValueError("TTS_PROVIDER=openai nhưng thiếu TTS_API_KEY trong file .env!")
        try:
            _synthesize_openai(text, str(out_path), config.TTS_API_KEY, selected_voice)
            success = True
        except Exception as e:
            error_log.append(f"OpenAI TTS error: {e}")

    # 3. ElevenLabs Provider
    elif provider == "elevenlabs":
        if not config.TTS_API_KEY:
            raise ValueError("TTS_PROVIDER=elevenlabs nhưng thiếu TTS_API_KEY trong file .env!")
        try:
            _synthesize_elevenlabs(text, str(out_path), config.TTS_API_KEY, selected_voice)
            success = True
        except Exception as e:
            error_log.append(f"ElevenLabs TTS error: {e}")

    # 4. Fallback attempt with Edge-TTS if other providers failed
    if not success and provider != "edge-tts":
        print(f"[Warning] Provider '{provider}' thất bại. Đang thử chuyển sang fallback Edge-TTS...")
        try:
            asyncio.run(_synthesize_edge_tts(text, str(out_path), "vi-VN-HoaiMyNeural"))
            success = True
        except Exception as e:
            error_log.append(f"Edge-TTS fallback error: {e}")

    # 5. Last resort fallback: gTTS
    if not success:
        try:
            _synthesize_gtts(text, str(out_path))
            success = True
        except Exception as e:
            error_log.append(f"gTTS error: {e}")

    if not success:
        raise RuntimeError(
            f"Không thể tạo file giọng đọc qua bất kỳ provider nào! Lỗi chi tiết:\n" +
            "\n".join(error_log) +
            "\nVui lòng kiểm tra kết nối mạng hoặc cấu hình TTS trong file .env."
        )

    # Return accurate duration
    duration = get_audio_duration(out_path)
    return duration
