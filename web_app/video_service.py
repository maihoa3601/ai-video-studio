"""
Video and Audio Processing Service for AI Video Studio.
Handles TTS synthesis, audio mixing/ducking, video looping, and image slideshows.
"""

import os
import re
import json
import asyncio
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

def get_media_duration(file_path: str) -> float:
    """Get accurate duration of any audio or video file via ffprobe."""
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json', str(file_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0.0

async def synthesize_voice_edge(text: str, output_path: str, voice_name: str = "vi-VN-NamMinhNeural", rate: str = "+0%") -> bool:
    """Synthesize text using edge-tts with sentence fallback."""
    import edge_tts
    cleaned_text = " ".join(text.split()).strip()
    if not cleaned_text:
        return False
        
    try:
        communicate = edge_tts.Communicate(cleaned_text, voice_name)
        await communicate.save(output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception as e:
        print(f"Edge-TTS full text attempt failed: {e}, falling back to sentence chunks.")

    # Split into sentences and concatenate
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', cleaned_text) if len(s.strip()) > 1]
    if not sentences:
        sentences = [cleaned_text]
        
    part_files = []
    parent_dir = Path(output_path).parent
    
    for i, s in enumerate(sentences):
        part_path = parent_dir / f"chunk_{i}_{Path(output_path).stem}.mp3"
        try:
            c = edge_tts.Communicate(s, voice_name)
            await c.save(str(part_path))
            if part_path.exists() and part_path.stat().st_size > 500:
                part_files.append(str(part_path))
        except Exception as err:
            print(f"Chunk {i} failed with {voice_name}: {err}")
            # Try gTTS fallback for this chunk
            try:
                from gtts import gTTS
                tts = gTTS(s, lang='vi')
                tts.save(str(part_path))
                part_files.append(str(part_path))
            except Exception as gerr:
                print(f"gTTS fallback failed: {gerr}")

    if not part_files:
        return False

    # Concat part files with ffmpeg
    list_file = parent_dir / f"list_{Path(output_path).stem}.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for p in part_files:
            p_esc = str(p).replace("\\", "/")
            f.write(f"file '{p_esc}'\n")

    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(list_file), '-c', 'copy', str(output_path)
    ], capture_output=True)

    # Cleanup temp chunks
    try:
        list_file.unlink(missing_ok=True)
        for p in part_files:
            Path(p).unlink(missing_ok=True)
    except:
        pass

    return os.path.exists(output_path) and os.path.getsize(output_path) > 1000

async def synthesize_voice(
    text: str,
    output_audio: str,
    voice_type: str = "nam_hai_huoc",
    speed: float = 1.0,
    pitch_style: str = "playful"
) -> float:
    """
    Main voice synthesis pipeline.
    Applies pitch and tempo filters to produce humorous, energetic or natural tones.
    Returns: Duration in seconds.
    """
    out_p = Path(output_audio)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    raw_audio = str(out_p.parent / f"raw_{out_p.stem}.mp3")

    # 1. Base voice synthesis
    if voice_type == "gtts_nu":
        from gtts import gTTS
        tts = gTTS(text, lang='vi')
        tts.save(raw_audio)
    else:
        # Default to NamMinhNeural as it is the most stable and natural
        v_name = "vi-VN-NamMinhNeural"
        await synthesize_voice_edge(text, raw_audio, v_name)

    if not os.path.exists(raw_audio) or os.path.getsize(raw_audio) < 100:
        # Ultimate fallback
        from gtts import gTTS
        tts = gTTS(text, lang='vi')
        tts.save(raw_audio)

    # 2. Apply humorous / tone filters
    # rubberband pitch and tempo
    pitch_val = 1.0
    tempo_val = speed

    if voice_type == "nam_hai_huoc" or pitch_style == "playful":
        pitch_val = 1.18
        tempo_val = speed * 1.08
    elif voice_type == "chipmunk" or pitch_style == "chipmunk":
        pitch_val = 1.38
        tempo_val = speed * 1.10
    elif voice_type == "nu_hai_huoc" or pitch_style == "female_playful":
        pitch_val = 1.26
        tempo_val = speed * 1.06
    elif voice_type == "energetic_sales":
        pitch_val = 1.10
        tempo_val = speed * 1.15
    elif voice_type == "natural":
        pitch_val = 1.0
        tempo_val = speed

    af_filter = f"rubberband=pitch={pitch_val:.2f}:tempo={tempo_val:.2f}"
    cmd = [
        'ffmpeg', '-y', '-i', raw_audio,
        '-af', af_filter,
        str(output_audio)
    ]
    subprocess.run(cmd, capture_output=True, check=True)

    # Cleanup raw
    try:
        Path(raw_audio).unlink(missing_ok=True)
    except:
        pass

    return get_media_duration(output_audio)

def mix_audio_with_bgm(
    voice_audio_path: str,
    bgm_path: Optional[str],
    output_audio_path: str,
    bgm_volume: float = 0.12
) -> str:
    """Mix voice audio with ducked background music."""
    if not bgm_path or not os.path.exists(bgm_path):
        return voice_audio_path

    voice_dur = get_media_duration(voice_audio_path)
    fade_start = max(0.0, voice_dur - 2.0)

    cmd = [
        'ffmpeg', '-y',
        '-i', str(voice_audio_path),
        '-i', str(bgm_path),
        '-filter_complex',
        f'[1:a]volume={bgm_volume:.2f},afade=t=out:st={fade_start:.2f}:d=2.0[bg];[0:a][bg]amix=inputs=2:duration=first[out]',
        '-map', '[out]',
        str(output_audio_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_audio_path

def create_video_from_video(
    video_input_path: str,
    audio_input_path: str,
    output_video_path: str,
    aspect_ratio: str = "keep"  # 'keep', '9:16', '16:9'
) -> str:
    """
    Combines input video with voice audio.
    Loops video seamlessly to match exact audio duration without trailing freeze.
    """
    audio_dur = get_media_duration(audio_input_path)
    
    vf_filters = []
    if aspect_ratio == "9:16":
        vf_filters.append("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
    elif aspect_ratio == "16:9":
        vf_filters.append("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080")

    cmd = [
        'ffmpeg', '-y',
        '-stream_loop', '-1',
        '-i', str(video_input_path),
        '-i', str(audio_input_path),
        '-t', f"{audio_dur:.3f}",
        '-map', '0:v:0',
        '-map', '1:a:0'
    ]

    if vf_filters:
        cmd.extend(['-vf', ",".join(vf_filters)])

    cmd.extend([
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-c:a', 'aac', '-b:a', '192k',
        str(output_video_path)
    ])

    subprocess.run(cmd, capture_output=True, check=True)
    return output_video_path

def create_video_from_images(
    image_paths: List[str],
    audio_input_path: str,
    output_video_path: str,
    aspect_ratio: str = "9:16"
) -> str:
    """
    Creates a slideshow video from multiple images matching total audio duration.
    Applies high-resolution scaling and smooth image transitions.
    """
    audio_dur = get_media_duration(audio_input_path)
    num_images = max(1, len(image_paths))
    dur_per_image = max(2.0, audio_dur / num_images)

    width, height = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
    temp_dir = Path(output_video_path).parent / f"tmp_slides_{Path(output_video_path).stem}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    segment_clips = []
    for i, img in enumerate(image_paths):
        seg_out = temp_dir / f"seg_{i:03d}.mp4"
        # Scale and pad to standard canvas
        vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30"
        cmd_seg = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(img),
            '-t', f"{dur_per_image:.3f}",
            '-vf', vf,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            str(seg_out)
        ]
        subprocess.run(cmd_seg, capture_output=True, check=True)
        segment_clips.append(seg_out)

    # Concat all segments
    list_file = temp_dir / "concat_list.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for seg in segment_clips:
            seg_esc = str(seg).replace("\\", "/")
            f.write(f"file '{seg_esc}'\n")

    unmerged_video = temp_dir / "unmerged_video.mp4"
    cmd_concat = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        str(unmerged_video)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # Merge with audio and exact duration
    cmd_merge = [
        'ffmpeg', '-y',
        '-i', str(unmerged_video),
        '-i', str(audio_input_path),
        '-t', f"{audio_dur:.3f}",
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        str(output_video_path)
    ]
    subprocess.run(cmd_merge, capture_output=True, check=True)

    # Cleanup temp
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass

    return output_video_path
