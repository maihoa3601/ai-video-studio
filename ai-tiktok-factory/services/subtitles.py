"""
Subtitle Generation Service.
Generates phrase-level TikTok subtitles with keyword highlighting.
Outputs both SRT and ASS format with safe margins for TikTok UI.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
import config
from utils.text import split_sentence_into_phrases, wrap_text_lines, extract_highlight_keywords

def format_timestamp_srt(seconds: float) -> str:
    """Format seconds into SRT timestamp: HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

def format_timestamp_ass(seconds: float) -> str:
    """Format seconds into ASS timestamp: H:MM:SS.cc"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int(round((seconds - int(seconds)) * 100))
    return f"{hrs:01d}:{mins:02d}:{secs:02d}.{centisecs:02d}"

def build_phrase_subtitles(scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Break down scene voice text into phrase-level subtitle chunks (2-4 words)
    with accurate start and end timestamps.
    """
    subtitles = []
    sub_id = 1

    for scene in scenes:
        scene_start = scene["start"]
        scene_end = scene["end"]
        scene_dur = scene_end - scene_start
        voice_text = scene.get("subtitle_text") or scene.get("caption_text") or scene.get("voice") or scene.get("text", "")
        
        # Extract phrases
        phrases = split_sentence_into_phrases(voice_text, max_words_per_phrase=4)
        if not phrases:
            # Fallback to single phrase if short
            if voice_text.strip():
                phrases = [voice_text.strip()]
            else:
                continue

        # Calculate phrase weights based on character length
        total_chars = sum(len(p) for p in phrases)
        if total_chars == 0:
            continue

        current_time = scene_start
        for p in phrases:
            phrase_dur = (len(p) / total_chars) * scene_dur
            phrase_start = current_time
            phrase_end = current_time + phrase_dur
            
            # Wrap lines if needed (max 2 lines)
            wrapped_lines = wrap_text_lines(p, max_chars_per_line=22, max_lines=2)
            display_text = "\n".join(wrapped_lines)
            
            # Detect highlights
            detected_hl = extract_highlight_keywords(p)
            scene_hl = [w for w in scene.get("highlight_words", []) if w.lower() in p.lower()]
            highlights = list(set(detected_hl + scene_hl))

            subtitles.append({
                "id": sub_id,
                "start": round(phrase_start, 3),
                "end": round(phrase_end, 3),
                "duration": round(phrase_dur, 3),
                "text": display_text,
                "raw_phrase": p,
                "highlights": highlights,
                "scene_id": scene.get("beat_id", scene.get("scene_id", 1))
            })
            
            sub_id += 1
            current_time += phrase_dur

    return subtitles

def generate_srt(subtitles: List[Dict[str, Any]], output_path: Path) -> Path:
    """Generate standard .srt subtitle file."""
    lines = []
    for sub in subtitles:
        lines.append(str(sub["id"]))
        start_str = format_timestamp_srt(sub["start"])
        end_str = format_timestamp_srt(sub["end"])
        lines.append(f"{start_str} --> {end_str}")
        lines.append(sub["text"])
        lines.append("")  # Empty line separator

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path

def generate_ass(subtitles: List[Dict[str, Any]], output_path: Path) -> Path:
    """
    Generate Advanced SubStation Alpha (.ass) subtitle file with
    custom fonts, neon borders, and safe margins for TikTok (1080x1920).
    """
    # ASS Header with Segoe UI Semibold / Bold
    font_name = "Segoe UI"
    font_size = 54
    bottom_margin = config.SUBTITLE_BOTTOM_MARGIN  # Default 420
    
    ass_header = f"""[Script Info]
Title: AI TikTok Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTokDefault,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,3,2,60,60,{bottom_margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for sub in subtitles:
        start_str = format_timestamp_ass(sub["start"])
        end_str = format_timestamp_ass(sub["end"])
        
        # Style text with highlight colors if keyword detected
        text = sub["text"].replace("\n", "\\N")
        for kw in sub.get("highlights", []):
            if not kw or len(kw) < 2:
                continue
            # Use negative lookbehind/lookahead to prevent partial word matching (e.g. "lai" -> "lAI")
            kw_esc = re.escape(kw)
            pattern = rf"(?i)(?<!\w){kw_esc}(?!\w)"
            text = re.sub(
                pattern,
                lambda m: f"{{\\c&H0000E6FF&}}{m.group(0).upper()}{{\\c&H00FFFFFF&}}",
                text
            )
            
        events.append(f"Dialogue: 0,{start_str},{end_str},TikTokDefault,,0,0,0,,{text}")

    full_ass = ass_header + "\n".join(events) + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_ass)

    return output_path
