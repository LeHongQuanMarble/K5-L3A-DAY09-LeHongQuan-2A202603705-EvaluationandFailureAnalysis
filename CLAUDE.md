# Hướng dẫn cho Claude / agent trong repo này

## Demo Day: luôn kiểm tra chất lượng

Repo này nộp cho Demo Day AI20K. Yêu cầu đầy đủ: @docs/DEMO_DAY_REQUIREMENTS.md
Checklist kiểm tra: @docs/DEMO_DAY_CHECKLIST.md

Quy tắc bắt buộc:

1. Trước khi báo "xong", "sẵn sàng nộp" hoặc tạo PR, chạy phần "Kiểm tra nhanh" trong `docs/DEMO_DAY_CHECKLIST.md`
   và đối chiếu mục liên quan tới thay đổi vừa làm.
2. Mỗi mục chỉ đánh `[x]` khi có bằng chứng chạy được trong lượt này (lệnh, file, link). Không đoán.
3. Không bịa số liệu đánh giá, link video/LangSmith, hoặc feedback người dùng. Thiếu thì báo thiếu.
4. Báo cáo theo mẫu mục E của checklist. Ưu tiên cái còn thiếu: Video demo, Evaluation evidence, Pitch deck.
5. Không commit secrets; không dùng bare `except`; giữ test và CI xanh.
6. Nếu thay đổi làm đổi yêu cầu (BTC cập nhật), sửa `docs/DEMO_DAY_REQUIREMENTS.md` và checklist trong cùng commit.
