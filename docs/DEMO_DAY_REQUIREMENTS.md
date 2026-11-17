# Yêu cầu nộp bài Demo Day (AI20K)

Nguồn: https://portal-cohort5.edufun.ai/technical-book/chapter-13 (Chương 13: Nộp bài Demo Day).
Trọng số từng tiêu chí có thể đổi theo cohort. Bản BTC phát hành là chuẩn cuối cùng, hãy đối chiếu lại với BTC.

## 1. Bằng chứng từ cohort 1

- Video demo: thiếu ở 11/11 đội (100%).
- Evaluation evidence: thiếu ~82% đội.
- Pitch deck: thiếu ~64% đội.
- Điểm mất chủ yếu vì thiếu deliverables và demo không chuẩn bị, không phải vì AI kém.

## 2. 10 deliverables (đủ 10/10 = điểm tối đa ở tiêu chí hoàn thành)

| # | Deliverable | Yêu cầu chính | Vị trí trong repo |
|---|---|---|---|
| 1 | Source code | GitHub public hoặc add BTC làm collaborator; không secrets; không file >10MB; pin version; type hints; docstrings; ≥1 file pytest | `src/` |
| 2 | README.md | Tên, mô tả, screenshot/GIF, cài đặt, cách chạy, cấu trúc thư mục, tech stack, tên env vars, API docs, team, Live URL | `README.md` |
| 3 | Architecture diagram | Mermaid/draw.io/Excalidraw; PNG/SVG; đủ Frontend, Backend, Agent, DB, External API; có mũi tên data flow | `docs/architecture.md` |
| 4 | AI logs | LangSmith URL public hoặc screenshot; 5-10 trace (input, LLM call, retrieval, output) | README hoặc docs |
| 5 | Live URL | HTTP 200, có `/health`, ghi trong README, sống đến Demo Day + 7 ngày (UptimeRobot nếu free tier) | README |
| 6 | Video demo | 3-5 phút HD, YouTube unlisted; giới thiệu team, use case chính, edge case, architecture; có phụ đề | `docs/video-demo.md` (link) |
| 7 | Pitch deck | 10 slide, định dạng PDF (không PPTX) | `docs/pitch-deck.pdf` |
| 8 | Development journal | ≥5-7 entry, mỗi entry 2-3 câu | `docs/journal.md` |
| 9 | Worklog | `git log --oneline --since="..." > docs/worklog.md` | `docs/worklog.md` |
| 10 | Evaluation evidence | Bảng pytest + coverage; metrics golden dataset (pass@k / pass^k, RAGAS nếu có RAG); benchmark; feedback 3-5 người thật; map test → feature | `docs/evaluation.md` |

Bonus DevOps: `.github/workflows/`, `Dockerfile`, `docker-compose.yml`.

## 3. 6 tiêu chí chấm

Thang điểm: 9-10 Giỏi, 7-8 Khá, 5-6 Trung bình, 3-4 Yếu, 1-2 Kém.

1. **Mức độ hoàn thiện (Demo)**
   - 10-15 edge case, mỗi case có test trong `tests/`.
   - Ẩn tính năng chưa xong, không treo "SOON" trên tính năng cốt lõi.
   - CI smoke-test demo account sau mỗi deploy.
   - E2E (Playwright) trong `tests/e2e/`.
2. **Kỹ thuật AI**
   - Guardrail tối thiểu 2 lớp (prompt + code, ví dụ Pydantic schema-lock, banned pattern) kèm test jailbreak.
   - RAG thì đo bằng RAGAS.
   - Graph có conditional edge thật (LangSmith trace thấy 2 path).
   - Chống hallucination bằng citation/grounding.
3. **Đánh giá hiệu quả (Evaluation)**
   - Golden dataset ≥30 câu on-topic + 15 off-topic từ người dùng thật (`eval/datasets/golden.jsonl`).
   - Đo pass@k VÀ pass^k; LLM-judge khác model generator; kết quả ở `eval/results/`.
   - Benchmark so baseline người hoặc đối thủ (bảng 3 cột).
   - Before/after: đo vòng 1 tuần 4, sửa, đo lại tuần 6 trên cùng dataset.
4. **Giao diện & UX**
   - Loading state cho mọi LLM call, lỗi thân thiện (không hiện raw exception).
   - Test mobile thật; không render reasoning token ra chat.
   - Có route `/privacy` thật nếu chạm dữ liệu cá nhân.
5. **Ý tưởng & ứng dụng thực tế**
   - Khảo sát 3 đối thủ, phỏng vấn ≥5 user thật.
   - Con số/messaging đồng nhất ở mọi nơi.
   - USP chạy end-to-end và demo trong video.
6. **Thuyết trình (Pitch)**
   - Kể chuyện theo AIDA (`presentation/demo_script.md`).
   - Backup 3 tầng: live → video → screenshot.
   - Tổng duyệt trước BGK đúng 1 tuần; tập 3 lần + chuẩn bị Q&A; ghi hình lần tập cuối.

**Chiến lược:** đạt Khá (7-8) ở cả 6 tiêu chí trước, rồi đẩy 2-3 tiêu chí lên Giỏi. Đội 7-7-7-7-7-7 thắng đội 10-10-4-4-4-4. "Quỹ điểm thừa" lớn nhất là Evaluation và Pitch/video.

## 4. Nghệ thuật demo

- **AIDA (3-5 phút):**
  - Attention (15s): không mở bằng "Xin chào, chúng tôi là đội...".
  - Interest (30s): dùng số liệu phỏng vấn thật.
  - Desire (2 phút): click từng bước `[CLICK] → [màn hình] → [lời nói]`.
  - Action (15s): link rút gọn + QR.
- **Showcase Mode:** dữ liệu giả realistic, không PII; demo account (`demo@yourapp.com`) đã đăng nhập sẵn; link/QR trỏ thẳng vào trạng thái showcase, không signup; tắt notifications; test OAuth từ hôm trước. QR để nguyên trong suốt Q&A, gắn UTM.
- **Backup 3 tầng:** (1) live, (2) video quay sẵn (chính là deliverable #6, lưu file local), (3) screenshot step-by-step có annotation.
- **Khi sự cố:** nói thẳng → chuyển backup → tiếp tục. Không hoảng, không im lặng, không xin lỗi nhiều lần.
- **Thời gian:** 70% story + value, 30% technical + Q&A.
- **Q&A cần chuẩn bị:** scale 1000 users, vì sao chọn tech này (LangGraph vs CrewAI/AutoGen), roadmap, hallucination, cost/request. Phân công ai trả lời câu nào.
- **Checklist 1 ngày trước:**
  - Deploy stable, không push code mới sáng hôm sau.
  - Seed lại dummy data, test full flow lần cuối, không có console error.
  - Video lưu local, có screenshots, slide backup, link rút gọn đã test.

## 5. Lộ trình 6 tuần

| Tuần | Việc |
|---|---|
| 1 | Clone template, deploy `/health`, mở checklist 10 deliverables, viết README bản đầu |
| 2 | **Proposal** (problem, user, USP); khảo sát 3 đối thủ + phỏng vấn 5 user; bắt đầu golden dataset |
| 3 | Build tính năng chính, CI/CD xanh, draft 10 slide thô, journal hằng ngày |
| 4 | **Midway demo nội bộ** (AIDA); eval vòng 1 (baseline "before"); phân công người quay video |
| 5 | **Tổng duyệt trước BGK** (đúng 1 tuần trước); quay video backup + screenshots; chỉnh deck |
| 6 | Demo Day: seed showcase, pre-login, tắt notifications, tập lần 3 + Q&A |

Ba mốc không được trễ: proposal (tuần 2), midway demo (tuần 4), tổng duyệt (tuần 5).

## 6. Lỗi phổ biến cần tránh

1. Không có CI/CD (`.github/workflows/ci.yml` chạy pytest).
2. Không có test (coverage 0%).
3. Bare `except` / silent fallback: phải bắt exception cụ thể, log, rồi raise.
4. Hardcoded secrets: dùng env vars và `.gitignore` cho `.env`.
5. Thiếu Evaluation Evidence.

## 7. Pitch deck (10 slide, mỗi slide ~1 phút)

1. Title
2. Problem
3. Solution
4. Product demo
5. Architecture
6. AI/LLM approach (+ eval metrics)
7. Technical highlights (CI/CD, coverage, guardrails)
8. Demo video / QR
9. Challenges & learnings
10. Team & next steps + Q&A + QR

Quy tắc slide: mỗi slide 1 ý, font ≥24pt, ≤30 từ, nền tối chữ sáng, hình hơn chữ, 1 người nói chính, nộp dạng PDF.

## 8. Bài tập cuối chương

**Bài 9.1:** viết `presentation/demo_script.md` là script demo 3 phút theo AIDA (cũng là kịch bản quay video). Chấm chéo: cho đội khác đọc script khi không nhìn màn hình; hiểu được câu chuyện là đạt.

## 9. Checklist cuối trước khi nộp

- [ ] 10/10 deliverables hoàn thành
- [ ] README có screenshot, install guide, API docs
- [ ] Live URL chạy (thử trình duyệt khác + incognito)
- [ ] pytest xanh
- [ ] Không có hardcoded secrets
- [ ] Không có bare except / silent fallback
- [ ] Docker build thành công
- [ ] CI/CD xanh
- [ ] Git history đều đặn (không phải 5 commit ngày cuối)
- [ ] Pitch deck đã tập ≥3 lần
- [ ] Video demo đã quay (backup tầng 2)
- [ ] Showcase Mode đã seed, demo account pre-login
- [ ] Đã tổng duyệt trước BGK đủ 1 tuần
