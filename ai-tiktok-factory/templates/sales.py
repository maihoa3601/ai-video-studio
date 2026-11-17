"""
Sales and service script template for legitimate AI solutions.
Focuses on authentic value: training, automation consulting, official setup, verified prompt packs.
Strictly prohibits cracked, shared, or illegal account offers.
"""

from typing import Dict, Any
import config

def generate_sales_script(topic: str, duration: int = 30, cta: str = "") -> Dict[str, Any]:
    """
    Generate an ethical and compliant sales TikTok script.
    Follows: HOOK -> PROBLEM -> SOLUTION -> BENEFIT -> CTA.
    """
    clean_topic = topic.strip().rstrip("?.!")
    default_cta = cta if cta else f"Nhắn tin cho kênh {config.CHANNEL_NAME} để nhận tư vấn và giải pháp phù hợp nhất!"
    
    if duration <= 35:
        hook = f"Bạn đang tốn quá nhiều thời gian mỗi ngày cho các công việc thủ công?"
        problem = "Quy trình làm việc rời rạc khiến năng suất của bạn bị kìm hãm nghiêm trọng."
        main_points = [
            f"Giải pháp tối ưu hiện nay là ứng dụng quy trình chuẩn hóa cùng {clean_topic}.",
            "Chúng tôi hỗ trợ bạn thiết lập hệ thống tự động hóa hoàn chỉnh và đào tạo trực tiếp.",
            "Bạn sẽ làm chủ công nghệ và cắt giảm được ít nhất 50% thời gian xử lý công việc."
        ]
        result = "Đầu tư vào kỹ năng và công cụ bài bản là cách nhanh nhất để tạo bước nhảy vọt."
    elif duration <= 50:
        hook = f"Đã đến lúc nâng cấp cách bạn làm việc với giải pháp {clean_topic} chuyên nghiệp!"
        problem = "Nhiều doanh nghiệp và cá nhân muốn chuyển đổi số nhưng thiếu lộ trình áp dụng bài bản."
        main_points = [
            "Chúng tôi mang đến dịch vụ tư vấn và setup quy trình ứng dụng AI thực chiến.",
            "Tất cả quy trình đều được tùy chỉnh riêng theo đúng nhu cầu và bảo mật tuyệt đối.",
            "Đội ngũ chuyên gia đồng hành hướng dẫn từng bước cho đến khi vận hành trơn tru.",
            "Bạn hoàn toàn yên tâm về tính bền vững, minh bạch và hiệu quả lâu dài."
        ]
        result = "Tối ưu hóa chi phí vận hành và tăng tốc độ phục vụ khách hàng lên gấp 3 lần."
    else:
        hook = f"Bí quyết giúp các chuyên gia hàng đầu tăng gấp đôi hiệu suất công việc là gì?"
        problem = "Tự mày mò thử sai có thể khiến bạn mất hàng tháng trời mà vẫn không đạt được kết quả mong muốn."
        main_points = [
            f"Đó là lý do gói giải pháp {clean_topic} được thiết kế để giải quyết triệt để bài toán này.",
            "Cung cấp trọn bộ tài liệu thực chiến, kho câu lệnh chuẩn và phương pháp ứng dụng thực tế.",
            "Kèm theo dịch vụ hỗ trợ kỹ thuật và cập nhật công nghệ mới liên tục.",
            "Cam kết đồng hành giải đáp 1-1, giúp bạn ứng dụng được ngay vào công việc hàng ngày.",
            "Không chỉ tiết kiệm thời gian, bạn còn tạo ra những sản phẩm chất lượng vượt bậc."
        ]
        result = "Hàng trăm học viên và đối tác đã thay đổi hoàn toàn cách vận hành công việc."

    all_sections = [
        {"role": "HOOK", "text": hook, "est_sec": 3.0, "headline": "TỐI ƯU NĂNG SUẤT"},
        {"role": "PROBLEM", "text": problem, "est_sec": 6.0, "headline": "VẤN ĐỀ BẠN GẶP PHẢI"},
    ]
    
    per_point_time = (duration - 14.0) / len(main_points)
    for i, pt in enumerate(main_points, 1):
        all_sections.append({
            "role": f"POINT_{i}",
            "text": pt,
            "est_sec": per_point_time,
            "headline": f"GIẢI PHÁP THỰC TẾ {i}"
        })
        
    all_sections.append({
        "role": "RESULT",
        "text": result,
        "est_sec": 4.0,
        "headline": "LỢI ÍCH CAM KẾT"
    })
    all_sections.append({
        "role": "CTA",
        "text": default_cta,
        "est_sec": 4.0,
        "headline": "LIÊN HỆ NGAY"
    })

    full_text = " ".join([s["text"] for s in all_sections])

    return {
        "topic": topic,
        "type": "sales",
        "duration": duration,
        "full_text": full_text,
        "sections": all_sections
    }
