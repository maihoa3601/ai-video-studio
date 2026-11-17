"""
Vietnamese text processing utilities.
Chunking, wrapping, keyword extraction, and subtitle line breaking.
"""

import re
from typing import List, Tuple

# Common impactful words to highlight in captions if present
HIGHLIGHT_PATTERNS = [
    r"\bAI\b", r"\bChatGPT\b", r"\bGemini\b", r"\bClaude\b", r"\bDeepSeek\b",
    r"\bMIỄN PHÍ\b", r"\bTỰ ĐỘNG\b", r"\bTIẾT KIỆM\b", r"\bCỰC NHANH\b",
    r"\bBÍ MẬT\b", r"\bĐỘT PHÁ\b", r"\bCÔNG CỤ\b", r"\bGIẢI PHÁP\b",
    r"\bHIỆU QUẢ\b", r"\bX2\b", r"\bX3\b", r"\bX5\b", r"\bX10\b",
    r"\b100%\b", r"\bTOP 1\b", r"\bLỢI ÍCH\b", r"\bLƯU NGAY\b"
]

def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences while respecting Vietnamese punctuation."""
    # Normalize spaces and line breaks
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?…])\s+", text)
    return [s.strip() for s in sentences if s.strip()]

def split_sentence_into_phrases(sentence: str, max_words_per_phrase: int = 4) -> List[str]:
    """
    Split a sentence into phrase-level chunks (2-5 words per chunk)
    for fast-paced TikTok subtitle display.
    """
    words = sentence.split()
    if not words:
        return []
    
    phrases = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        # Break chunk if reaches limit or word ends with comma/colon/dash
        if len(current_chunk) >= max_words_per_phrase or word.endswith((",", ";", ":", "-")):
            phrases.append(" ".join(current_chunk))
            current_chunk = []
            
    if current_chunk:
        # If the trailing chunk is just 1 word and we have previous phrases, merge
        if len(current_chunk) == 1 and phrases:
            phrases[-1] += " " + current_chunk[0]
        else:
            phrases.append(" ".join(current_chunk))
            
    return phrases

def wrap_text_lines(text: str, max_chars_per_line: int = 24, max_lines: int = 2) -> List[str]:
    """
    Wrap text into at most max_lines, each having at most max_chars_per_line.
    Ideal for TikTok center captions.
    """
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = []
    current_len = 0

    for word in words:
        word_len = len(word)
        if current_line and (current_len + 1 + word_len) > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_len = word_len
            if len(lines) >= max_lines - 1:
                # If we're at the last line limit, place all remaining words here
                break
        else:
            current_line.append(word)
            current_len += (1 if current_len > 0 else 0) + word_len

    # Add any remaining words
    remaining_idx = len([w for line in lines for w in line.split()])
    if remaining_idx < len(words):
        lines.append(" ".join(words[remaining_idx:]))
    elif current_line:
        lines.append(" ".join(current_line))

    return lines[:max_lines]

def extract_highlight_keywords(text: str) -> List[str]:
    """Find words or phrases that should be emphasized visually."""
    found = set()
    for pattern in HIGHLIGHT_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            found.add(m.strip())
            
    # Also find any numbers or percentages (e.g., 5, 10x, 90%)
    numbers = re.findall(r"\b\d+[%xX]?\b", text)
    for n in numbers:
        found.add(n)
        
    return list(found)
