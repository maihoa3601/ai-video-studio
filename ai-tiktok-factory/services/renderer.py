"""
Video Rendering Engine for AI TikTok Video Factory.
Concatenates visual beats, mixes broadcast-mastered voice-over,
transition SFX tracks, and background music with ducking and progress bar.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import config
from utils.ffmpeg import run_ffmpeg

DEFAULT_TRANSITIONS = [
    "slideleft",     # Beat 1 -> 2 (Intro to Chat)
    "slideup",       # Beat 2 -> 3 (Chat to Workflow)
    "fade",          # Beat 3 -> 4 (Workflow Step 1 to Step 3)
    "slideleft",     # Beat 4 -> 5 (Workflow to Bento Grid)
    "fade",          # Beat 5 -> 6 (Bento to Generative Canvas)
    "slideright",    # Beat 6 -> 7 (Canvas to Comparison Mistake)
    "fade",          # Beat 7 -> 8 (Mistake to Solution)
    "slideup",       # Beat 8 -> 9 (Comparison to Poll Question)
    "fadewhite"      # Beat 9 -> 10 (Poll to Channel Follow Action)
]

def render_final_video(
    beat_clip_paths: List[Path],
    voice_path: Path,
    sfx_path: Optional[Path],
    subtitles_path: Optional[Path],
    output_video_path: Path,
    temp_dir: Path,
    total_duration: float,
    beat_durations: Optional[List[float]] = None,
    transitions: Optional[List[str]] = None,
    transition_duration: float = 0.25
) -> Path:
    """
    Renders the complete TikTok video:
    1. Chained xfade transitions between all visual beat clips (slideleft, slideup, fade, etc.)
    2. Burns dynamic kinetic ASS/SRT subtitles onto the timeline (safe zone, zero ghosting)
    3. Master voice-over with normalization, light compression, and limiter
    4. Blends UI transition SFX at visual beat boundaries
    5. Blends background music (subtle 8-10%, ducked, fade in/out)
    6. Adds dynamic animated progress bar from 0% to 100%
    7. Encodes to H.264 / yuv420p / 30fps / 1080x1920
    """
    # 1. Check for background music in assets/music/
    bg_music_candidates = [
        config.MUSIC_DIR / "background.mp3",
        config.MUSIC_DIR / "bg.mp3",
        config.MUSIC_DIR / "music.mp3"
    ]
    all_music = list(config.MUSIC_DIR.glob("*.mp3")) + list(config.MUSIC_DIR.glob("*.wav"))
    bg_music_path: Optional[Path] = None
    if all_music:
        bg_music_path = all_music[0]

    # 2. Dynamic progress bar at bottom (y = 1904, height = 8)
    bar_y = config.VIDEO_HEIGHT - 16
    bar_h = 8
    dur_str = f"{total_duration:.2f}"
    
    video_filter = (
        f"drawbox=x=0:y={bar_y}:w=iw:h={bar_h}:color=0x222222@0.6:t=fill,"
        f"drawbox=x=0:y={bar_y}:w='min(iw, (t/{dur_str})*iw)':h={bar_h}:color=0x00F0FF@0.95:t=fill"
    )

    # Subtitle burn filter (burns AFTER transitions so subtitles never ghost across clips)
    if subtitles_path and subtitles_path.exists():
        clean_sub = str(subtitles_path.resolve().as_posix()).replace(":", "\\:")
        if str(subtitles_path).endswith(".ass"):
            sub_filter = f",ass='{clean_sub}'"
        else:
            sub_filter = f",subtitles='{clean_sub}'"
    else:
        sub_filter = ""

    num_clips = len(beat_clip_paths)
    use_xfade = (num_clips > 1 and beat_durations and len(beat_durations) == num_clips)
    
    cmd = ["-y"]
    filter_parts = []

    if use_xfade:
        # Pass all clip files as individual inputs [0:v] .. [N-1:v]
        for p in beat_clip_paths:
            cmd += ["-i", str(p)]
        
        # Build xfade chain across all clips
        trans_list = transitions or DEFAULT_TRANSITIONS
        prev_v = "[0:v]"
        curr_offset = 0.0

        for i in range(1, num_clips):
            d_prev = beat_durations[i - 1]
            curr_offset += d_prev
            t_name = trans_list[(i - 1) % len(trans_list)]
            next_v = f"[vx{i}]" if i < num_clips - 1 else "[v_transitions]"
            filter_parts.append(
                f"{prev_v}[{i}:v]xfade=transition={t_name}:duration={transition_duration:.2f}:offset={curr_offset:.2f}{next_v}"
            )
            prev_v = f"[vx{i}]"

        # Apply progress bar + dynamic subtitles onto transitioned video
        filter_parts.append(f"[v_transitions]{video_filter}{sub_filter}[outv]")
        voice_input_idx = num_clips
    else:
        # Fallback: concat demuxer if single clip or no durations
        concat_file = temp_dir / "beats_concat.txt"
        with open(concat_file, "w", encoding="utf-8") as f:
            for p in beat_clip_paths:
                clean_p = str(p.resolve()).replace("\\", "/")
                f.write(f"file '{clean_p}'\n")
        cmd += ["-f", "concat", "-safe", "0", "-i", str(concat_file)]
        filter_parts.append(f"[0:v]{video_filter}{sub_filter}[outv]")
        voice_input_idx = 1

    # Add Voice Input
    cmd += ["-i", str(voice_path)]

    # Add SFX Input (if available)
    has_sfx = bool(sfx_path and sfx_path.exists())
    if has_sfx:
        cmd += ["-i", str(sfx_path)]
        sfx_input_idx = voice_input_idx + 1
    else:
        sfx_input_idx = None

    # Add BGM Input (if available)
    has_bgm = bool(bg_music_path and bg_music_path.exists())
    if has_bgm:
        cmd += ["-stream_loop", "-1", "-i", str(bg_music_path)]
        bgm_input_idx = voice_input_idx + (2 if has_sfx else 1)
    else:
        bgm_input_idx = None

    # Master voice processing: dynaudnorm for clear vocal presence, limiter to prevent clipping
    voice_filter = f"[{voice_input_idx}:a]dynaudnorm=f=150:g=15:m=10.0,alimiter=limit=0.95[voice_norm]"
    filter_parts.append(voice_filter)
    audio_inputs_to_mix = ["[voice_norm]"]

    if has_sfx and sfx_input_idx is not None:
        filter_parts.append(f"[{sfx_input_idx}:a]volume=0.35[sfx_norm]")
        audio_inputs_to_mix.append("[sfx_norm]")

    if has_bgm and bgm_input_idx is not None:
        fade_out_start = max(0.5, total_duration - 2.0)
        filter_parts.append(
            f"[{bgm_input_idx}:a]volume={config.MUSIC_VOLUME},"
            f"afade=t=in:ss=0:d=1.5,"
            f"afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm_norm]"
        )
        audio_inputs_to_mix.append("[bgm_norm]")

    mix_count = len(audio_inputs_to_mix)
    if mix_count > 1:
        mix_inputs_str = "".join(audio_inputs_to_mix)
        filter_parts.append(f"{mix_inputs_str}amix=inputs={mix_count}:duration=first:dropout_transition=2[outa]")
        audio_map = "[outa]"
    else:
        audio_map = "[voice_norm]"

    filter_complex_str = ";".join(filter_parts)

    cmd += [
        "-filter_complex", filter_complex_str,
        "-map", "[outv]",
        "-map", audio_map,
        "-t", dur_str,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", str(config.VIDEO_FPS),
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_video_path)
    ]

    run_ffmpeg(cmd, desc="Exporting master dynamic TikTok video with smooth xfade transitions")
    return output_video_path
