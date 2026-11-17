"""
Script and Visual Beat Generator service.
Supports rule-based templates and external AI LLM providers (OpenAI, Gemini).
Produces structured beat data with assigned visual components and dynamic captions.
"""

import json
from typing import Dict, Any, List
import config
from templates.education import generate_education_script
from templates.review import generate_review_script
from templates.comparison import generate_comparison_script
from templates.sales import generate_sales_script
from utils.text import extract_highlight_keywords

def generate_script(
    topic: str,
    video_type: str = "education",
    duration: int = 30,
    cta: str = ""
) -> Dict[str, Any]:
    """
    Generate TikTok script based on topic, type, and target duration.
    Falls back gracefully to high-quality built-in templates.
    """
    video_type = video_type.lower()
    
    if video_type == "review":
        return generate_review_script(topic, duration, cta)
    elif video_type == "comparison":
        return generate_comparison_script(topic, duration, cta)
    elif video_type == "sales":
        return generate_sales_script(topic, duration, cta)
    else:
        return generate_education_script(topic, duration, cta)

def create_beats_from_script(script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert script sections and sub-beats into a timeline of visual beats (1.0 - 3.5s each).
    Assigns purpose-driven visual components matching the semantic meaning of each beat.
    """
    sections = script_data.get("sections", [])
    beats = []
    current_time = 0.0
    beat_id = 1

    for sec in sections:
        role = sec.get("role", "SCENE")
        sec_beats = sec.get("beats", [])
        
        # If section already has explicit beats defined (like education.py)
        if sec_beats:
            for b in sec_beats:
                est_sec = float(b.get("est_sec", 2.5))
                cap_text = b.get("text", "")
                
                beat_obj = {
                    "beat_id": beat_id,
                    "role": role,
                    "component": b.get("component", "kinetic_text"),
                    "start": round(current_time, 3),
                    "end": round(current_time + est_sec, 3),
                    "duration": round(est_sec, 3),
                    "caption_text": cap_text,
                    "headline_top": b.get("headline_top", "KIẾN THỨC AI"),
                    "headline_main": b.get("headline_main", "ĐỘT PHÁ"),
                    "user_prompt": b.get("user_prompt", "AI giúp gì cho công việc?"),
                    "ai_response": b.get("ai_response", "Tự động hóa tác vụ, tóm tắt và sáng tạo nội dung tức thì!"),
                    "active_step": b.get("active_step", 1),
                    "highlight_card": b.get("highlight_card", 0),
                    "prompt": b.get("prompt", "Tạo ảnh và nội dung chất lượng cao..."),
                    "cta_mode": b.get("cta_mode", "action"),
                    "active_side": b.get("active_side", "all"),
                    "transition": b.get("transition", "slideleft"),
                    "highlight_words": extract_highlight_keywords(cap_text)
                }
                beats.append(beat_obj)
                current_time += est_sec
                beat_id += 1
        else:
            # Auto-split section into 2 beats if long
            sec_text = sec.get("text", "")
            sec_sec = float(sec.get("est_sec", 4.0))
            words = sec_text.split()
            half = len(words) // 2
            
            p1 = " ".join(words[:half]) if half > 0 else sec_text
            p2 = " ".join(words[half:]) if half > 0 else ""
            
            # Select component based on role
            comp = "kinetic_text" if "HOOK" in role else ("workflow" if "CONCEPT" in role or "POINT" in role else ("comparison" if "BENEFIT" in role else "cta"))
            
            beat_obj1 = {
                "beat_id": beat_id,
                "role": role,
                "component": comp,
                "start": round(current_time, 3),
                "end": round(current_time + sec_sec / 2, 3),
                "duration": round(sec_sec / 2, 3),
                "caption_text": p1,
                "headline_top": "KIẾN THỨC",
                "headline_main": "AI MASTER",
                "highlight_words": extract_highlight_keywords(p1)
            }
            beats.append(beat_obj1)
            current_time += sec_sec / 2
            beat_id += 1
            
            if p2:
                beat_obj2 = {
                    "beat_id": beat_id,
                    "role": role,
                    "component": "icon_grid" if comp == "workflow" else comp,
                    "start": round(current_time, 3),
                    "end": round(current_time + sec_sec / 2, 3),
                    "duration": round(sec_sec / 2, 3),
                    "caption_text": p2,
                    "headline_top": "THỰC THI",
                    "headline_main": "GIẢI PHÁP",
                    "highlight_words": extract_highlight_keywords(p2)
                }
                beats.append(beat_obj2)
                current_time += sec_sec / 2
                beat_id += 1

    return beats

def rebalance_beat_timings(beats: List[Dict[str, Any]], actual_total_duration: float) -> List[Dict[str, Any]]:
    """
    Scale visual beat start/end timestamps proportionally so the total matches
    the exact recorded voice duration to the millisecond.
    """
    if not beats:
        return beats
        
    initial_total = sum(b["duration"] for b in beats)
    if initial_total <= 0:
        initial_total = 1.0

    ratio = actual_total_duration / initial_total
    current_time = 0.0

    for b in beats:
        new_dur = round(b["duration"] * ratio, 3)
        b["start"] = round(current_time, 3)
        b["end"] = round(current_time + new_dur, 3)
        b["duration"] = new_dur
        current_time += new_dur

    if beats:
        beats[-1]["end"] = round(actual_total_duration, 3)
        beats[-1]["duration"] = round(actual_total_duration - beats[-1]["start"], 3)

    return beats
