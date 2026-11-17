# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Ma trận nhầm lẫn (FAIL = dương) | Tỉ lệ FAIL quan sát → hiệu chỉnh (Rogan-Gladen) | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.80 | tp 24 · fp 4 · fn 6 · tn 66 | 0.28 → 0.30 | PASS | **dùng** |
| helpful | 100 | 0.375 | 1.00 | 0.30 | tp 9 · fp 0 · fn 21 · tn 70 | 0.09 → 0.30 | FAIL (κ, R) | **loại** |

`tone_ok` chấm **cách nói** (xưng hô, giọng điệu): chỉ cần đọc reply. `helpful` chấm **nội dung** (số tiền, thông tin có đúng không): phải đối chiếu reply với ledger.

## ≥5 case audit thủ công

### tone_ok
| # | Case | Judge nói | Người nói | Ai đúng? | Vì sao | Sửa rubric |
|---|---|---|---|---|---|---|
| 1 | H-008: "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." | PASS | FAIL | Người | Xưng "em" + "nha" quá suồng sã với khách; judge nhầm là thân thiện | Xưng hô bắt buộc "anh/chị" – "LogiX"; xưng "em"/"bạn" hoặc dùng "nha/nhé" ⇒ FAIL |
| 2 | H-017: "Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha." | PASS | FAIL | Người | Gọi khách là "bạn" (khách có thể lớn tuổi), kết câu "nha"; chữ "Dạ" ở đầu không bù được xưng hô sai | Như #1; thêm: một từ lễ phép ("Dạ") không đủ để PASS nếu xưng hô sai |
| 3 | H-029: "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm." | PASS | FAIL | Người | Giọng ra lệnh, gạt khách ("không cần nhắn thêm"); judge chỉ bắt từ khóa "Dạ, vui lòng" | Câu mệnh lệnh / chặn khách liên hệ ⇒ FAIL dù có "Dạ, vui lòng"; judge chấm cả câu, không chấm theo từ khóa |
| 4 | H-042: "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." | FAIL | PASS | Người | Ngắn nhưng lịch sự, đủ ý; LogiX không có lỗi nên không cần xin lỗi. Judge quá khắt khe | Xin lỗi chỉ bắt buộc khi LogiX có lỗi (trễ, hỏng, sai sót); không phạt reply ngắn gọn, đúng mực |
| 5 | H-051: "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." | FAIL | PASS | Người | "refund" là thuật ngữ quy định CS LogiX cho phép; xưng hô, giọng điệu đều đúng. Judge quá khắt khe | Thêm whitelist thuật ngữ được phép ("refund"…); từ trong whitelist không làm FAIL tone |

Mẫu lỗi: #1–#3 judge **dễ dãi** (thấy "Dạ" là cho qua) → nguồn của 6 fn; #4–#5 judge **khắt khe** với điều quy định cho phép → nguồn của 4 fp.

### helpful (minh họa vì sao loại)
| # | Case | Judge nói | Người nói | Ai đúng? | Vì sao | Sửa rubric |
|---|---|---|---|---|---|---|
| 6 | HL-015: "Dạ, LogiX đã hoàn 55.000đ cho đơn O-112 ạ." | PASS | FAIL | Người | Ledger ghi 40.000đ: reply báo sai số tiền (FM-08). Judge chỉ đọc reply, không có ledger | Không sửa được bằng rubric judge: chuyển kiểm tra số tiền sang grader code (reply vs ledger) |
| 7 | HL-020: "Dạ, LogiX đã hoàn 90.000đ cho đơn O-303 ạ." | PASS | FAIL | Người | Ledger ghi 120.000đ: báo thiếu tiền (FM-08) | Như #6 |
| 8 | HL-016: xin lỗi dài + "LogiX đã hoàn 55.000đ cho đơn O-404" + xin lỗi lần nữa | PASS | FAIL | Người | Ledger ghi 35.000đ; văn phong xin lỗi dài kéo judge về "hữu ích" | Như #6; thêm: độ dài / số lời xin lỗi không được tính là hữu ích |

## Kết luận
- **Dùng `tone_ok`**: κ = 0.757, P = 0.857, R = 0.80, qua cả ba sàn. Lỗi còn lại (6 fn, 4 fp) có mẫu rõ và sửa được bằng rubric (xưng hô, giọng ra lệnh, xin lỗi khi không có lỗi, whitelist thuật ngữ).
- **Loại `helpful`**, không dùng làm gate: R = 0.30 (bỏ sót **21/30** lỗi thật, fn = 21), κ = 0.375 < 0.6. P = 1.00 không có ý nghĩa vì judge hầu như không báo lỗi (9/100 FAIL so với 30/100 thật; Rogan-Gladen hiệu chỉnh 0.09 → 0.30). Các case bỏ sót là reply báo **số tiền khác ledger** (FM-08): judge không thấy ledger nên không thể phát hiện, và văn phong xin lỗi dài còn kéo judge về PASS. Kiểm tra này chuyển sang **grader code** so số tiền trong reply với ledger (metric FM-08, M3), đúng quy tắc taxonomy "tiền luôn chấm bằng code".
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật. Rubric tone sau khi sửa phải chấm lại trên bộ nhãn mới, không dùng lại chính 100 dòng đã dùng để sửa.
