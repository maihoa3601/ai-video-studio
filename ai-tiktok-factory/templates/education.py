"""
Educational script template for AI knowledge and concepts.
Spoken Vietnamese, authentic explanations, zero fake metrics.
"""

from typing import Dict, Any, List
import config

def generate_education_script(topic: str, duration: int = 30, cta: str = "") -> Dict[str, Any]:
    """
    Generate an authentic, spoken Vietnamese educational TikTok script.
    Follows: HOOK -> EXPLAIN CONCEPT -> REAL EXAMPLES -> BENEFIT -> CTA.
    """
    clean_topic = topic.strip().rstrip("?.!")
    default_cta = cta if cta else f"Follow kênh {config.CHANNEL_NAME} và comment AI."
    
    # Authentic, human narrative specifically explaining AI without corporate jargon
    all_sections = [
        {
            "role": "HOOK",
            "text": "AI không còn là chuyện của tương lai. Có thể hôm nay bạn đã dùng AI nhiều lần mà không nhận ra.",
            "est_sec": 5.5,
            "beats": [
                {
                    "component": "kinetic_text",
                    "text": "AI không còn là chuyện của tương lai.",
                    "headline_top": "AI KHÔNG CÒN LÀ",
                    "headline_main": "CHUYỆN TƯƠNG LAI",
                    "est_sec": 2.6
                },
                {
                    "component": "chat_ui",
                    "transition": "slideleft",
                    "text": "Có thể hôm nay bạn đã dùng AI nhiều lần mà không nhận ra.",
                    "user_prompt": "Hôm nay tôi đã dùng AI ở đâu?",
                    "ai_response": "Tìm kiếm, bản đồ, lọc email và camera điện thoại của bạn đều có AI!",
                    "est_sec": 2.9
                }
            ]
        },
        {
            "role": "EXPLAIN_CONCEPT",
            "text": "Hiểu đơn giản, AI là công nghệ giúp máy tính học từ dữ liệu để nhận biết, dự đoán hoặc tạo ra kết quả.",
            "est_sec": 7.5,
            "beats": [
                {
                    "component": "workflow",
                    "transition": "slideup",
                    "active_step": 1,
                    "text": "Hiểu đơn giản, AI là công nghệ giúp máy tính học từ dữ liệu",
                    "est_sec": 3.7
                },
                {
                    "component": "workflow",
                    "transition": "fade",
                    "active_step": 3,
                    "text": "để nhận biết, dự đoán hoặc tạo ra kết quả.",
                    "est_sec": 3.8
                }
            ]
        },
        {
            "role": "REAL_EXAMPLES",
            "text": "AI có thể xử lý công việc lặp lại, tổng hợp thông tin, tạo nội dung, hình ảnh và giọng nói.",
            "est_sec": 7.5,
            "beats": [
                {
                    "component": "icon_grid",
                    "transition": "slideleft",
                    "highlight_card": 1,
                    "text": "AI có thể xử lý công việc lặp lại, tổng hợp thông tin,",
                    "est_sec": 3.7
                },
                {
                    "component": "image_scene",
                    "transition": "fade",
                    "prompt": "Tạo nội dung, hình ảnh và giọng nói AI chân thực...",
                    "text": "tạo nội dung, hình ảnh và giọng nói.",
                    "est_sec": 3.8
                }
            ]
        },
        {
            "role": "BENEFIT",
            "text": "Điều quan trọng không phải dùng thật nhiều AI, mà là biết chọn đúng công cụ cho công việc.",
            "est_sec": 6.5,
            "beats": [
                {
                    "component": "comparison",
                    "transition": "slideright",
                    "active_side": "left",
                    "text": "Điều quan trọng không phải dùng thật nhiều AI,",
                    "est_sec": 3.2
                },
                {
                    "component": "comparison",
                    "transition": "fade",
                    "active_side": "right",
                    "text": "mà là biết chọn đúng công cụ cho công việc.",
                    "est_sec": 3.3
                }
            ]
        },
        {
            "role": "CTA",
            "text": f"Muốn mình test những công cụ AI đáng dùng? {default_cta}",
            "est_sec": 5.5,
            "beats": [
                {
                    "component": "cta",
                    "transition": "slideup",
                    "cta_mode": "question",
                    "text": "Muốn mình test những công cụ AI đáng dùng?",
                    "est_sec": 2.5
                },
                {
                    "component": "cta",
                    "transition": "fadewhite",
                    "cta_mode": "action",
                    "text": default_cta,
                    "est_sec": 3.0
                }
            ]
        }
    ]

    full_text = " ".join([s["text"] for s in all_sections])

    return {
        "topic": topic,
        "type": "education",
        "duration": duration,
        "full_text": full_text,
        "sections": all_sections
    }
