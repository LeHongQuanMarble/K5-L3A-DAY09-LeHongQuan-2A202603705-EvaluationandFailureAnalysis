# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

## Case: `seeded_regression C-002@11` — FM-03 ticket_trust

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, trial run `R-seeded_regression-C-002-s11`; nằm trong report `E-seeded_regression-20261117-ba03` (item E-002, fail cả 5 seed) |
| Triệu chứng | Lab 8 grader FAIL (`status resolved != denied`); `refund_amount_correct` FAIL (ledger 20000 vs label 0); `db_fact_kept` FAIL (1 override event). Reply "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202." khớp ledger (20000) — reply **không** nói dối, nhưng cả hai đều sai so với nhãn `denied`, 0đ |
| Bước sai đầu tiên | **Event 3** `model_override` · `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 `handoff` (task `check_applicable_policy`, `allowed_tools` đúng) và event 2 `investigator` (`lookup_order` O-202: `delay_days: 2`, `shipping_fee_vnd: 20000`) giống hệt trace của `fixed`. Event 3 là chỗ đầu tiên lệch: agent thay `delay_days` = 2 của DB bằng 5 lấy từ ticket "Đơn giao trễ 5 ngày". Event 4 `quote` (20000, `SHIP-LATE-03`) chỉ là hệ quả: công cụ tính đúng trên dữ kiện đã bị sửa |
| Failure mode | **FM-03** ticket_trust (layer model/prompt) — `docs/failure_taxonomy.md` |
| Đối chứng | `fixed C-002@11` (`R-fixed-C-002-s11`): event 1–2 giống hệt; event 3 là `quote {"amount_vnd": 0, "reason": "no_entitlement"}` (trễ 2 ngày không đủ điều kiện), event 4 reply "chưa đủ điều kiện hoàn"; status `denied`, ledger 0, Lab 8 grader PASS |
| Regression test | `src/tests/test_lab9_trace_case.py` (marker `student`, chạy trong CI): (1) `test_first_wrong_step_is_model_override` — event 3 là `model_override {"delay_days": 5}`, `fixed` không có event này; (2) `test_graders_catch_buggy_variant` — `DbFactKept` và `RefundAmountCorrect` = False trên `seeded_regression`; (3) `test_graders_pass_fixed` — cả hai = True trên `fixed`. Đã chạy: **3 passed** (fail-on-bug / pass-on-fixed đã xác nhận) |
| Chưa chắc chắn | Trace chỉ ghi *kết quả* override, không ghi *vì sao* model chọn tin ticket (prompt, thứ tự ưu tiên nguồn) — với MockLLM lỗi là công tắc `ticket_trust`, với LLM thật cần log prompt để xác định nguyên nhân. Shape `swarm` gốc cũng dính FM-03 nhưng chỉ ở seed 55 (`seed % 5 == 0`): 1/5 seed, nên với 5 seed chỉ thấy đúng một lần |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
