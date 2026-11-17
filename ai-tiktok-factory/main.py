"""
AI TikTok Video Factory - CLI and Main Pipeline Entrypoint.
Automated vertical 9:16 video generation with dynamic visual components,
fast visual beats (1-2.5s), kinetic captions, UI transition SFX, and broadcast audio mastering.
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Fix Windows console Unicode encoding (cp1252 -> utf-8)
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from utils.files import slugify, get_output_dir, get_temp_dir, cleanup_temp, save_json, save_text
from utils.ffmpeg import get_ffmpeg_path, probe_video
from services.script_generator import generate_script, create_beats_from_script, rebalance_beat_timings
from services.tts import generate_voice
from services.sfx_generator import build_sfx_timeline_track
from services.subtitles import generate_srt, generate_ass, build_phrase_subtitles
from services.visual_generator import render_beat_clip
from services.renderer import render_final_video

def print_banner():
    banner = f"""
============================================================
              AI TIKTOK VIDEO FACTORY (9:16)
               KÊNH: {config.CHANNEL_NAME.upper()}
      Dynamic Visual Beats • Sound Design • Kinetic Captions
============================================================
"""
    print(banner)

def parse_cli_args():
    parser = argparse.ArgumentParser(description="AI TikTok Video Factory Generator")
    parser.add_argument("--topic", type=str, help="Video topic / subject")
    parser.add_argument("--type", type=str, choices=["education", "review", "comparison", "sales"], help="Video type")
    parser.add_argument("--duration", type=int, choices=[30, 45, 60], help="Target duration in seconds")
    parser.add_argument("--cta", type=str, help="Call to action message")
    parser.add_argument("--voice", type=str, help="Voice ID (e.g. vi-VN-HoaiMyNeural, vi-VN-NamMinhNeural)")
    parser.add_argument("--auto", action="store_true", help="Run without interactive prompts")
    return parser.parse_args()

def interactive_prompt():
    """Prompt user interactively in Vietnamese."""
    print("Chủ đề video:")
    try:
        topic = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
        
    while not topic:
        print("Vui lòng nhập chủ đề video:")
        topic = input("> ").strip()

    print("\nLoại video:")
    print("1. Kiến thức (Education)")
    print("2. Review (Đánh giá công cụ)")
    print("3. So sánh (Comparison)")
    print("4. Bán hàng / Dịch vụ (Sales)")
    choice_type = input("> ").strip()
    type_map = {
        "1": "education",
        "2": "review",
        "3": "comparison",
        "4": "sales"
    }
    video_type = type_map.get(choice_type, "education")

    print("\nThời lượng:")
    print("1. 30 giây")
    print("2. 45 giây")
    print("3. 60 giây")
    choice_dur = input("> ").strip()
    dur_map = {
        "1": 30,
        "2": 45,
        "3": 60
    }
    duration = dur_map.get(choice_dur, 30)

    print("\nCTA (Lời kêu gọi hành động - Nhấn Enter để dùng mặc định):")
    cta = input("> ").strip()

    return topic, video_type, duration, cta

def generate_video_pipeline(topic: str, video_type: str = "education", duration: int = 30, cta: str = "", voice_id: str = None) -> Path:
    """
    Execute the 6-stage video production pipeline:
    [1/6] Generating script...
    [2/6] Creating visual beats...
    [3/6] Generating voice & SFX track...
    [4/6] Creating subtitles...
    [5/6] Rendering dynamic visual beats...
    [6/6] Exporting master video...
    """
    start_time = time.time()
    
    # Verify FFmpeg before starting
    try:
        ffmpeg_exe = get_ffmpeg_path()
    except Exception as e:
        print(f"\n[LỖI NGHIÊM TRỌNG] {e}")
        sys.exit(1)

    # 0. Setup directories and slug
    slug = slugify(topic)
    out_dir = get_output_dir(slug)
    temp_dir = get_temp_dir(slug)
    print(f"\n--- Bắt đầu quy trình sản xuất video cho: '{topic}' ({slug}) ---")

    # [1/6] Generating script...
    print("\n[1/6] Generating script...")
    script_data = generate_script(topic=topic, video_type=video_type, duration=duration, cta=cta)
    script_txt_path = out_dir / "script.txt"
    save_text(script_txt_path, script_data["full_text"])
    print(f"      -> Script saved: {script_txt_path.name} ({len(script_data['full_text'].split())} từ)")

    # [2/6] Creating visual beats...
    print("\n[2/6] Creating visual beats...")
    beats = create_beats_from_script(script_data)
    print(f"      -> Created {len(beats)} visual beats (1-2.5s per beat, 0 static PowerPoint cards).")

    # [3/6] Generating voice & SFX...
    print("\n[3/6] Generating voice & sound design...")
    voice_path = out_dir / "voice.mp3"
    actual_duration = generate_voice(
        text=script_data["full_text"],
        output_file=str(voice_path),
        voice_id=voice_id
    )
    print(f"      -> Voice-over rendered: {voice_path.name} (Độ dài thực tế: {actual_duration:.2f}s)")

    # Rebalance visual beat timeline to match real voice length
    beats = rebalance_beat_timings(beats, actual_duration)
    scenes_json_path = out_dir / "scenes.json"
    save_json(scenes_json_path, beats)
    
    # Build synchronized SFX track with whooshes and pops
    beat_start_times = [b["start"] for b in beats]
    sfx_track_path = temp_dir / "sfx_timeline.wav"
    build_sfx_timeline_track(beat_start_times, actual_duration, sfx_track_path)
    print(f"      -> SFX track generated with {len(beat_start_times)} transition cues.")

    # [4/6] Creating subtitles...
    print("\n[4/6] Creating subtitles...")
    phrase_subs = build_phrase_subtitles(beats)
    srt_path = out_dir / "subtitles.srt"
    generate_srt(phrase_subs, srt_path)
    ass_path = out_dir / "subtitles.ass"
    generate_ass(phrase_subs, ass_path)
    print(f"      -> Generated {len(phrase_subs)} kinetic subtitle phrases: {ass_path.name} & {srt_path.name}")

    # [5/6] Rendering dynamic visual beats...
    print("\n[5/6] Rendering dynamic visual beats...")
    beat_clips = []
    total_beats = len(beats)
    transition_padding = 0.25

    for idx, b in enumerate(beats):
        b_dur = b["duration"]
        clip_path = temp_dir / f"beat_{idx:03d}.mp4"
        comp_name = b.get("component", "kinetic_text").upper()
        print(f"      -> Beat {idx + 1}/{total_beats} [{comp_name}] ({b_dur:.2f}s): \"{b['caption_text'][:25]}...\"")
        render_beat_clip(
            beat=b,
            beat_idx=idx,
            total_beats=total_beats,
            output_clip_path=clip_path,
            temp_dir=temp_dir,
            transition_padding=transition_padding
        )
        beat_clips.append(clip_path)

    # [6/6] Exporting master video...
    print("\n[6/6] Exporting video with smooth transitions & audio mastering...")
    final_video_path = out_dir / "final.mp4"
    beat_durations = [b["duration"] for b in beats]
    transitions = [b.get("transition", "slideleft") for b in beats[1:]]

    render_final_video(
        beat_clip_paths=beat_clips,
        voice_path=voice_path,
        sfx_path=sfx_track_path,
        subtitles_path=ass_path,
        output_video_path=final_video_path,
        temp_dir=temp_dir,
        total_duration=actual_duration,
        beat_durations=beat_durations,
        transitions=transitions,
        transition_duration=transition_padding
    )

    elapsed = time.time() - start_time
    print("\nSUCCESS")
    print(f"output/{slug}/final.mp4")
    print(f"Thời gian render: {elapsed:.1f}s")

    return final_video_path

def main():
    print_banner()
    args = parse_cli_args()

    if args.topic or args.auto:
        topic = args.topic or "AI là gì và tại sao bạn nên biết?"
        video_type = args.type or "education"
        duration = args.duration or 30
        cta = args.cta or ""
        voice_id = args.voice
    else:
        topic, video_type, duration, cta = interactive_prompt()
        voice_id = None

    try:
        final_file = generate_video_pipeline(
            topic=topic,
            video_type=video_type,
            duration=duration,
            cta=cta,
            voice_id=voice_id
        )

        info = probe_video(final_file)
        print("\n============================================================")
        print(" THÔNG SỐ VIDEO XUẤT XƯỞNG (FFPROBE VERIFIED)")
        print("============================================================")
        print(f" Đường dẫn : {final_file.resolve()}")
        print(f" Độ phân giải : {info.get('width')}x{info.get('height')} (Chuẩn 9:16 dọc)")
        print(f" Frame Rate   : {info.get('fps')} FPS")
        print(f" Video Codec  : {info.get('codec')}")
        print(f" Thời lượng   : {info.get('duration'):.2f} giây")
        print("============================================================\n")

    except KeyboardInterrupt:
        print("\n[Hủy] Người dùng đã dừng chương trình.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[LỖI THỰC THI] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
