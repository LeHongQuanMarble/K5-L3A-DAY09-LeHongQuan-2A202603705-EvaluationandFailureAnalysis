# Bonus — port grader sang Inspect AI và so khớp

**Mục tiêu (RUBRIC, bonus +5):** port grader sang Inspect AI và so khớp kết quả với harness chính (pydantic-evals).

```bash
cd src
pip install -r requirements-bonus.txt          # inspect-ai==0.3.290
python -m bonus.inspect_port                    # v1: swarm, fixed, seeded_regression
python -m bonus.inspect_port --spec config/metric_spec_v2.yaml \
    --shapes swarm,honest_refactor,slice_regression,flaky_regression --out reports/bonus_inspect_compare_v2.json
python -m pytest -q -o addopts= tests/test_bonus_inspect.py
```

## Port những gì

4 grader code của nhóm được **viết lại độc lập** thành `@scorer` của Inspect (`src/bonus/inspect_port.py`) — không import `lab9.graders`, để so khớp thực sự là hai cài đặt kiểm tra lẫn nhau:

| Grader (lab9 / pydantic-evals) | Scorer Inspect | Đọc gì |
|---|---|---|
| `ApprovalBypass` | `approval_bypass` | ledger `refund_count` + nhãn `approval_ok`; `unexpected_rows` |
| `RefundAmountCorrect` | `refund_amount_correct` | ledger `refund_vnd` vs nhãn |
| `ReplyMatchesLedger` (FM-08) | `reply_matches_ledger` | `state.output.completion` (reply) vs ledger |
| `ProposalCorrect` (FM-04/05) | `proposal_correct` | `proposal_amount` vs nhãn |

Ánh xạ khái niệm:

| pydantic-evals (lab9) | Inspect AI |
|---|---|
| `Dataset` / `Case(name="E-001@11")` | `Task(dataset=[Sample(id="E-001@11")])` |
| `expected_output` = nhãn | `Sample.target` = nhãn (JSON) |
| task `run_one` trả Trial | `@solver run_shape` chạy shape, lưu Trial vào `state.store`, reply vào `state.output.completion` |
| `Evaluator.evaluate(ctx)` → `EvaluationReason` | `@scorer` → `Score(value, explanation)` |
| `dataset.evaluate_sync(max_concurrency=1)` | `inspect_eval(task, model="mockllm/model", max_samples=1)` |

Không cần API key: solver không gọi model; Inspect dùng model có sẵn `mockllm/model`. Agent vẫn là shape Lab 8 với MockLLM, cùng seed, nên trial giống hệt.

## Kết quả so khớp (từng (item, seed))

| Eval set | Shape | approval_bypass | refund_amount_correct | reply_matches_ledger | proposal_correct | Khớp |
|---|---|---|---|---|---|---|
| v1 | swarm | 0 / 0 | 0.9857 / 0.9857 | 1.0 / 1.0 | 0.9857 / 0.9857 | 280/280 |
| v1 | fixed | 0 / 0 | 1.0 / 1.0 | 1.0 / 1.0 | 1.0 / 1.0 | 280/280 |
| v1 | seeded_regression | 0 / 0 | 0.8571 / 0.8571 | 0.7857 / 0.7857 | 0.7857 / 0.7857 | 280/280 |
| v2 | swarm | 0 / 0 | 0.9786 / 0.9786 | 1.0 / 1.0 | 0.9786 / 0.9786 | 560/560 |
| v2 | honest_refactor | 0 / 0 | 1.0 / 1.0 | 1.0 / 1.0 | 1.0 / 1.0 | 560/560 |
| v2 | slice_regression | 0 / 0 | 0.9357 / 0.9357 | 1.0 / 1.0 | 0.9357 / 0.9357 | 560/560 |
| v2 | flaky_regression | 0 / 0 | 0.9643 / 0.9643 | 1.0 / 1.0 | 0.9143 / 0.9143 | 560/560 |
| v1 (seed 11) | `sibling_refund` (test) | **4 / 4** | 0.7143 / 0.7143 | 1.0 / 1.0 | 1.0 / 1.0 | 56/56 |

Ô = pydantic-evals / Inspect. **Tổng: 3.136 điểm chấm, 0 bất đồng.** File: `src/reports/bonus_inspect_compare.json`, `src/reports/bonus_inspect_compare_v2.json`.

Hàng cuối là `tests/test_bonus_inspect.py`: không variant công khai nào làm `approval_bypass` bật, nên test dựng shape một-bug `sibling_refund` (FM-07) để kiểm cả **nhánh vi phạm** — cả hai bên cùng đếm 4 lần ghi tiền dưới claim khác.

## Nhận xét

- Khớp 100% vì grader là code tất định đọc cùng một Trial; giá trị của port là **kiểm tra chéo cách đọc Trial** (ví dụ: reply lấy từ event cuối, "không có reply ⇒ pass", số tiền "35.000đ" → 35000) — hai cài đặt độc lập ra cùng kết quả trên 3.136 điểm chấm.
- Inspect cho thêm log có cấu trúc mở được bằng `inspect view --log-dir src/reports/inspect_logs` (từng sample, score, explanation) — hữu ích khi review trace lỗi; log không commit (nặng, tái tạo được).
- Giới hạn: chỉ port grader code; judge `tone_ok` vẫn là replay CSV, chưa port sang `model_graded_qa` của Inspect vì không có API key / model thật.
