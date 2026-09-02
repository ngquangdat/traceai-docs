# TraceAI — deck thuyết trình

Bài trình bày sản phẩm TraceAI, đóng gói thành **một file HTML tự chứa**: mở
`traceai-slides.html` bằng trình duyệt là chạy, không cần server và không gọi mạng.

## Nội dung

| Đường dẫn | Là gì |
|---|---|
| `traceai-slides.html` | Bản dựng sẵn — 15 slide, song ngữ Việt/Anh |
| `src/` | Nguồn của deck (`deck_*.html`) và script dựng |
| `diagrams/*.json` | Nguồn sơ đồ, viết theo JSON IR của Archify |
| `diagrams/*.html` | Sơ đồ đã render, được nhúng vào deck lúc build |

## Điều khiển khi trình bày

`←` `→` hoặc `Space` chuyển slide · `O` mở mục lục · `V` đổi Việt/Anh · `Esc` thoát.
Nút **VI | EN** đổi ngôn ngữ toàn bộ; **Xem đầy đủ** trên slide sơ đồ mở bản
Archify đầy đủ có PATH, LENS và guided views.

## Dựng lại

Sửa sơ đồ thì sửa file JSON trong `diagrams/` rồi render lại bằng Archify:

```bash
node ~/.claude/skills/archify/bin/archify.mjs deliver architecture \
  diagrams/architecture.json diagrams/architecture.html --quality showcase
```

Sửa nội dung slide thì sửa `src/deck_*.html`. Sau đó dựng lại deck:

```bash
python3 src/build.py
```

Script gzip từng sơ đồ, mã hoá base64 và nhúng vào `traceai-slides.html`;
lúc chạy, deck giải nén rồi đưa vào iframe qua `srcdoc`.

`diagrams/workflow.*` là sơ đồ Auto Fix, hiện không nằm trong deck nhưng vẫn giữ lại.
