# TraceAI — Kịch bản thuyết trình

**Deck:** 15 slide
**Cách dùng file này:** phần chữ thường là lời nói. Phần trong ngoặc vuông là ghi chú thao tác, không đọc.

**Thời lượng:** khoảng **20 phút** nói + hỏi đáp. Nhãn thời lượng ở mỗi phần là số đo thật, không phải ước lượng.

Đây là bản chính, trình bày đủ. Nếu tới hôm đó bị rút ngắn quỹ thời gian, cuối file có mục **"Đường cắt dự phòng"** với sẵn đường về 13 phút và 10 phút — chỉ dùng khi cần.

---

## Mở đầu — Slide 1 · 1 phút

[Đứng ở slide bìa, chưa bấm gì]

Kính chào ban giám khảo.

Tôi muốn bắt đầu bằng một tình huống mà anh chị em kỹ thuật ở đây chắc ai cũng từng gặp.

Một khách hàng gọi lên tổng đài, nói là đặt lệnh không được. Bạn Support nhấc máy. Câu hỏi đầu tiên bạn ấy phải trả lời là: lỗi này của đội nào? Không biết. Câu thứ hai: có bao nhiêu khách đang bị như vậy? Cũng không biết.

Thế là bạn ấy đẩy ticket sang cho dev. Dev mở Sentry, thấy stack trace. Copy trace ID, dán sang Kibana, lọc log. Rồi mở Bitbucket tìm đoạn code. Rồi quay lại đoán xem khách đã bấm gì trước đó.

Bốn hệ thống, bốn tab trình duyệt, và trung bình khoảng hai mươi phút cho mỗi lần như vậy.

[Bấm sang slide 2]

Cái tôi mang tới hôm nay là TraceAI. Nó rút hai mươi phút đó xuống còn ba phút, với chi phí ba mươi hai xu một lần điều tra.

---

## Bài toán — Slide 2 · 1 phút

[Slide 2, sơ đồ luồng thủ công]

Sơ đồ này là quy trình hiện tại, tôi vẽ lại đúng như nó đang diễn ra.

Nhìn từ trái sang phải sẽ thấy vấn đề không nằm ở chỗ nào thiếu công cụ. Chúng ta có đủ cả: Sentry cho lỗi frontend, Kibana và APM cho log backend, Matomo cho hành vi người dùng, Bitbucket cho mã nguồn.

Vấn đề là bốn hệ thống này không nói chuyện với nhau. Người kỹ sư chính là sợi dây nối. Anh ta phải tự copy trace ID từ chỗ này sang chỗ kia, tự nhớ mình đang tìm gì, tự ghép các mảnh lại.

Và có một câu hỏi mà không hệ thống nào trả lời được: bao nhiêu khách hàng đang bị ảnh hưởng? Đó lại đúng là câu Support cần nhất để trả lời khách.

Cho nên đây không phải bài toán thiếu dữ liệu. Đây là bài toán dữ liệu nằm rời rạc.

---

## Giải pháp — Slide 3 · 1 phút 30

[Slide 3]

TraceAI không phải thêm một cái dashboard nữa. Nếu tôi làm dashboard thì tôi chỉ đang tạo ra tab thứ năm cho mọi người mở.

Nó là một agent. Nghĩa là nó tự chọn công cụ, tự quyết định bước tiếp theo dựa trên cái nó vừa đọc được.

Ba điểm tôi muốn nhấn.

Thứ nhất, xuyên tầng. Một trace ID chạy suốt từ lỗi frontend, qua từng service backend mà request đó đi qua, tới hành vi người dùng và dòng code cụ thể. Đây là thứ mà không sản phẩm nào ngoài thị trường làm được, vì không ai có sẵn bốn nguồn dữ liệu nội bộ của mình.

Thứ hai, mọi kết luận đều gắn với bằng chứng. Không có câu nào là suy đoán. Mỗi nhận định đều trỏ về một dòng log thật hoặc một file kèm số dòng. Và nếu thiếu bằng chứng, agent buộc phải nói thẳng là thiếu, chứ không được bịa ra. Cái này tôi ràng buộc bằng schema ở đầu ra chứ không phải nhắc nhở trong prompt.

Thứ ba, khép vòng. Chọn một khuyến nghị, hệ thống tự tạo branch, commit và pull request nháp trên Bitbucket. Phần này tôi nói thật là mới xử lý được các sửa đơn giản, và quyền merge luôn thuộc về con người.

---

## Kiến trúc — Slide 4 · 3 phút 30

[Slide 4. Sơ đồ này có ba lớp xem sẵn, bấm lần lượt theo ba đoạn dưới đây]

Đây là kiến trúc runtime. Tôi sẽ đi theo ba lớp, mỗi lớp trả lời một câu hỏi.

**[Bấm lớp 1 — Analysis request path]**

Câu thứ nhất: một yêu cầu đi qua đâu.

Người dùng vào TraceAI Web, viết bằng React 19. Đăng nhập qua Entra ID, trả về JWT có kèm vai trò. FastAPI nhận request, kiểm vai, rồi đẩy xuống AIAnalyzer.

AIAnalyzer là lõi, dựng trên LangGraph. Vòng lặp của nó là: lập kế hoạch, gọi công cụ, kiểm chứng kết quả, rồi mới sinh báo cáo. Trạng thái từng bước ghi checkpoint xuống PostgreSQL, nên một phân tích đang chạy dở mà process chết thì chạy tiếp được, không phải làm lại từ đầu.

Có hai cái chốt tôi đặt trong vòng lặp này. Một là ngân sách vòng lặp, agent không được gọi công cụ vô hạn. Hai là bước kết luận bắt buộc: khi chạm ngưỡng, hệ thống tắt hết công cụ và ép agent phải chốt bằng cái nó đang có. Đây là cách tôi chặn kiểu agent chạy loạn rồi đốt tiền.

Đầu ra không phải văn xuôi tự do. Nó là JSON được validate bằng Pydantic, có schema cố định, bắt buộc mỗi luận điểm phải kèm nguồn.

**[Bấm lớp 2 — Cross-stack evidence]**

Câu thứ hai: nó lấy bằng chứng ở đâu.

Bốn hệ thống. Kibana cho log và APM span. Sentry cho lỗi frontend. Matomo cho hành vi người dùng. Bitbucket cho mã nguồn, commit và pull request.

Thứ khâu bốn cái này lại là distributed trace ID. Và mắt xích khó nhất là nối frontend với backend, vì hai bên vốn không biết nhau. Chỗ đó tôi đi qua trường additional_data của Sentry, nơi có trace ID mà request đã mang theo. Nối được mắt xích đó thì cả chuỗi mới thông.

Riêng phần mã nguồn thì không phải grep. Tôi dựng code graph bằng tree-sitter, biết hàm nào gọi hàm nào, nên đi từ dòng lỗi ngược lên caller hoặc xuôi xuống callee đều được.

**[Bấm lớp 3 — Privacy boundary]**

Câu thứ ba, và là câu quan trọng nhất với ngân hàng: quyền và dữ liệu.

Agent này không có quyền riêng của nó. Mọi lời gọi tới bốn hệ thống kia đều đi bằng token của chính người đang hỏi. Nếu bạn không được phép đọc log của một service, thì agent chạy cho bạn cũng không đọc được. Không có super-token dùng chung nằm ở đâu cả. Token lưu thì mã hóa AES-256-GCM.

Và mọi đường ra Bedrock đều bị chặn qua PIIMaskingLLM. Không có nhánh nào đi tắt. Phần này tôi nói kỹ hơn ở slide sau.

[Chỉ vào khung bao ngoài của sơ đồ]

Cái khung lớn bao quanh là ranh giới đám mây TCBS. Không có SaaS bên thứ ba nào nhìn thấy log hay mã nguồn của mình. Bedrock cũng nằm trong region, trong tài khoản AWS của mình.

Tôi quyết định mô hình quyền này ngay từ ngày đầu. Nếu làm ngược lại, cho agent một tài khoản riêng cho tiện, thì sau này gỡ ra rất khó.

---

## Một lần điều tra — Slide 5 · 3 phút 15

[Slide 5, sơ đồ sequence]

Slide này trả lời câu hỏi mà tôi đoán ban giám khảo sẽ hỏi: sao rẻ được như vậy?

Câu trả lời là TraceAI lấy log theo thứ tự thu hẹp dần. Bốn bước, mỗi bước đầu vào đã ít hơn bước trước.

**Bước một, tìm log lỗi.** Chỉ lấy mức ERROR và WARN. Trong hàng triệu dòng log một ngày, số dòng thực sự là lỗi chiếm tỉ lệ rất nhỏ. Nên ngay bộ lọc đầu tiên đã cắt đi phần lớn.

**Bước hai, nếu có trace ID thì chỉ tìm theo trace ID đó.** Đây là bước thu hẹp mạnh nhất. Chỉ những dòng log thuộc đúng trace của sự cố mới được lấy, và lấy xuyên suốt tất cả service mà request đó đi qua. Một request, không phải một service.

**Bước ba, tìm log ngữ cảnh theo vị trí trong code.** Từ dòng lỗi, qua stack trace, TraceAI biết lỗi phát sinh ở file nào hàm nào. Rồi mới tìm thêm các log liên quan quanh vị trí đó. Tức là tìm có chủ đích, không phải đọc bừa.

**Bước bốn, tìm log theo khoảng thời gian.** Mở cửa sổ cộng trừ hai phút quanh thời điểm lỗi. Đủ để dựng lại câu chuyện của request, mà không phải kéo cả ngày về.

[Dừng một nhịp]

Kết quả là lượng log thực sự đi vào mô hình cho mỗi lần điều tra chỉ vài chục dòng, nhiều lắm là vài trăm dòng đã lọc. Không phải hàng triệu dòng.

Quy ra token là khoảng ba mươi hai nghìn token đầu vào. Tức là mười tám xu tiền mô hình.

Nếu làm theo kiểu dồn hết log vào rồi bảo mô hình tự tìm, chi phí sẽ gấp mấy chục lần mà kết quả còn tệ hơn, vì mô hình bị nhiễu. Cái khó không phải gọi được LLM. Cái khó là biết đưa cho nó đúng thứ cần đưa.

**Một điều kiện tôi muốn nói thẳng.**

Để cơ chế trace ID chạy tốt nhất, các service phải có tích hợp thư viện sinh và truyền trace ID xuyên suốt, tức là distributed tracing. Khi trace ID giữ được liền mạch qua các service, TraceAI lần theo đúng một luồng request duy nhất. Đó chính là thứ khiến lượng log đưa vào ít mà vẫn đủ để kết luận.

Service nào chưa có trace ID xuyên suốt thì vẫn điều tra được, hệ thống lùi về tìm theo message cộng thời gian cộng tên service. Nhưng độ chính xác và độ gọn sẽ thấp hơn.

Nói cách khác, TraceAI không bắt buộc phải có distributed tracing mới chạy. Nhưng service nào chuẩn hóa được trace ID thì hiệu quả trên service đó cao hơn hẳn. Đây cũng là một lý do để đẩy chuẩn hóa tracing rộng ra, vì giá trị thu về đo được ngay.

---

## Hai chế độ — Slide 6 · 1 phút

[Slide 6]

Một điểm mà tôi thấy các sản phẩm ngoài thị trường bỏ qua: người cần câu trả lời không phải lúc nào cũng là dev.

Nên TraceAI có hai chế độ, phân theo vai trò.

Chế độ Support trả lời bốn câu: đội nào sở hữu lỗi, bao nhiêu khách bị ảnh hưởng, khách đã thao tác gì trước đó, và nên xử lý thế nào. Không cần biết kỹ thuật vẫn đọc hiểu.

Chế độ Dev thì đi tới tận dòng code, kèm bảng bằng chứng, luồng xuyên service và các bước tái hiện.

Quan trọng là hai chế độ này được chặn ở tầng middleware, không phải bằng cách ẩn nút trên giao diện. Support không bao giờ chạm được vào mã nguồn, kể cả có gọi thẳng API.

---

## Tính năng — Slide 7 · 40 giây

[Slide 7, lướt nhanh]

Slide này tôi lướt nhanh, ban giám khảo có thể xem lại sau.

Từ một công cụ phân tích ban đầu, nó đã thành một hệ sinh thái: chat AI hỏi tiếp trên từng kết quả, thông báo qua Teams kèm deep link, monitor lỗi theo thời gian thực, truy vết hiệu năng chứ không chỉ lỗi, và code graph dựng bằng tree-sitter cho bốn ngôn ngữ Java, Python, TypeScript, Go.

Điểm tôi muốn nói là cái này không dừng ở proof of concept. Nó đang chạy thật và đang được dùng thật.

---

## Quyền riêng tư — Slide 8 · 1 phút

[Slide 8, sơ đồ PII masking]

Đây là phần tôi nghĩ ban giám khảo quan tâm nhất, vì chúng ta là công ty chứng khoán.

Mô hình không bao giờ nhìn thấy dữ liệu khách hàng thật.

Mọi lời gọi LLM đi qua một lớp bọc bắt buộc. Trước khi gửi đi, số tài khoản, tên, số điện thoại, email đều bị che. Nhận về thì khôi phục lại. Bảng ánh xạ chỉ nằm trong bộ nhớ tiến trình, không ghi xuống đĩa, không ghi vào log, không đi đâu cả.

Tôi dùng Presidio kết hợp spaCy NER, cộng thêm bộ luật riêng cho các định dạng tài chính Việt Nam mà thư viện có sẵn không nhận ra.

Và toàn bộ chạy trên AWS Bedrock trong chính tài khoản AWS của TCBS. Dữ liệu không rời khỏi ranh giới đám mây của mình.

---

## Quản trị — Slide 9 · 40 giây

[Slide 9]

Bốn ràng buộc để hệ thống này chạy được trong môi trường ngân hàng, tôi nói gọn.

Danh tính thì đăng nhập bằng Entra ID, phân vai ở middleware.

Thông tin đăng nhập thì token riêng từng người, mã hóa AES-256-GCM khi lưu.

Thực thi thì mặc định chỉ đọc. Đường ghi duy nhất là Auto Fix, và phải do người bấm.

Giám sát thì mỗi lần chạy đều có telemetry về thời lượng và số token. Chính telemetry đó là nguồn của mọi con số ở slide tiếp theo.

---

## Kết quả — Slide 10 · 1 phút 30

[Slide 10 — slide quan trọng nhất, nói chậm lại]

Đây là phần con số. Tôi sẽ nói rõ cái nào là đo được và cái nào là ước tính, để ban giám khảo tự đánh giá.

**Cái đo được, không phụ thuộc giả định nào:**

Thời gian mỗi lần chạy, hệ thống tự ghi. Trung bình khoảng ba phút.

Chi phí token, Bedrock trả về theo từng lần gọi. Mười tám xu phần mô hình, cộng hạ tầng chia đều thành ba mươi hai xu trọn gói.

Số lần chạy, khoảng tám trăm một tháng.

**Cái là ước tính:**

Mốc thủ công hai mươi phút. Tôi lấy từ một mẫu các sự cố xử lý tay, không phải thí nghiệm đối chứng. Nếu ban giám khảo cho rằng con số thật khác đi thì kết quả sẽ dịch theo.

Từ đó ra: mỗi lần tiết kiệm mười bảy phút. Tám trăm lần một tháng là hai trăm hai mươi bảy giờ. Chia cho một trăm sáu mươi giờ công một tháng, tương đương một phẩy bốn hai FTE.

Quy ra tiền theo đơn giá hai nghìn đô một FTE tháng, được khoảng hai nghìn tám trăm ba ba đô mỗi tháng.

So với chi phí vận hành thật là hai trăm năm hai đô.

Tỷ lệ hoàn vốn khoảng mười một phẩy hai lần.

---

## Chi phí — Slide 11 · 1 phút 30

[Slide 11]

Bóc tách chi phí.

**Xây dựng, trả một lần:**

Nhân sự hai nghìn hai trăm năm mươi đô. Ba kỹ sư, đơn giá hai nghìn một tháng, nhưng làm bán thời gian ba phần tám. Đây không phải dự án chiếm trọn ba người trong một tháng.

Phần mềm sáu trăm đô, là ba license Kiro Power Plan.

Tổng hai nghìn tám trăm năm mươi đô. Toàn bộ còn lại là stack mã nguồn mở, không mua license nào.

**Vận hành, mỗi tháng:**

Bedrock một trăm bốn tư đô ở mức tám trăm lần phân tích.

Hạ tầng một trăm lẻ tám đô, trong đó sáu mươi mốt là compute.

Tổng hai trăm năm hai đô.

[Chỉ vào thanh trượt bên phải]

Bên phải là công cụ tính. Ban giám khảo có thể kéo số lần điều tra để xem chi phí thay đổi thế nào.

Điểm cần nhìn là hình dạng của đường chi phí. Phần LLM luôn là mười tám xu mỗi lần, ở mọi khối lượng. Không có bậc license, không tính theo ghế. Chỉ hạ tầng cố định là được chia đều, nên càng dùng nhiều thì đơn giá trọn gói càng rẻ.

Và với chi phí xây hai nghìn tám trăm năm mươi đô, so với giá trị tiết kiệm hai nghìn tám trăm ba ba một tháng, thì hoàn vốn trong tháng đầu.

---

## So sánh thị trường — Slide 12, 13 · 2 phút

[Slide 12, bảng so sánh]

Câu hỏi hợp lý là: sao không đi mua?

Tôi đã tra giá niêm yết công khai của ba sản phẩm gần nhất.

Elastic AI Assistant nằm sẵn trong Kibana mình đã trả tiền. Nhưng nó chỉ thấy dữ liệu trong Elastic. Không thấy Sentry, không thấy Matomo, không đọc mã nguồn.

Datadog Bits AI SRE, tính theo AI Credits. Cùng tám trăm lần điều tra là khoảng năm nghìn hai trăm đô một tháng. Và cũng chỉ trong phạm vi telemetry của Datadog.

Sentry Seer thì đọc code và mở được autofix PR, nhưng không đi xuyên nhiều service backend.

Còn cách làm phổ biến nhất hiện nay là dán log vào chatbot. Rẻ nhất về license, nhưng rủi ro PII cao nhất, và vẫn tốn giờ người.

[Chỉ vào cột TraceAI]

Không ai trong số này đi từ hành vi khách hàng tới dòng code. Vì để làm được thì phải có sẵn bốn nguồn dữ liệu nội bộ nối với nhau bằng trace ID. Đó là thứ không bán ngoài thị trường.

[Bấm sang slide 13]

Slide này quy hết về cùng một khối lượng, tám trăm lần điều tra một tháng, để so cho công bằng.

Điều tôi muốn ban giám khảo nhìn không phải con số tuyệt đối, mà là hình dạng của nó. TraceAI tăng theo số lần dùng. Tất cả phần còn lại tăng theo số ghế đăng ký. Đội càng đông thì khoảng cách càng giãn ra.

Và có một ràng buộc cứng nữa: dữ liệu khách hàng không được rời khỏi ranh giới đám mây của mình. Riêng điều đó đã loại phần lớn phương án mua.

---

## Mở rộng và lộ trình — Slide 14 · 1 phút

[Slide 14]

Về khả năng mở rộng, điểm tôi muốn nhấn là thêm một đội chỉ là cấp quyền, không phải dựng hạ tầng. Đội mới được gán vai, tự nhập token của mình, xong.

Code graph thiết kế cho khoảng năm trăm repository và một triệu hàm, có cache hai tầng nên chi phí mỗi truy vấn không phụ thuộc tổng số repo.

[Cuộn xuống phần dưới slide 14]

Bốn hướng tiếp theo.

Phân tích chủ động: cảnh báo tự kích hoạt phân tích trước khi có người kịp hỏi.

Trí nhớ sự cố: RAG trên kho báo cáo cũ, lỗi lặp lại được trả lời ngay từ lần điều tra trước.

Test hồi quy: biến các bước tái hiện thành test chạy được, đính kèm luôn trong PR.

Bản tin ưu tiên: tổng hợp hằng ngày, chấm điểm theo mức ảnh hưởng.

---

## Kết — Slide 15 · 1 phút

[Slide 15]

Tôi xin tóm lại bằng ba ý.

Một, cái này đã chạy thật. Số liệu vận hành lấy từ database production, không phải mô phỏng. Phần quy đổi ra tiền là ước tính, và tôi đã nói rõ giả định đứng sau nó.

Hai, nó an toàn theo thiết kế chứ không phải theo quy trình. Quyền của chính người dùng, PII che trước mô hình, con người giữ quyền merge. Ba thứ đó nằm trong code, không phải trong tài liệu.

Ba, nó mở rộng được ngay. Thêm một đội là cấp quyền. Thêm một nguồn dữ liệu là thêm một tool vào registry.

Ba phút, ba mươi hai xu, và một bằng chứng luôn chỉ đúng dòng code.

Tôi xin hết. Rất mong nhận được câu hỏi từ ban giám khảo.

---

# Phần chuẩn bị hỏi đáp

## Câu chắc chắn sẽ bị hỏi

**"Làm sao biết mốc hai mươi phút là đúng?"**

Đây là ước tính từ mẫu sự cố xử lý tay, tôi không giấu điều đó. Nhưng ROI vẫn dương rất rộng. Kể cả nếu mốc thật chỉ là tám phút, tức là chỉ tiết kiệm năm phút mỗi lần, thì vẫn ra khoảng sáu mươi bảy giờ một tháng, giá trị tám trăm ba tám đô, ROI vẫn trên ba lần. Mốc thủ công phải rơi xuống khoảng bốn phút rưỡi thì mới hòa vốn — mà bốn phút rưỡi thì gần bằng đúng thời gian máy chạy, tức là gần như không còn gì để tiết kiệm.

**"Nếu AI trả lời sai thì sao?"**

Ba lớp chặn. Đầu ra ràng buộc schema và bắt buộc kèm mức độ tin cậy. Mọi nhận định phải trỏ về bằng chứng thật, thiếu bằng chứng thì phải khai là thiếu. Và có nút phản hồi tốt xấu trên từng phân tích để đo tỷ lệ chính xác thật.

Quan trọng hơn: hệ thống không tự sửa production. Auto Fix chỉ mở PR nháp, người review và merge.

**"Chi phí có tăng vọt khi dùng nhiều không?"**

Không. Phần LLM tuyến tính, mười tám xu mỗi lần, không đổi ở mọi khối lượng. Hạ tầng là chi phí cố định. Nên càng dùng nhiều thì đơn giá trọn gói càng giảm. Ban giám khảo có thể kéo thử thanh trượt ở slide 11.

**"Ai đang dùng, dùng bao nhiêu?"**

Khoảng tám trăm lượt phân tích một tháng. Con số này lấy từ module thống kê trong sản phẩm, không phải ước lượng.

**"Sao không dùng Elastic AI Assistant cho rẻ?"**

Về license thì đúng là rẻ hơn vì gói Elastic mình đã trả. Nhưng token LLM qua connector vẫn phải trả riêng. Và giới hạn thật nằm ở phạm vi: nó không thấy Sentry, không thấy Matomo, không đọc mã nguồn. Nghĩa là nó trả lời được câu "log nói gì" nhưng không trả lời được câu "bao nhiêu khách bị ảnh hưởng và code sai ở dòng nào".

**"Ba kỹ sư bán thời gian trong bao lâu?"**

Ba phần tám thời gian, quy đổi ra là khoảng một tháng công cho cả nhóm. Chi phí nhân sự hai nghìn hai trăm năm mươi đô.

**"Rủi ro lộ dữ liệu khách hàng?"**

PII được che bắt buộc trước mọi lời gọi LLM, không có đường vòng. Bảng ánh xạ chỉ tồn tại trong RAM. Mô hình chạy trên Bedrock trong tài khoản AWS của TCBS, dữ liệu không ra khỏi ranh giới đám mây. Và agent chạy bằng token của người hỏi nên không đọc được nhiều hơn người đó được phép đọc.

**"Hệ thống có phụ thuộc vào việc service phải có distributed tracing không?"**

Có phụ thuộc, nhưng không phải điều kiện bắt buộc.

Khi service có trace ID xuyên suốt, TraceAI lần theo đúng một luồng request duy nhất. Đó là lý do lượng log đưa vào mô hình ít mà vẫn đủ kết luận.

Service chưa có thì hệ thống lùi về tìm theo message, thời gian và tên service. Vẫn ra kết quả, nhưng độ chính xác và độ gọn thấp hơn, và chi phí mỗi lần cao hơn vì phải đọc nhiều log hơn.

Nên tôi nhìn nó theo hướng ngược lại: đây là một lý do cụ thể để đẩy chuẩn hóa tracing rộng ra. Service nào chuẩn hóa xong thì giá trị thu về đo được ngay trên chính service đó.

**"Sao chọn LangGraph mà không tự viết vòng lặp?"**

Cái tôi cần ở framework chỉ có hai thứ: quản lý trạng thái theo bước, và checkpoint để phục hồi. LangGraph cho sẵn cả hai. Tự viết thì cũng ra, nhưng mất thêm thời gian mà không tạo thêm giá trị nào cho bài toán này. Phần logic riêng của TraceAI nằm ở tool registry và ở chiến lược thu hẹp, không nằm ở vòng lặp.

**"Nếu agent chạy loạn, gọi công cụ mãi không dừng thì sao?"**

Có hai chốt. Ngân sách vòng lặp giới hạn số lần gọi công cụ. Và khi chạm ngưỡng thì có bước kết luận bắt buộc: hệ thống tắt hết công cụ, agent buộc phải chốt bằng dữ liệu đang có, hoặc khai là chưa đủ bằng chứng. Nên chi phí mỗi lần chạy có trần, không có trường hợp một request đốt hết ngân sách tháng.

**"Nếu người xây nghỉ việc thì sao?"**

Stack là công nghệ phổ thông: Python, FastAPI, PostgreSQL, React. Không có framework tự chế. Kiến trúc tool registry nên thêm nguồn dữ liệu là thêm một file, không phải đọc hiểu toàn hệ thống.

---

# Ghi chú cho người trình bày

**Nhịp độ**

Ba slide cần chậm và rõ: slide 8 về PII, slide 10 về kết quả, slide 12 về so sánh. Đây là ba chỗ ban giám khảo sẽ cân nhắc nhất.

Ba slide có thể lướt: slide 7 tính năng, slide 9 quản trị, slide 14 mở rộng và lộ trình.

---

# Đường cắt dự phòng

Chỉ dùng khi bị rút quỹ thời gian tại chỗ. Mặc định là trình bày bản đầy đủ 20 phút ở trên.

Cắt theo đúng thứ tự dưới đây.

## Bản 13 phút

| Cắt gì | Tiết kiệm |
|---|---|
| Slide 4: bỏ lớp 1 và lớp 2, chỉ nói lớp 3 | 2 phút |
| Slide 5: bỏ phần điều kiện distributed tracing, đẩy sang Q&A | 1 phút |
| Slide 7 (tính năng): bỏ hẳn | 40 giây |
| Slide 9 (quản trị): bỏ hẳn, nội dung đã nằm trong slide 4 và 8 | 40 giây |
| Slide 12–13: bỏ đoạn nói từng đối thủ, chỉ nói dòng kết | 45 giây |
| Slide 14: bỏ phần mở rộng, chỉ đọc 4 hướng roadmap | 30 giây |

Câu thay cho lớp 1 và 2 của slide 4: *"Lõi là một vòng lặp agent trên LangGraph, có ngân sách vòng lặp và bước kết luận bắt buộc. Nó lấy bằng chứng từ bốn hệ thống, khâu lại bằng trace ID."*

Câu thay cho đoạn đối thủ ở slide 12: *"Ba sản phẩm gần nhất, cái rẻ nhất thì không thấy Sentry, Matomo và mã nguồn, cái thấy nhiều nhất thì năm nghìn hai một tháng. Không ai đi từ hành vi khách hàng tới dòng code."*

## Bản 10 phút

Cắt tiếp từ bản 13 phút:

| Cắt thêm | Tiết kiệm |
|---|---|
| Slide 5: gộp bước 3 và bước 4 thành một câu | 30 giây |
| Slide 3: bỏ điểm thứ ba (khép vòng), nói ở slide 7 hoặc bỏ | 30 giây |
| Slide 2: rút còn hai câu, vì slide 1 đã kể câu chuyện rồi | 30 giây |
| Slide 6 (hai chế độ): rút còn ba câu | 30 giây |

Câu gộp bước 3 và 4 của slide 5: *"Rồi thu hẹp tiếp theo vị trí trong code qua stack trace, và theo cửa sổ cộng trừ hai phút quanh thời điểm lỗi."*

## Không bao giờ cắt

Slide 1 (con số mở), slide 8 (PII), slide 10 (kết quả), slide 11 (chi phí), và lớp 3 của slide 4 (quyền và ranh giới dữ liệu).

Đây là năm chỗ quyết định điểm. Mọi thứ khác đều có thể co lại.

---

# Ghi chú thêm

**Nếu bị hỏi cắt ngang giữa chừng**

Trả lời ngắn rồi quay lại mạch. Nếu câu hỏi rơi đúng vào slide sắp tới thì nói: "Câu này em có một slide riêng, xin phép trả lời ở phần sau ạ."

**Thái độ với con số**

Chủ động nói cái nào là ước tính trước khi bị hỏi. Ban giám khảo tin người tự vạch ra giới hạn của mình hơn người trình bày toàn số đẹp.

Đừng nói "tiết kiệm được rất nhiều". Nói "hai trăm hai mươi bảy giờ, dựa trên giả định mốc thủ công hai mươi phút".

**Ba câu phải nói bằng được, dù có bị cắt thời gian thế nào**

1. Hai mươi phút xuống ba phút, ba mươi hai xu một lần.
2. Mô hình không bao giờ thấy dữ liệu khách hàng thật.
3. Hoàn vốn trong tháng đầu, ROI mười một phẩy hai lần.
