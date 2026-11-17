"""
Visual Engine for AI TikTok Video Factory.
Coordinates visual beat rendering by dispatching to specialized components
(KineticTextScene, WorkflowScene, ChatUIScene, IconGridScene, ComparisonScene, ImageScene, CTAScene)
and applying smooth micro-animations.
"""

from pathlib import Path
from typing import Dict, Any, List
from PIL import Image
import config
from utils.ffmpeg import run_ffmpeg
from services.visual_components import (
    render_kinetic_text_scene,
    render_workflow_scene,
    render_chat_ui_scene,
    render_icon_grid_scene,
    render_comparison_scene,
    render_image_scene,
    render_cta_scene
)

def render_beat_frame(beat: Dict[str, Any], beat_idx: int, total_beats: int) -> Image.Image:
    """
    Generate the visual frame for a specific beat using the assigned component.
    """
    comp = beat.get("component", "kinetic_text").lower()
    caption = beat.get("caption_text", "")

    if comp == "workflow":
        return render_workflow_scene(
            active_step=beat.get("active_step", 1),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    elif comp == "chat_ui":
        return render_chat_ui_scene(
            user_prompt=beat.get("user_prompt", "Hôm nay tôi đã dùng AI ở đâu?"),
            ai_response=beat.get("ai_response", "Tìm kiếm, bản đồ, lọc email và camera điện thoại của bạn đều có AI!"),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    elif comp == "icon_grid":
        return render_icon_grid_scene(
            highlight_card=beat.get("highlight_card", 0),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    elif comp == "comparison":
        return render_comparison_scene(
            active_side=beat.get("active_side", "all"),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    elif comp == "image_scene":
        return render_image_scene(
            prompt_text=beat.get("prompt", "Tạo nội dung, hình ảnh và giọng nói AI chân thực..."),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    elif comp == "cta":
        return render_cta_scene(
            mode=beat.get("cta_mode", "action"),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )
    else:
        # Default: KineticTextScene
        return render_kinetic_text_scene(
            headline_top=beat.get("headline_top", "AI KHÔNG CÒN LÀ"),
            headline_main=beat.get("headline_main", "CHUYỆN TƯƠNG LAI"),
            caption_text=caption,
            beat_idx=beat_idx,
            total_beats=total_beats
        )

def render_beat_clip(
    beat: Dict[str, Any],
    beat_idx: int,
    total_beats: int,
    output_clip_path: Path,
    temp_dir: Path,
    transition_padding: float = 0.25
) -> Path:
    """
    Render a single visual beat clip with smooth micro-animation using FFmpeg.
    Adds transition padding for seamless xfade blending between scenes.
    Ensures exact 1080x1920, 30 FPS, H.264 encoding.
    """
    duration = beat["duration"]
    # Tail padding for xfade overlap (last clip needs no padding)
    effective_duration = duration + (transition_padding if beat_idx < total_beats - 1 else 0.0)
    
    # 1. Generate base frame
    frame_img = render_beat_frame(beat, beat_idx, total_beats)
    frame_img_path = temp_dir / f"beat_frame_{beat_idx:03d}.png"
    frame_img.save(frame_img_path, format="PNG")

    # 2. Silky-smooth ease-in-out continuous micro-animation without jitter
    frames_count = max(1, int(round(effective_duration * config.VIDEO_FPS)))
    
    # Smoothstep interpolation factor: 3*p^2 - 2*p^3 (eases smoothly into and out of motion)
    smooth_p = f"(3*pow(on/{frames_count},2)-2*pow(on/{frames_count},3))"
    
    if beat_idx == 0:
        # Dynamic Hook push-in (1.00 -> 1.045)
        zoom_expr = f"1.00+0.045*{smooth_p}"
    elif beat_idx % 2 == 1:
        # Subtle slow push-in (1.00 -> 1.025)
        zoom_expr = f"1.00+0.025*{smooth_p}"
    else:
        # Subtle slow pull-out (1.025 -> 1.00)
        zoom_expr = f"1.025-0.025*{smooth_p}"

    filter_complex = (
        f"zoompan=z='{zoom_expr}':d={frames_count}:s={config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}:"
        f"fps={config.VIDEO_FPS}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        f"format=yuv420p"
    )

    args = [
        "-y",
        "-loop", "1",
        "-i", str(frame_img_path),
        "-vf", filter_complex,
        "-t", f"{effective_duration:.3f}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-r", str(config.VIDEO_FPS),
        str(output_clip_path)
    ]

    run_ffmpeg(args, desc=f"Render beat {beat_idx + 1}/{total_beats} [{beat.get('component')}]")
    return output_clip_path
