# Checklist kiểm tra chất lượng Demo Day (dành cho người và agent)

Yêu cầu gốc: `docs/DEMO_DAY_REQUIREMENTS.md`. File này là bản **kiểm tra được**: mỗi mục phải có bằng chứng
(lệnh chạy, đường dẫn file, hoặc link). Không có bằng chứng thì ghi `[ ]`, không đoán `[x]`.

## Cách dùng

1. Chạy các lệnh "Kiểm tra nhanh" bên dưới, dán kết quả vào báo cáo.
2. Duyệt từng mục; đánh `[x]` chỉ khi đã tự mở file/chạy lệnh trong lượt này.
3. Báo cáo cuối: liệt kê mục còn thiếu theo thứ tự ưu tiên (Video, Evaluation, Pitch Deck trước).
4. Không sửa số liệu, không bịa metrics, link, hay feedback người dùng để checklist "xanh".

## Kiểm tra nhanh (chạy từ gốc repo)

```bash
# 1. Deliverables có mặt?
for f in README.md docs/architecture.md docs/video-demo.md docs/pitch-deck.pdf \
         docs/journal.md docs/worklog.md docs/evaluation.md presentation/demo_script.md; do
  [ -s "$f" ] && echo "OK   $f" || echo "MISS $f"
done

# 2. Secrets bị commit?
git ls-files | grep -E '(^|/)\.env$' && echo "CÓ .env TRONG GIT"
git grep -nE '(sk-[A-Za-z0-9_-]{16,}|api[_-]?key\s*=\s*["'\''][^"'\'']+["'\''])' -- . ':!docs' || echo "no hardcoded keys"

# 3. File lớn >10MB?
git ls-files -z | xargs -0 du -k 2>/dev/null | awk '$1>10240{print "BIG", $2}'

# 4. Bare except / silent fallback?
git grep -nE '^\s*except\s*:|except Exception:\s*(pass|return)' -- 'src' 'tests' || echo "no bare except"

# 5. Test + CI + Docker?
ls tests .github/workflows Dockerfile docker-compose.yml 2>&1 | head -20
python -m pytest -q 2>&1 | tail -15

# 6. Lịch sử commit đều đặn?
git log --format='%ad' --date=short | sort | uniq -c
```

## A. 10 deliverables

- [ ] 1. Source code: repo push được, `.gitignore` đúng, deps pin version, có type hints + docstrings, ≥1 file test
- [ ] 2. README: tên, mô tả, screenshot/GIF, cài đặt, cách chạy, cấu trúc thư mục, tech stack, tên env vars (không giá trị), API docs, team, Live URL
- [ ] 3. Architecture diagram: đủ Frontend/Backend/Agent/DB/External API + mũi tên data flow, PNG/SVG hoặc Mermaid, có mô tả ngắn
- [ ] 4. AI logs: LangSmith URL hoặc screenshot, 5-10 trace có input, LLM call, retrieval, output
- [ ] 5. Live URL: HTTP 200 (`curl -sI <url>`), `/health` OK, ghi trong README, không sleep
- [ ] 6. Video demo: 3-5 phút, YouTube unlisted, link trong `docs/video-demo.md`, có team intro + use case chính + edge case
- [ ] 7. Pitch deck: đúng 10 slide, **PDF** tại `docs/pitch-deck.pdf`, đã tập ≥3 lần
- [ ] 8. Journal: ≥5-7 entry, mỗi entry 2-3 câu, lưu `docs/journal.md`
- [ ] 9. Worklog: `docs/worklog.md` từ `git log`, khớp lịch sử thật
- [ ] 10. Evaluation evidence: `docs/evaluation.md` có đủ các mục ở phần B3

## B. 6 tiêu chí chấm (mục tiêu: tất cả ≥ Khá 7-8, đẩy 2-3 lên Giỏi 9-10)

### B1. Mức độ hoàn thiện (Demo)
- [ ] 10-15 edge case, mỗi case có test đặt tên tương ứng trong `tests/`
- [ ] Không có tính năng treo "SOON"/placeholder chết trên luồng cốt lõi
- [ ] CI smoke-test demo account sau deploy; log GitHub Actions xanh
- [ ] E2E (Playwright) cho luồng quan trọng nhất

### B2. Kỹ thuật AI
- [ ] Guardrail ≥2 lớp (prompt + code như Pydantic schema-lock/banned pattern), có test jailbreak
- [ ] RAG (nếu có): có bảng RAGAS trong `docs/evaluation.md`
- [ ] Graph có conditional edge thật; trace chứng minh ≥2 path
- [ ] Chống hallucination bằng citation/grounding, có screenshot kiểm chứng được

### B3. Đánh giá hiệu quả (Evaluation)
- [ ] Golden dataset ≥30 câu on-topic + 15 off-topic từ người dùng thật
- [ ] Đo cả pass@k và pass^k
- [ ] LLM-judge dùng model **khác** generator
- [ ] Benchmark so baseline người hoặc đối thủ (bảng 3 cột)
- [ ] Before/after trên cùng dataset (vòng 1 tuần 4 → vòng 2 tuần 6)
- [ ] Feedback ≥3-5 người thật
- [ ] Bảng map test case → feature (traceability)
- [ ] Mọi con số trong `docs/evaluation.md` tái tạo được từ file kết quả trong repo

### B4. Giao diện & UX
- [ ] Loading state cho mọi LLM call, lỗi thân thiện (không lộ raw exception); có screenshot 3 trạng thái
- [ ] Responsive, đã test mobile thật; có screenshot mobile + desktop
- [ ] Không render reasoning token ra bong bóng chat
- [ ] Route `/privacy` thật nếu có dữ liệu cá nhân

### B5. Ý tưởng & ứng dụng thực tế
- [ ] Bảng 3 đối thủ trực tiếp + lý do không dùng giải pháp có sẵn
- [ ] Phỏng vấn ≥5 user thật, có file phỏng vấn + thống kê câu hỏi
- [ ] Một con số/messaging dùng đồng nhất ở README, deck, demo, video
- [ ] USP chạy end-to-end từ UI công khai và xuất hiện trong video

### B6. Thuyết trình (Pitch)
- [ ] `presentation/demo_script.md` theo AIDA (A 15s / I 30s / D 2 phút / A 15s), mở đầu không phải "Xin chào, chúng tôi là đội..."
- [ ] Backup 3 tầng: live → video local → screenshot annotated
- [ ] Đã tổng duyệt trước BGK ≥1 tuần trước sự kiện, đã fix feedback
- [ ] Đã tập 3 lần + có Q&A prep (scale, chọn tech, roadmap, hallucination, cost/request)

## C. Chất lượng kỹ thuật chung

- [ ] Không có secrets trong code hoặc git history
- [ ] Không bare `except`, không silent fallback (bắt exception cụ thể + log)
- [ ] `pytest` xanh; CI xanh; `docker build` thành công
- [ ] Commit message rõ ràng (`feat:`/`fix:`/`test:`), lịch sử đều đặn
- [ ] Code chia module rõ, không dồn vào 1-2 file

## D. Ngày Demo Day (1 ngày trước)

- [ ] Deploy bản stable, không push code mới sáng hôm sau
- [ ] Seed lại dummy data (không PII), demo account pre-login, tắt notifications
- [ ] Chạy full flow lần cuối, không có console error
- [ ] Video lưu local; screenshots, slide backup, link rút gọn/QR đã test

## E. Báo cáo kết quả kiểm tra (mẫu)

```
Ngày kiểm tra: ...
Deliverables: x/10 (thiếu: ...)
Tiêu chí: B1 .. B2 .. B3 .. B4 .. B5 .. B6 .. (Khá/Giỏi/Thiếu bằng chứng)
Lệnh đã chạy + kết quả: ...
Việc cần làm trước, theo ưu tiên: 1) ... 2) ... 3) ...
```
