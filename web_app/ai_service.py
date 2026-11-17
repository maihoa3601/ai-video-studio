"""
AI Script Generator and Polisher Service.
Supports Gemini API, OpenAI API, Groq, and Smart Local Templates.
"""

import os
import json
import requests
from typing import Optional, Dict, Any

SYSTEM_PROMPT_HUMOR = """Bạn là chuyên gia sáng tạo nội dung và đạo diễn kịch bản video TikTok/Reels hàng đầu tại Việt Nam.
Phong cách của bạn: cực kỳ hài hước, dí dỏm, tếu táo, lém lỉnh, dùng từ ngữ trendy tự nhiên (như 'đỉnh nóc kịch trần bay phấp phới', 'xỉu up xỉu down', 'bao đẹp bao xịn', 'không mua là tiếc đứt ruột').
Yêu cầu:
- Viết kịch bản ngắn gọn, gãy gọn để đọc lồng tiếng (Voiceover).
- Có câu mở đầu bắt tai (Hook) gây tò mò hoặc bật cười ngay trong 3 giây đầu.
- Phần thân nêu bật điểm vượt trội của sản phẩm/chủ đề một cách vui vẻ, duyên dáng.
- Đoạn kết kêu gọi hành động (Call To Action - bấm giỏ hàng / nhắn tin) thật tự nhiên, hài hước.
- CHỈ TRẢ VỀ DUY NHẤT LỜI THOẠI ĐỂ ĐỌC (Voice-over text). Không kèm chú thích đạo diễn như [Cảnh 1], [Nhạc nổi lên], hay (cười)."""

def generate_script_with_ai(
    topic: str,
    tone: str = "humorous",
    target_duration: int = 30,
    api_provider: str = "gemini",
    api_key: Optional[str] = None,
    custom_notes: Optional[str] = None
) -> str:
    """
    Generate voice-over script using selected AI Provider or smart fallback.
    """
    topic = topic.strip()
    if not topic:
        return "Vui lòng nhập chủ đề hoặc tên sản phẩm!"

    # 1. Try Gemini API if requested and key provided
    if api_provider == "gemini" and api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"""Chủ đề/Sản phẩm: {topic}
Tone giọng: {tone} (hài hước, dí dỏm, lôi cuốn)
Thời lượng dự kiến: khoảng {target_duration} giây (tầm {int(target_duration * 2.8)} từ).
Yêu cầu bổ sung: {custom_notes or 'Tập trung tạo tiếng cười nhẹ nhàng, kích thích người xem tương tác hoặc bấm giỏ hàng.'}

{SYSTEM_PROMPT_HUMOR}"""
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.85, "maxOutputTokens": 600}
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return _clean_script_text(text)
        except Exception as e:
            print(f"Gemini API Error: {e}, falling back to built-in generator.")

    # 2. Try OpenAI API if requested and key provided
    elif api_provider == "openai" and api_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT_HUMOR},
                {"role": "user", "content": f"Viết kịch bản voice-over TikTok cho: {topic}. Tone: {tone}, thời lượng {target_duration}s. {custom_notes or ''}"}
            ]
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.85
            }
            res = requests.post(url, headers=headers, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                text = data["choices"][0]["message"]["content"].strip()
                return _clean_script_text(text)
        except Exception as e:
            print(f"OpenAI API Error: {e}, falling back to built-in generator.")

    # 3. Smart Offline Generator (High-converting templates customized for topic)
    return _generate_smart_offline_script(topic, tone, target_duration)

def polish_script_humor(script: str, api_key: Optional[str] = None, api_provider: str = "gemini") -> str:
    """
    Takes an existing script and rewrites it to be funnier, more playful and catchy.
    """
    if not script.strip():
        return script

    if api_key:
        prompt = f"""Hãy đọc đoạn kịch bản sau và viết lại nó sao cho CỰC KỲ HÀI HƯỚC, lém lỉnh, dí dỏm chuẩn giọng review TikTok siêu cuốn, nhưng vẫn giữ nguyên thông điệp chính và tên sản phẩm.
Chỉ trả về duy nhất lời thoại lồng tiếng, không ghi chú thích.

Kịch bản gốc:
{script}"""
        try:
            if api_provider == "gemini":
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    return _clean_script_text(data["candidates"][0]["content"]["parts"][0]["text"])
            elif api_provider == "openai":
                url = "https://api.openai.com/v1/chat/completions"
                res = requests.post(url, headers={"Authorization": f"Bearer {api_key}"}, json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}]
                }, timeout=20)
                if res.status_code == 200:
                    return _clean_script_text(res.json()["choices"][0]["message"]["content"])
        except Exception as e:
            print(f"Polish Error: {e}")

    # Fallback polish: Add lively TikTok flair
    cleaned = script.strip()
    if not cleaned.endswith((".", "!", "?")):
        cleaned += "."
    return f"Úi chùi ui các bác ơi! {cleaned} Mê chữ ê kéo dài luôn nha, không chốt đơn lẹ tay là hết ráng chịu đó nghen!"

def _clean_script_text(text: str) -> str:
    """Remove markdown formatting, quotes, and parenthetical instructions."""
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove markdown headers and bullets
        if line.startswith(("#", "-", "*", ">")):
            line = line.lstrip("#-* >").strip()
        # Skip stage directions like [Nhạc nền] or (cười)
        if line.startswith(("[", "(")) and line.endswith(("]", ")")):
            continue
        cleaned_lines.append(line)
    return " ".join(cleaned_lines).replace('"', '').strip()

def _generate_smart_offline_script(topic: str, tone: str, duration: int) -> str:
    """Built-in dynamic humorous script creator."""
    if "tóc" in topic.lower():
        return (
            f"Tóc móc tay từ tóc thật một trăm phần trăm, đội lên là tự nhiên như tóc mọc từ da đầu luôn nha cả nhà ơi! "
            f"Bên mình có đủ mẫu từ tóc ngắn cá tính, tóc dài thướt tha, uốn xoăn bồng bềnh cho tới màu highlight chất chơi người dơi cực xinh. "
            f"Bác nào ưng mắt mẫu nào thì cứ click nhẹ vào giỏ hàng góc trái màn hình để rinh về liền tay. "
            f"Còn chị em nào muốn đặt may riêng theo form đầu hay màu sắc phong thủy thì cứ nhắn tin trực tiếp, mình làm tận tâm chiều tới bến luôn nha!"
        )
    elif "quần áo" in topic.lower() or "váy" in topic.lower() or "thời trang" in topic.lower():
        return (
            f"Trời ơi tin được không, mặc em {topic} này lên một cái là dáng chuẩn như hoa hậu liền luôn á mọi người! "
            f"Chất vải mềm mịn mát rượi, đường may giấu chỉ tinh tế từng milimet, mặc đi làm hay đi cà phê sống ảo là ai nhìn cũng phải trầm trồ khen tấm tắc. "
            f"Hiện tại shop đang sẵn đủ size từ bé tí teo tới ngoại cỡ nha. "
            f"Số lượng có hạn nên chị em bấm ngay vào góc màn hình để chốt ngay kẻo tiếc hùi hụi nhé!"
        )
    else:
        return (
            f"Alo alo mọi người ơi, ai đang tìm kiếm chân ái về {topic} thì dừng lại đúng 3 giây ngắm ngay em này nha! "
            f"Phải công nhận là đỉnh của chóp, dùng mê chữ ê kéo dài luôn á. Thiết kế thì đẹp mắt, công năng thì khỏi phải bàn cãi mà giá lại hạt dẻ bất ngờ. "
            f"Ai xem được clip này là duyên tới rồi đó, bấm liền vào giỏ hàng bên dưới để rinh ngay ưu đãi khủng hôm nay nha, số lượng có hạn thôi đó mọi người ơi!"
        )
