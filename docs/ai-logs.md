# AI Logs (Deliverable #4)

Nhật ký chạy agent: mỗi trace cho thấy input (claim) → handoff/tool/model event → output → ledger so với nhãn.
Repo này dùng MockLLM nên không có LangSmith; trace do harness của Lab 8/9 ghi.
Tái tạo: `cd src && python -m lab9.ai_logs > ../docs/ai-logs.md`.

### Trace 1: `fixed` C-001@11

- Lab 8 grader: **PASS** (ok)
- Result status: `resolved` (label: `resolved`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-001", "request_id": "REQ-C-001"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-107", "status": "delivered_late", "delay_days": 4, "shipping_fee_vnd": 35000, "paid_` |
| 3 | `quote` | `{"amount_vnd": 35000, "reason": "entitled", "clause_ids": ["SHIP-LATE-03"], "parts": {"SHIP-LATE-03": 35000}}` |
| 4 | `reply` | `{"text": "Dạ, LogiX đã hoàn 35.000đ cho đơn O-107."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 35000 | 35000 |
| `refund_count` | 1 | 1 |

### Trace 2: `fixed` C-002@11

- Lab 8 grader: **PASS** (ok)
- Result status: `denied` (label: `denied`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-002", "request_id": "REQ-C-002"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-202", "status": "delivered", "delay_days": 2, "shipping_fee_vnd": 20000, "paid_vnd":` |
| 3 | `quote` | `{"amount_vnd": 0, "reason": "no_entitlement", "clause_ids": [], "parts": {}}` |
| 4 | `reply` | `{"text": "Dạ, đơn O-202 chưa đủ điều kiện hoàn theo chính sách hiện hành."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 0 | 0 |
| `refund_count` | 0 | 0 |

### Trace 3: `fixed` C-003@11

- Lab 8 grader: **PASS** (ok)
- Result status: `resolved` (label: `resolved`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-003", "request_id": "REQ-C-003"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-303", "status": "delivered", "delay_days": 0, "shipping_fee_vnd": 15000, "paid_vnd":` |
| 3 | `quote` | `{"amount_vnd": 150000, "reason": "entitled", "clause_ids": ["DMG-04"], "parts": {"DMG-04": 150000}}` |
| 4 | `reply` | `{"text": "Dạ, LogiX đã hoàn 150.000đ cho đơn O-303."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 150000 | 150000 |
| `refund_count` | 1 | 1 |

### Trace 4: `fixed` C-004@11

- Lab 8 grader: **PASS** (ok)
- Result status: `needs_info` (label: `needs_info`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `decision` | `{"status": "needs_info"}` |
| 2 | `reply` | `{"text": "Dạ, anh/chị vui lòng cho LogiX xin mã đơn hàng để kiểm tra ạ."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 0 | 0 |
| `refund_count` | 0 | 0 |

### Trace 5: `fixed` C-005@11

- Lab 8 grader: **PASS** (ok)
- Result status: `escalated` (label: `escalated`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-005", "request_id": "REQ-C-005"` |
| 2 | `investigator` | `{"lookup_order": {"visible": false, "reason": "outside_principal_scope", "order_id": "O-110"}, "policy_count": 1}` |
| 3 | `reply` | `{"text": "Dạ, yêu cầu đã được chuyển cho chuyên viên xử lý."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 0 | 0 |
| `refund_count` | 0 | 0 |

### Trace 6: `seeded_regression` C-002@11

- Lab 8 grader: **FAIL** (status resolved != denied)
- Result status: `resolved` (label: `denied`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-002", "request_id": "REQ-C-002"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-202", "status": "delivered", "delay_days": 2, "shipping_fee_vnd": 20000, "paid_vnd":` |
| 3 | `model_override` | `{"delay_days": 5}` |
| 4 | `quote` | `{"amount_vnd": 20000, "reason": "entitled", "clause_ids": ["SHIP-LATE-03"], "parts": {"SHIP-LATE-03": 20000}}` |
| 5 | `refund_history` | `{"refund_count": 0, "refunded_vnd": 0}` |
| 6 | `reply` | `{"text": "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 20000 | 0 ⚠️ differs |
| `refund_count` | 1 | 0 ⚠️ differs |

### Trace 7: `flaky_regression` C-001@11

- Lab 8 grader: **PASS** (ok)
- Result status: `resolved` (label: `resolved`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-001", "request_id": "REQ-C-001"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-107", "status": "delivered_late", "delay_days": 4, "shipping_fee_vnd": 35000, "paid_` |
| 3 | `quote` | `{"amount_vnd": 35000, "reason": "entitled", "clause_ids": ["SHIP-LATE-03"], "parts": {"SHIP-LATE-03": 35000}}` |
| 4 | `reply` | `{"text": "Dạ, LogiX đã hoàn 35.000đ cho đơn O-107."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 35000 | 35000 |
| `refund_count` | 1 | 1 |

### Trace 8: `slice_regression` C-003@11

- Lab 8 grader: **PASS** (ok)
- Result status: `resolved` (label: `resolved`)

| Step | Kind | Payload |
|---|---|---|
| 1 | `handoff` | `{"principal_scope": "owner_order_only", "task": "check_applicable_policy", "max_output_tokens": 400, "facts": {}, "claim_id": "C-003", "request_id": "REQ-C-003"` |
| 2 | `investigator` | `{"lookup_order": {"visible": true, "reason": "ok", "order": {"order_id": "O-303", "status": "delivered", "delay_days": 0, "shipping_fee_vnd": 15000, "paid_vnd":` |
| 3 | `quote` | `{"amount_vnd": 150000, "reason": "entitled", "clause_ids": ["DMG-04"], "parts": {"DMG-04": 150000}}` |
| 4 | `reply` | `{"text": "Dạ, LogiX đã hoàn 150.000đ cho đơn O-303."}` |

| Ledger | Actual | Label |
|---|---|---|
| `refund_vnd` | 150000 | 150000 |
| `refund_count` | 1 | 1 |

