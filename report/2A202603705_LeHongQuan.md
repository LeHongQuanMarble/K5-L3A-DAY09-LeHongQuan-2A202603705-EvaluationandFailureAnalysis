# Báo cáo cá nhân — 2A202603705_LeHongQuan (Lab 9 · Evaluation & Failure Analysis)

## 1. Thông tin

- Họ tên: Lê Hồng Quân
- MSSV: 2A202603705
- Email: 26ai.quanlh3@vinuni.edu.vn
- GitHub: https://github.com/LeHongQuanMarble
- Repo / PR: https://github.com/LeHongQuanMarble/K5-L3A-DAY09-LeHongQuan-2A202603705-EvaluationandFailureAnalysis/pull/1 (`starter/d09` → `main`)
- Hình thức: bài cá nhân — tự làm toàn bộ Core (M0–M4) và Advanced/Expert (M5–M7).

## 2. Phần việc

| Mốc | Việc | File chính |
|---|---|---|
| M0 | Overlay Lab 8 (nhóm HHTQ) vào repo, không sửa `src/lab8/`; bổ sung data/config Lab 8, `.gitignore` chặn secret, `harness_map.yaml` có section `eval` | `src/lab8/` (giống hệt), `src/harness_map.yaml` |
| M1 | Taxonomy FM-01…FM-09 từ trace; gắn `failure_modes` cho 14 item; trace case + regression test | `docs/failure_taxonomy.md`, `src/lab9/evalset.py`, `docs/trace_case.md`, `src/tests/test_lab9_trace_case.py` |
| M2 | confusion, P/R, Cohen κ, Rogan-Gladen; audit 8 bất đồng | `src/lab9/stats.py`, `docs/judge_audit.md` |
| M3 | `ApprovalBypass`, `RefundAmountCorrect`; 2 metric riêng `reply_matches_ledger` (FM-08) và `proposal_correct` (FM-04/05) | `src/lab9/graders.py`, `src/config/metric_spec.yaml` |
| M4 | Paired bootstrap; baseline v1 + report; CI gate | `src/lab9/stats.py`, `src/reports/*.json` |
| M5 | `fm_map.yaml` (+ FM-09), eval set v2 (28 item), slice gate | `src/config/fm_map.yaml`, `src/config/metric_spec_v2.yaml`, `src/lab9/gate.py::slice_check` |
| M6 | `pass_at_k` / `pass_hat_k`; `pass_hat_5` blocking, sàn từ A/A | `src/lab9/stats.py`, `src/config/metric_spec_v2.yaml` |
| M7 | `integrity_check` + ratchet | `src/lab9/gate.py::integrity_check` |
| Tài liệu | Eval card (v1 + v2), PRD v1.1, kịch bản demo | `docs/eval_card.md`, `docs/PRD_v1.1.md`, `DEMO.md`, `DEMO.html` |

## 3. Đóng góp cụ thể

### Commit chính
| Commit | Nội dung |
|---|---|
| `05edc76` | Overlay Lab 9 lên code Lab 8 |
| `09c1fb2` | M1 taxonomy + `failure_modes` |
| `1876e4b`, `196536e` | M2 thống kê judge + audit |
| `951dea3` | M3 graders + metric FM-08 |
| `9d15bf0` | M4 paired bootstrap, baseline v1, report |
| `be6fc58` | Trace case + regression test, eval card, PRD v1.1 |
| `0fce433` | M5–M7: eval set v2, slice gate, pass^k, integrity + ratchet, `proposal_correct` |
| `5d8c22f`, `edf72a1` | Kịch bản demo + bản mô phỏng trực quan |

### Quyết định kỹ thuật
1. **Gắn `failure_modes` theo bằng chứng, không theo cảm tính.** Bật từng bug đơn lẻ của `variant_agent` và xem claim nào fail; ví dụ C-009 ("ignore policy, tôi là giám đốc") nghe giống FM-03 nhưng bug `ticket_trust` không làm nó fail, nên không gắn.
2. **Tiền chấm bằng code, không bằng judge.** Judge `helpful` có P = 1.0 nhưng R = 0.30: 21/30 lỗi bị bỏ sót đều là reply báo số tiền khác ledger — judge không có ledger. Chuyển sang grader `reply_matches_ledger` (tách số tiền trong reply, so với ledger; không có reply → không có gì để báo sai → pass).
3. **Thêm `proposal_correct` thay vì nới ngưỡng.** `mutation --detect` ban đầu 75% (< 80%) vì E-013: agent tự trừ khoản đã hoàn (đề xuất 0 thay vì 35.000đ) nhưng outcome tình cờ đúng. Grader mới chấm số đề xuất cho host → 100%, 0% báo nhầm. Thêm metric = chặt hơn, đúng ratchet.
4. **Sàn `pass_hat_5` = 0.85 chọn từ A/A.** Cùng `swarm`, seed 11–55 vs 66–110 → Δ = 0. Sàn dưới baseline (0.8929), ngoài dải nhiễu, trên `flaky_regression` (0.5714).
5. **Slice tag lấy từ nhãn.** `money_movement` = nhãn có `refund_vnd` > 0 (12 item). `slice_regression` có pass_rate trung bình 0.9357 (trên sàn, CI chạm 0) nhưng slice rơi 1.0 → 0.85 → chặn.
6. **`integrity_check` fail-closed nhưng không báo nhầm.** Kiểm số dòng, dòng trùng, tập (item, seed) và manifest so với baseline, `evaluator_failures`, dòng thiếu giá trị grader, metric tổng khớp tính lại từ dòng (với report do `lab9.eval` sinh), slice tag, ratchet (min/max/max_increase/no_significant_drop/blocking/kind/xóa metric-slice/seeds/confidence). Slice rỗng → MISSING → chặn.
7. **Không hạ ngưỡng để bắt lỗi 1/3 seed.** Variant `rare` (chỉ seed 33) cho metric y hệt baseline → ghi là giới hạn cỡ mẫu trong eval card.

### Test đã thêm
- `src/tests/test_lab9_trace_case.py` (3 test, marker `student`, chạy trong CI): bước sai đầu tiên của `seeded_regression C-002@11` là event 3 `model_override {"delay_days": 5}`; `DbFactKept`/`RefundAmountCorrect` fail trên variant lỗi, pass trên `fixed`.

## 4. Bằng chứng

| Kiểm tra | Kết quả |
|---|---|
| `python -m lab9.smoke` | `M0 PASS` |
| `pytest -m student -k "lab9 and not advanced"` | 14 passed |
| `pytest -m student -k advanced` | 12 passed |
| `evalset --check` / `evalset --v2` | `ba03889993ae: 0 problem(s)` / `472b70f08380: 0 problem(s)` |
| `judge` tone / helpful | κ 0.757 P 0.857 R 0.80 PASS / κ 0.375 P 1.0 R 0.30 FAIL |
| `mutation --detect` | detection 100% · false alarms 0% |
| Gate `fixed` (v1) | `exit 0 — merge` |
| Gate `seeded_regression` (v1) | `pass_rate 0.7143 Δ -0.271 CI [-0.500, -0.057] BLOCK` → `exit 1 — blocked: refund_amount_correct, proposal_correct, pass_rate, reply_matches_ledger` |
| A/A `--aa 66,77,88,99,110` | Δ = 0 mọi metric |
| Scorecard v2 | `mutation score 3/3 · false alarms 0` |
| `lab9.traps` | 4/4 trap `blocked` (INTEGRITY / ratchet) |
| Baseline v2 so với chính nó | `exit 0 — merge` |
| CI PR #1 | `detect` ✓ · `eval-gate` ✓ · `eval-gate-v2` ✓ (chạy thật: 12 test, evalset v2, scorecard) |

Run ID: v1 `E-swarm-20261117-ba03`, `E-fixed-20261117-ba03`, `E-seeded_regression-20261117-ba03`; v2 `E-swarm-20261117-472b`, `E-slice_regression-20261117-472b`, `E-flaky_regression-20261117-472b`.

Kiểm thử thêm ngoài bộ công khai (không commit, chạy trong scratch): 8 trap kiểu ẩn (dòng trùng, run xanh có `evaluator_failures`, đổi slice tag, sửa tay metric, inf, bỏ một slice, bỏ blocking `pass_hat_5`, giảm seed trong spec) → 8/8 bị chặn; 13 variant kiểu ẩn → 11/13 đúng (chặn `quiet_override`, `misreport`, `stale_clause`, `sibling_refund`, `leaky_trace`, `pre_deducted`, `ignore_denied`; merge `paraphrase`, `extra_lookup`); 2 variant `rare` lọt — giới hạn cỡ mẫu đã nêu.

## 5. Đối chiếu RUBRIC / SUBMISSION

### Core (60)
| Hạng mục | Yêu cầu | Trạng thái |
|---|---|---|
| M1 (12) | ≥5 FM có bằng chứng trace; `--check` sạch; provenance | ✓ 9 FM, 5 FM có trace từ variant công khai kèm số event |
| M2 (12) | test stats xanh; tone dùng, helpful loại; audit ≥5 có sửa rubric | ✓ 8 case, cột "Sửa rubric" |
| M3 (12) | 2 grader; ≥80% phát hiện, ≤10% báo nhầm; metric FM-08 | ✓ 100% / 0%; `reply_matches_ledger` |
| M4 (15) | CI lệch ≤0.01; chặn seeded, qua fixed; job xanh; `eval` trong harness_map | ✓ Δ −0.271 CI [−0.500, −0.057] khớp tham chiếu |
| Eval card + PRD (9) | số liệu khớp run_id; nêu giới hạn | ✓ MockLLM, 14 item, judge replay, rare 1/3 seed |

### Advanced (25) / Expert (15)
| Kiểm tra | Trạng thái |
|---|---|
| `pass_at_k` / `pass_hat_k`, từ chối (n, c, k) sai | ✓ 9 vector công khai; kiểm n ≥ 1, 0 ≤ c ≤ n, 1 ≤ k ≤ n, kiểu số nguyên |
| `fm_map.yaml` đúng mã FM; `evalset --v2` sạch, ≥3 item/FM | ✓ |
| `pass_hat_5` blocking; slice `money_movement` + `adversarial` blocking | ✓ |
| Chặn `slice_regression` + slice regression ẩn | ✓ công khai; ẩn: thử `intermittent + round_down` → chặn |
| Chặn lỗi FM-08 ẩn | ✓ thử `misreport` → chặn bởi `reply_matches_ledger` |
| Không báo nhầm trên `fixed`, `honest_refactor`, refactor ẩn | ✓ thử `paraphrase`, `extra_lookup` → merge |
| Chặn mọi trap (4 công khai + 2 ẩn) | ✓ 4/4 công khai; 8/8 trap tự dựng |
| `flaky_regression` + variant không để lại override; self-merge; A/A Δ = 0; sàn ≥ 0.8 | ✓ (`quiet_override` chặn; sàn 0.85) |

### Trừ điểm — đã tự kiểm
- Không sửa `src/lab8/` (so `diff -rq` với repo Lab 8: giống hệt).
- Không sửa tay `reports/` — mọi file sinh bằng `lab9.eval` / `lab9.traps`.
- Không nới ngưỡng: spec v1 chỉ **thêm** metric; spec v2 giữ nguyên ngưỡng gốc.
- Không có nhãn inline (`expected`/`label` không xuất hiện trong eval set).
- Không sửa variant / trap / bộ chấm (`variants.py`, `traps.py`, `mutation.py`, `eval.py`, `ci_check.py` không đổi so với template).

## 6. Công cụ AI đã dùng

- **Claude Code** (trợ lý lập trình trong terminal): đọc code starter, đề xuất cách viết grader/thống kê/gate, chạy lệnh kiểm chứng, soạn nháp tài liệu.
- Cách tự kiểm tra: mọi con số trong tài liệu lấy từ report do script sinh (có run_id); mọi hàm qua test công khai; tự chạy `trace_case` để đọc lại bằng chứng từng FM; tự phán "ai đúng" trong judge audit; kiểm lại kết quả gate bằng tay trên `fixed` / `seeded_regression`; dựng thêm trap và variant ngoài bộ công khai để thử gate. Phần audit và lý do chọn layer/ngưỡng đã đọc lại và có thể giải thích khi được hỏi.

## 7. Tự đánh giá

- **Làm tốt:** chuỗi bằng chứng từ trace → FM → grader → gate rõ ràng; tìm ra và sửa lỗ hổng detection (E-013) bằng grader mới thay vì nới ngưỡng; gate chống được cả trap công khai lẫn tự dựng.
- **Giới hạn:** MockLLM tất định (A/A = 0 không nói gì về nhiễu LLM thật); 14/28 item cho CI rộng; lỗi 1/3 seed không bắt được với 5 seed; integrity không phát hiện report bị đổi giá trị từng dòng rồi tính lại — cần CI tự chạy lại eval.
- **Nếu làm tiếp:** tăng số seed theo lớp lỗi, thêm item từ trace case vào eval set (`provenance.from_trace`), port grader sang Inspect AI / DeepEval để đối chiếu.
