"""
Comparison script template for AI tools.
E.g., "ChatGPT vs Gemini: Chọn cái nào cho công việc?"
"""

from typing import Dict, Any
import config

def generate_comparison_script(topic: str, duration: int = 30, cta: str = "") -> Dict[str, Any]:
    """Generate a comparison TikTok script based on topic and duration."""
    
    clean_topic = topic.strip().rstrip("?.!")
    default_cta = cta if cta else f"Follow kênh {config.CHANNEL_NAME} và bình luận công cụ bạn yêu thích nhất nhé!"
    
    if duration <= 35:
        hook = f"Đang phân vân giữa {clean_topic}? Đây là câu trả lời cho bạn!"
        problem = "Cả hai đều là những mô hình hàng đầu hiện nay, nhưng mỗi bên lại mạnh ở một khía cạnh riêng."
        main_points = [
            "Nếu bạn cần sự sáng tạo, viết lách mượt mà và phân tích logic chặt chẽ, bên thứ nhất vượt trội hơn.",
            "Còn nếu bạn cần tra cứu thông tin thời gian thực, tích hợp hệ sinh thái đám mây, bên thứ hai là quán quân.",
            "Về tốc độ phản hồi, cả hai đều xử lý cực nhanh và hỗ trợ tiếng Việt rất tốt."
        ]
        result = "Tùy thuộc vào nhu cầu thực tế của bạn, chọn đúng công cụ sẽ giúp công việc tăng tốc gấp đôi."
    elif duration <= 50:
        hook = f"So sánh toàn diện {clean_topic}: Ai mới là người chiến thắng?"
        problem = "Nhiều người lầm tưởng công cụ nào cũng giống nhau, nhưng chọn sai có thể làm bạn mất thêm thời gian."
        main_points = [
            "Thứ nhất về khả năng lập trình và xử lý tác vụ phức tạp, một bên thể hiện độ chính xác vượt bậc.",
            "Thứ hai về khả năng cập nhật tin tức và đọc link trực tiếp, bên đối trọng lại chiếm ưu thế tuyệt đối.",
            "Về mức độ tự nhiên trong câu từ tiếng Việt, cả hai ngày càng hoàn thiện và khó phân định thắng thua.",
            "Giải pháp thông minh nhất là phối hợp cả hai công cụ cho từng công việc cụ thể."
        ]
        result = "Hiểu rõ thế mạnh của từng bên sẽ giúp bạn tối ưu hóa 100% hiệu suất."
    else:
        hook = f"Đại chiến AI: {clean_topic}, đâu mới là lựa chọn số một hiện tại?"
        problem = "Cuộc đua trí tuệ nhân tạo đang diễn ra khốc liệt, và đây là những khác biệt sống còn bạn cần biết."
        main_points = [
            "Khía cạnh thứ nhất là độ nhạy bén và khả năng thấu hiểu ngữ cảnh dài hàng trăm trang tài liệu.",
            "Khía cạnh thứ hai là khả năng tích hợp công việc hàng ngày như email, lịch họp và tài liệu văn phòng.",
            "Về trải nghiệm người dùng, một bên có giao diện trực quan, bên kia lại có tốc độ tải siêu tốc.",
            "Đặc biệt về chi phí, cả hai đều có phiên bản miễn phí đủ mạnh cho người dùng phổ thông.",
            "Khi nâng cấp gói chuyên nghiệp, sự khác biệt mới bộc lộ rõ ở các tác vụ phân tích chuyên sâu."
        ]
        result = "Lời khuyên là hãy trải nghiệm cả hai để tìm ra người bạn đồng hành ăn ý nhất."

    all_sections = [
        {"role": "HOOK", "text": hook, "est_sec": 3.0, "headline": "CUỘC CHIẾN AI"},
        {"role": "PROBLEM", "text": problem, "est_sec": 6.0, "headline": "KHÁC BIỆT CỐT LÕI"},
    ]
    
    per_point_time = (duration - 14.0) / len(main_points)
    for i, pt in enumerate(main_points, 1):
        all_sections.append({
            "role": f"POINT_{i}",
            "text": pt,
            "est_sec": per_point_time,
            "headline": f"SO SÁNH TIÊU CHÍ {i}"
        })
        
    all_sections.append({
        "role": "RESULT",
        "text": result,
        "est_sec": 4.0,
        "headline": "LỰA CHỌN TỐI ƯU"
    })
    all_sections.append({
        "role": "CTA",
        "text": default_cta,
        "est_sec": 4.0,
        "headline": "BÌNH LUẬN NGAY"
    })

    full_text = " ".join([s["text"] for s in all_sections])

    return {
        "topic": topic,
        "type": "comparison",
        "duration": duration,
        "full_text": full_text,
        "sections": all_sections
    }
