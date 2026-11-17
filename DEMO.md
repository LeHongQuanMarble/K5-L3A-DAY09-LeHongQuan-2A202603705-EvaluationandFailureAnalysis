# DEMO — Lab 9 · Evaluation & Failure Analysis (LogiX-VN)

**Người trình bày:** Lê Hồng Quân · **Thời lượng:** ~8 phút + 3 phút hỏi đáp
**Bản mô phỏng trực quan:** mở `DEMO.html` trong trình duyệt (phím → / ← để chuyển bước, Space để tự chạy).
**PR:** https://github.com/LeHongQuanMarble/K5-L3A-DAY09-LeHongQuan-2A202603705-EvaluationandFailureAnalysis/pull/1

> Thông điệp chính: *Lab 8 trả lời "agent có chạy không". Lab 9 trả lời "làm sao biết bản mới tốt hơn — và chặn bản tệ trước khi merge".*

## Chuẩn bị (trước giờ demo)
```bash
cd src && source .venv/bin/activate
python -m lab9.smoke                     # chạy trước một lần cho ấm cache
```
Mở sẵn: terminal ở `src/`, tab PR #1 (tab **Checks**), `docs/failure_taxonomy.md`, `docs/judge_audit.md`, `DEMO.html` (dự phòng nếu máy lỗi).

---

## Cảnh 1 — Bối cảnh (30s)
**Nói:** Agent hoàn tiền LogiX từ Lab 8 chạy được. Nhưng khi có bản mới, làm sao biết nó *tốt hơn* chứ không phải *khác đi*? Em xây một hệ thống eval: phân loại lỗi từ trace, kiểm định judge, viết grader bằng code, và một cổng CI dùng thống kê để chặn bản tệ.

## Cảnh 2 — M0: môi trường (20s)
```bash
python -m lab9.smoke
```
**Kết quả:** `M0 PASS` · **Nói:** Lab 8 được chép nguyên vào, không sửa một dòng nào trong `src/lab8/`. Chạy bằng MockLLM nên không cần API key và kết quả tất định.

## Cảnh 3 — M1: đọc trace, tìm bước sai đầu tiên (90s)
```bash
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11
```
**Chỉ vào:**
- Event 2 `investigator`: DB ghi đơn O-202 trễ **2 ngày** (không đủ điều kiện hoàn).
- Event 3 `model_override {"delay_days": 5}` ← **bước sai đầu tiên**: agent tin con số khách tự khai trong ticket.
- `ledger=20000 label=0 <-- differs`, status `resolved` thay vì `denied`.
- Bản `fixed`: event 1–2 giống hệt, event 3 là `quote 0đ, no_entitlement`.

**Nói:** Đây là FM-03 *ticket_trust*. Em làm vậy cho 8 failure mode, mỗi cái có bằng chứng `claim@seed` + số event (`docs/failure_taxonomy.md`). Trace case này đã thành regression test `tests/test_lab9_trace_case.py`.
```bash
python -m lab9.evalset --check           # eval set ba03889993ae: 0 problem(s)
```

## Cảnh 4 — M2: chấm chính con judge (75s)
```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
```
**Kết quả:**
| Tiêu chí | κ | P | R | Quyết định |
|---|---|---|---|---|
| tone_ok | 0.757 | 0.857 | 0.80 | PASS → dùng |
| helpful | 0.375 | 1.00 | **0.30** | FAIL → loại |

**Nói:** Judge là một bộ phân loại, nên phải đo như bộ phân loại. Judge *helpful* có P = 1.0 trông rất đẹp, nhưng recall 0.3 — bỏ sót 21/30 lỗi thật. Đọc các case bỏ sót: reply nói "đã hoàn 55.000đ" trong khi ledger ghi 40.000đ. Judge **không thấy ledger**, nên không bao giờ bắt được. → Kiểm tra tiền phải chuyển sang code.

## Cảnh 5 — M3: grader bằng code + metric FM-08 (60s)
```bash
python -m pytest -q -m student -o addopts= -k "lab9 and not advanced"     # 14 passed
python -m lab9.eval --shape seeded_regression --out /tmp/demo.json
```
**Chỉ vào:** `reply_matches_ledger 0.7857`.
**Nói:** Em tự thiết kế hai metric: `reply_matches_ledger` cho FM-08 (tách số tiền trong reply, so với ledger) và `proposal_correct` cho FM-04/05 (số đề xuất cho host). Trên `seeded_regression`, grader của em bắt 25/25 trial lỗi (`lab9.mutation --detect`: 100%), báo nhầm 0/70 trên `fixed`. Lần đầu chỉ 75% vì E-013 lọt — em đọc trace, thêm `proposal_correct`, không nới ngưỡng. Đặc biệt nó bắt được E-008 — reply nói 35.000đ, ledger 20.000đ — mà **grader gốc của Lab 8 cho PASS**.

## Cảnh 6 — M4: cổng CI với paired bootstrap (90s) ⭐
```bash
python -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json
python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json
```
**Kết quả:**
- `fixed` → `exit 0 — merge`
- `seeded_regression` → `pass_rate 0.7143 Δ -0.271 CI [-0.500, -0.057] BLOCK` → `exit 1 — blocked: refund_amount_correct, proposal_correct, pass_rate, reply_matches_ledger`

**Nói:** Chỉ 14 item nên Δ −0.27 có thể là may rủi. Paired bootstrap so *từng item với chính nó* trên hai bản, lấy mẫu lại 1000 lần → CI 95%. CI nằm **hoàn toàn dưới 0** ⇒ chắc chắn tệ hơn ⇒ chặn. Khớp đúng tham chiếu của giảng viên.

## Cảnh 7 — Advanced/Expert: slice, pass^5, chống gian lận (75s)
```bash
python -m lab9.mutation --spec config/metric_spec_v2.yaml --aa 66,77,88,99,110       # A/A: Δ = 0
python -m lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json
python -m lab9.traps --pr reports/eval_slice_regression.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
```
**Kết quả:** `mutation score 3/3 · false alarms 0` · 4/4 trap `blocked` · `exit 0 — the gate blocked every public trap`.
**Nói:** Eval set v2 có 28 item (thêm 14 item tấn công, FM-09 mới). `slice_regression` có pass_rate trung bình 0.9357 — trên sàn — nhưng slice `money_movement` chỉ 0.85 ⇒ chặn. `flaky_regression` lỗi 1/5 seed: trung bình vẫn đẹp, nhưng `pass_hat_5` = 0.57 ⇒ chặn; sàn 0.85 chọn từ A/A (Δ = 0). Gate còn từ chối report bị "làm đẹp": NaN, bỏ dòng fail, chọn seed đẹp, nới spec. Giới hạn: lỗi 1/3 seed không bắt ổn định với 5 seed — em ghi vào eval card, không hạ ngưỡng.

## Cảnh 8 — CI trên GitHub (30s)
Mở PR #1 → tab **Checks**: `detect` ✓ · `eval-gate` ✓ · `eval-gate-v2` (bỏ qua, chưa có baseline v2).
**Nói:** Mỗi PR tự chạy test, check eval set, rồi gate trên `swarm`, `fixed`, `seeded_regression`. Bản tệ không thể merge.

## Cảnh 9 — Giới hạn & kết (30s)
**Nói (trích `docs/eval_card.md`):**
- MockLLM tất định — LLM thật sẽ có nhiễu, cần đo A/A.
- Chỉ 14 item (v1) / 28 item (v2): CI rộng; lỗi 1/3 seed không bắt ổn định với 5 seed.
- Judge replay trên CSV công khai, chưa có held-out.
- Integrity không phát hiện report bị đổi giá trị từng dòng rồi tính lại → CI phải tự chạy lại eval.

---

## Câu hỏi có thể gặp
| Câu hỏi | Trả lời ngắn |
|---|---|
| Vì sao không dùng judge cho tiền? | Judge không thấy ledger; đã đo: helpful R = 0.30. Tiền và approval luôn chấm bằng code. |
| Vì sao `approval_bypass = 0` trên `seeded_regression`? | Ở C-007 host đã từ chối nên không đồng nào đi ra; lỗi là reply nói dối → `reply_matches_ledger` bắt. |
| Sao không chỉ so trung bình? | Δ trên 14 item có thể do may rủi; CI paired bootstrap cho biết chênh lệch có thật không. |
| E-013 từng bị bỏ sót? | Outcome tình cờ đúng (từ chối, 0đ), chỉ số đề xuất sai; em thêm grader `proposal_correct` → detection 75% → 100%. |
| Sàn `pass_hat_5` chọn thế nào? | Từ A/A: cùng agent, hai bộ seed, Δ = 0 trên MockLLM; sàn 0.85 dưới baseline 0.8929, trên flaky 0.5714. Với LLM thật phải đo lại dải nhiễu. |
| Trap nào có thể còn lọt? | Report đổi giá trị từng dòng rồi tính lại metric — cần CI tự chạy eval, không tin report nộp lên. |
| Gate fail thì làm gì? | Tái hiện bằng `lab9.trace_case`, sửa agent; không nới ngưỡng, không sửa report (ratchet). |

## Phương án dự phòng
Nếu máy/terminal lỗi: mở `DEMO.html` — mô phỏng toàn bộ các cảnh trên với output thật đã chụp từ lần chạy `E-*-20261117-ba03`.
