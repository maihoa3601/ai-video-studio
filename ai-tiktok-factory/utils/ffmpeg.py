"""
FFmpeg and ffprobe interface utilities.
Detects ffmpeg binary from PATH or imageio_ffmpeg fallback.
Provides audio/video probing and execution helpers.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

def _find_winget_binary(bin_name: str) -> Optional[str]:
    """Search winget package directories for executable."""
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if not local_app_data:
        return None
    winget_dir = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
    if not winget_dir.exists():
        return None
    for candidate in winget_dir.glob(f"**/{bin_name}.exe"):
        if candidate.is_file():
            return str(candidate)
    return None

def get_ffmpeg_path() -> str:
    """Find FFmpeg binary in system PATH, WinGet packages, or imageio_ffmpeg."""
    # 1. Check system PATH
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg

    # 2. Check WinGet installation path
    winget_ffmpeg = _find_winget_binary("ffmpeg")
    if winget_ffmpeg:
        return winget_ffmpeg

    # 3. Check imageio_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

    raise RuntimeError(
        "Không tìm thấy FFmpeg! Vui lòng cài đặt FFmpeg (VD: winget install Gyan.FFmpeg) "
        "hoặc chạy: pip install imageio-ffmpeg"
    )

def get_ffprobe_path() -> Optional[str]:
    """Find ffprobe binary if available in system PATH or WinGet."""
    sys_ffprobe = shutil.which("ffprobe")
    if sys_ffprobe:
        return sys_ffprobe
    return _find_winget_binary("ffprobe")

def run_ffmpeg(args: List[str], desc: str = "FFmpeg processing") -> subprocess.CompletedProcess:
    """Run an FFmpeg command with error handling."""
    ffmpeg_bin = get_ffmpeg_path()
    cmd = [ffmpeg_bin] + args
    
    # Run process
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    if process.returncode != 0:
        err_msg = process.stderr[-1000:] if process.stderr else "Unknown error"
        raise RuntimeError(f"FFmpeg thất bại trong bước '{desc}':\n{err_msg}")
        
    return process

def get_audio_duration(file_path: Path) -> float:
    """Get accurate audio duration in seconds using mutagen, ffprobe, or ffmpeg."""
    file_str = str(file_path)
    
    # 1. Try mutagen first (very fast and native Python)
    try:
        from mutagen.mp3 import MP3
        from mutagen.wave import WAVE
        if file_str.endswith(".mp3"):
            audio = MP3(file_str)
            return float(audio.info.length)
        elif file_str.endswith(".wav"):
            audio = WAVE(file_str)
            return float(audio.info.length)
    except Exception:
        pass

    # 2. Try ffmpeg probe fallback
    ffmpeg_bin = get_ffmpeg_path()
    cmd = [ffmpeg_bin, "-i", file_str]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="replace")
    
    # Parse Duration: 00:00:30.45
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        hours = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        return hours * 3600 + minutes * 60 + seconds
        
    raise RuntimeError(f"Không thể xác định độ dài file âm thanh: {file_path}")

def probe_video(file_path: Path) -> Dict[str, Any]:
    """
    Get video properties (duration, width, height, fps, codec)
    using ffprobe if present, or ffmpeg -i fallback.
    """
    file_str = str(file_path)
    ffprobe_bin = get_ffprobe_path()

    if ffprobe_bin:
        cmd = [
            ffprobe_bin,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,codec_name:format=duration",
            "-of", "default=noprint_wrappers=1",
            file_str
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
        if res.returncode == 0 and res.stdout:
            info = {}
            for line in res.stdout.strip().split("\n"):
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    info[k] = v
            # Parse fps
            fps = 30.0
            if "r_frame_rate" in info and "/" in info["r_frame_rate"]:
                num, den = info["r_frame_rate"].split("/")
                fps = round(float(num) / float(den), 2)
                
            return {
                "width": int(info.get("width", 0)),
                "height": int(info.get("height", 0)),
                "duration": float(info.get("duration", 0.0)),
                "codec": info.get("codec_name", "unknown"),
                "fps": fps
            }

    # Fallback to ffmpeg -i parsing
    ffmpeg_bin = get_ffmpeg_path()
    res = subprocess.run([ffmpeg_bin, "-i", file_str], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="replace")
    out = res.stderr

    duration = 0.0
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", out)
    if dur_match:
        duration = float(dur_match.group(1)) * 3600 + float(dur_match.group(2)) * 60 + float(dur_match.group(3))

    width, height = 0, 0
    res_match = re.search(r",\s*(\d{3,4})x(\d{3,4})", out)
    if res_match:
        width = int(res_match.group(1))
        height = int(res_match.group(2))

    fps = 30.0
    fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", out)
    if fps_match:
        fps = float(fps_match.group(1))

    codec = "unknown"
    codec_match = re.search(r"Video:\s*([a-zA-Z0-9_-]+)", out)
    if codec_match:
        codec = codec_match.group(1)

    return {
        "width": width,
        "height": height,
        "duration": duration,
        "codec": codec,
        "fps": fps
    }
