"""
Review script template for AI tools.
E.g., "ChatGPT Plus có đáng dùng không?", "Review Claude 3.5 Sonnet"
"""

from typing import Dict, Any
import config

def generate_review_script(topic: str, duration: int = 30, cta: str = "") -> Dict[str, Any]:
    """Generate a review TikTok script based on tool topic and duration."""
    
    clean_topic = topic.strip().rstrip("?.!")
    default_cta = cta if cta else f"Follow kênh {config.CHANNEL_NAME} để xem thêm review các công cụ AI đỉnh cao nhé!"
    
    if duration <= 35:
        hook = f"{clean_topic} thực sự có đáng tiền như lời đồn không?"
        problem = "Rất nhiều bạn đang phân vân không biết công cụ này có giải quyết được công việc thực tế hay không."
        main_points = [
            "Về ưu điểm, tốc độ xử lý và khả năng hiểu ngữ cảnh tiếng Việt cực kỳ ấn tượng.",
            "Nó giúp tóm tắt tài liệu 50 trang chỉ trong 10 giây và viết văn bản rất tự nhiên.",
            "Tuy nhiên, nếu bạn không biết cách ra lệnh chính xác, câu trả lời sẽ khá chung chung."
        ]
        result = "Tóm lại, nếu công việc của bạn gắn liền với xử lý văn bản, đây là khoản đầu tư rất đáng giá."
    elif duration <= 50:
        hook = f"Đừng mua {clean_topic} nếu bạn chưa xem hết video này!"
        problem = "Nhiều người bỏ tiền mua gói trả phí nhưng lại chỉ dùng như một cỗ máy tra cứu thông thường."
        main_points = [
            "Điểm mạnh lớn nhất là khả năng phân tích logic và hỗ trợ lập kế hoạch công việc chuyên sâu.",
            "Bạn có thể tải lên tệp Excel hay tài liệu phức tạp để trích xuất báo cáo ngay lập tức.",
            "Hạn chế là đôi khi dữ liệu chưa được cập nhật theo thời gian thực.",
            "Để đạt hiệu quả 100%, bạn cần chuẩn bị sẵn các câu lệnh mẫu chất lượng."
        ]
        result = "Với dân văn phòng và người làm kinh doanh, công cụ này giúp x2 năng suất rõ rệt."
    else:
        hook = f"Trải nghiệm thực tế sau 6 tháng sử dụng {clean_topic}, có gì đặc biệt?"
        problem = "Giữa ma trận hàng trăm công cụ AI, liệu công cụ này có thực sự vượt trội hay chỉ là trào lưu?"
        main_points = [
            "Đầu tiên về giao diện, cực kỳ thân thiện và dễ làm quen ngay cả với người mới.",
            "Thứ hai về hiệu năng, các tác vụ viết lách, dịch thuật và lập luận đạt độ chuẩn xác rất cao.",
            "Thứ ba là tính năng tạo quy trình tùy chỉnh, giúp bạn lưu sẵn phong cách làm việc riêng.",
            "Điểm trừ nhỏ là thỉnh thoảng hệ thống bị chậm vào các khung giờ cao điểm.",
            "Nhưng xét trên mức chi phí, giá trị nhận lại vượt xa mong đợi."
        ]
        result = f"Nếu bạn muốn tiết kiệm thời gian mỗi ngày, {clean_topic} chắc chắn là lựa chọn hàng đầu."

    all_sections = [
        {"role": "HOOK", "text": hook, "est_sec": 3.0, "headline": "CÓ ĐÁNG TIỀN KHÔNG?"},
        {"role": "PROBLEM", "text": problem, "est_sec": 6.0, "headline": "GÓC NHÌN THỰC TẾ"},
    ]
    
    per_point_time = (duration - 14.0) / len(main_points)
    for i, pt in enumerate(main_points, 1):
        all_sections.append({
            "role": f"POINT_{i}",
            "text": pt,
            "est_sec": per_point_time,
            "headline": f"ĐÁNH GIÁ CHI TIẾT {i}"
        })
        
    all_sections.append({
        "role": "RESULT",
        "text": result,
        "est_sec": 4.0,
        "headline": "KẾT LUẬN CUỐI CÙNG"
    })
    all_sections.append({
        "role": "CTA",
        "text": default_cta,
        "est_sec": 4.0,
        "headline": "CHIA SẺ Ý KIẾN"
    })

    full_text = " ".join([s["text"] for s in all_sections])

    return {
        "topic": topic,
        "type": "review",
        "duration": duration,
        "full_text": full_text,
        "sections": all_sections
    }
