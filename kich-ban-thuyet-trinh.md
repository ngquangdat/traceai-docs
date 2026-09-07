# TraceAI — Kịch bản thuyết trình

**Deck:** 15 slide
**Cách dùng file này:** phần chữ thường là lời nói. Phần trong ngoặc vuông là ghi chú thao tác, không đọc.

**Thời lượng:** khoảng **17 phút** nói + hỏi đáp. Nhãn ở mỗi phần là số đo thật, không phải ước lượng.

**Đối tượng:** hội đồng cấp cao — CEO, HĐQT, Chairman. Bài này đã được cân theo đối tượng đó:

| Nhóm nội dung | Thời lượng | Tỉ lệ |
|---|---|---|
| Tiền (kết quả, chi phí, so sánh) | 4,7 phút | 27% |
| Câu chuyện (bài toán, giải pháp) | 4,6 | 27% |
| Cơ chế kỹ thuật | 3,5 | 21% |
| Rủi ro và kiểm soát | 2,5 | 14% |
| Chiến lược | 1,9 | 11% |

**Mục tiêu:** báo cáo kết quả. Không xin phê duyệt, không xin ngân sách. Nếu hội đồng hỏi "vậy anh muốn gì" thì trả lời thẳng: hôm nay em báo cáo để hội đồng nắm hiện trạng, chưa đề xuất gì.

**Ba nguyên tắc khi nói với hội đồng này:**

1. Không đọc tên công nghệ. Nói "mô hình AI" chứ không nói tên mô hình; nói "bản đồ mã nguồn" chứ không nói tên thư viện. Chi tiết kỹ thuật nằm ở **Phụ lục kỹ thuật** cuối file, chỉ rút ra khi bị hỏi.
2. Mọi con số phải đi kèm việc nó là đo được hay ước tính. Hội đồng tin người tự vạch giới hạn hơn người trình bày toàn số đẹp.
3. Khi bí, quay về ba thứ họ quan tâm: tiền, rủi ro, và ai chịu trách nhiệm.

---

## Mở đầu — Slide 1 · 1 phút

[Đứng ở slide bìa, chưa bấm gì]

Kính chào ban giám khảo.

Em muốn bắt đầu bằng một tình huống mà anh chị em kỹ thuật ở đây chắc ai cũng từng gặp.

Một khách hàng gọi lên tổng đài, nói là đặt lệnh không được. Bạn Support nhấc máy. Câu hỏi đầu tiên bạn ấy phải trả lời là: lỗi này của đội nào? Không biết. Câu thứ hai: có bao nhiêu khách đang bị như vậy? Cũng không biết.

Thế là bạn ấy đẩy ticket sang cho dev. Dev mở Sentry, thấy thông báo lỗi. Chép mã truy vết, dán sang Kibana, lọc log. Rồi mở Bitbucket tìm đoạn code. Rồi quay lại đoán xem khách đã bấm gì trước đó.

Bốn hệ thống, bốn tab trình duyệt, và trung bình khoảng sáu mươi phút cho mỗi lần như vậy.

[Bấm sang slide 2]

Cái em mang tới hôm nay là TraceAI. Nó rút một tiếng đó xuống còn ba phút, với chi phí ba mươi hai xu một lần điều tra.

---

## Bài toán — Slide 2 · 1 phút

[Slide 2, sơ đồ luồng thủ công]

Sơ đồ này là quy trình hiện tại, em vẽ lại đúng như nó đang diễn ra.

Nhìn từ trái sang phải sẽ thấy vấn đề không nằm ở chỗ nào thiếu công cụ. Chúng ta có đủ cả: Sentry cho lỗi frontend, Kibana và APM cho log backend, Matomo cho hành vi người dùng, Bitbucket cho mã nguồn.

Vấn đề là bốn hệ thống này không nói chuyện với nhau. Người kỹ sư chính là sợi dây nối. Anh ta phải tự chép mã truy vết từ chỗ này sang chỗ kia, tự nhớ mình đang tìm gì, tự ghép các mảnh lại.

Và có một câu hỏi mà không hệ thống nào trả lời được: bao nhiêu khách hàng đang bị ảnh hưởng? Đó lại đúng là câu Support cần nhất để trả lời khách.

Cho nên đây không phải bài toán thiếu dữ liệu. Đây là bài toán dữ liệu nằm rời rạc.

---

## Giải pháp — Slide 3 · 1 phút 30

[Slide 3]

TraceAI không phải thêm một cái dashboard nữa. Nếu em làm dashboard thì em chỉ đang tạo ra tab thứ năm cho mọi người mở.

Nó là một agent. Nghĩa là nó tự chọn công cụ, tự quyết định bước tiếp theo dựa trên cái nó vừa đọc được.

Ba điểm em muốn nhấn.

Thứ nhất, xuyên tầng. Một mã truy vết chạy suốt từ lỗi trên màn hình khách hàng, qua từng hệ thống backend mà yêu cầu đó đi qua, tới hành vi người dùng và dòng code cụ thể. Đây là thứ mà không sản phẩm nào ngoài thị trường làm được, vì không ai có sẵn bốn nguồn dữ liệu nội bộ của mình.

Thứ hai, mọi kết luận đều gắn với bằng chứng. Không có câu nào là suy đoán. Mỗi nhận định đều trỏ về một dòng log thật hoặc một file kèm số dòng. Và nếu thiếu bằng chứng, agent buộc phải nói thẳng là thiếu, chứ không được bịa ra. Cái này em ràng buộc bằng chính cấu trúc đầu ra của hệ thống, chứ không phải bằng cách dặn dò mô hình.

Thứ ba, khép vòng. Chọn một khuyến nghị, hệ thống tự soạn sẵn một bản sửa nháp trên kho mã nguồn. Phần này em nói thật là mới xử lý được các sửa đơn giản, và quyền merge luôn thuộc về con người.

---

## Kiến trúc — Slide 4 · 1 phút 15

[Slide 4]

Sơ đồ này là kiến trúc hệ thống. Em sẽ không đi vào từng hộp, chỉ nói ba điều em nghĩ hội đồng cần nghe.

**Thứ nhất, hệ thống không có quyền riêng của nó.** Mọi lời gọi tới bốn nguồn dữ liệu đều đi bằng quyền của chính người đang hỏi. Nếu một bạn Support không được phép đọc dữ liệu của một mảng nào đó, thì hệ thống chạy cho bạn ấy cũng không đọc được. Không có tài khoản quyền cao dùng chung nằm ở đâu cả.

**Thứ hai, dữ liệu không rời khỏi nhà.**

[Chỉ vào khung bao ngoài của sơ đồ]

Cái khung lớn này là ranh giới đám mây của TCBS. Mô hình AI chạy trong chính tài khoản AWS của mình. Không có nhà cung cấp bên ngoài nào nhìn thấy log hay mã nguồn của chúng ta.

**Thứ ba, hệ thống có phanh.** Nó không được phép chạy vô hạn. Có giới hạn số bước, và khi chạm ngưỡng thì buộc phải kết luận bằng dữ liệu đang có. Nên chi phí mỗi lần chạy luôn có trần — không có chuyện một yêu cầu đốt hết ngân sách tháng.

Phần còn lại của sơ đồ là cách các thành phần nói chuyện với nhau. Nếu hội đồng muốn đi sâu, em có phần chi tiết để trả lời riêng.

---

## Một lần điều tra — Slide 5 · 1 phút 15

[Slide 5]

Slide này trả lời một câu mà em nghĩ thế nào cũng có người hỏi: ba mươi hai xu một lần điều tra, có thật không, hay là có cắt xén gì đó.

Câu trả lời nằm ở chỗ hệ thống không đọc bừa.

Mỗi ngày hệ thống của mình sinh ra hàng triệu dòng log. Nếu đưa hết cho AI đọc thì vừa đắt vừa sai, vì nó bị nhiễu. TraceAI làm ngược lại: nó thu hẹp dần qua bốn bước lọc, mỗi bước nhỏ hơn bước trước, để cuối cùng chỉ còn vài chục tới vài trăm dòng thực sự liên quan tới đúng sự cố đó.

[Chỉ vào sơ đồ]

Sơ đồ này là bốn bước đó. Điểm cần nhìn không phải từng bước, mà là hình dạng của nó: một cái phễu hẹp dần.

Kết quả là mỗi lần điều tra chỉ tốn mười tám xu tiền mô hình, cộng hạ tầng chia đều thành ba mươi hai xu trọn gói.

Nói gọn lại: cái khó không phải gọi được AI, ai cũng gọi được. Cái khó là biết đưa cho nó đúng thứ cần đưa. Đó là phần chúng em bỏ công nhiều nhất, và cũng là phần làm nên khoảng cách chi phí ở slide sau.

---

## Hai chế độ — Slide 6 · 1 phút

[Slide 6]

Một điểm mà em thấy các sản phẩm ngoài thị trường bỏ qua: người cần câu trả lời không phải lúc nào cũng là dev.

Nên TraceAI có hai chế độ, phân theo vai trò.

Chế độ Support trả lời bốn câu: đội nào sở hữu lỗi, bao nhiêu khách bị ảnh hưởng, khách đã thao tác gì trước đó, và nên xử lý thế nào. Không cần biết kỹ thuật vẫn đọc hiểu.

Chế độ Dev thì đi tới tận dòng code, kèm bảng bằng chứng, luồng xuyên service và các bước tái hiện.

Quan trọng là hai chế độ này được chặn ở tầng hệ thống, không phải bằng cách ẩn nút trên giao diện. Support không bao giờ chạm được vào mã nguồn, kể cả khi cố tình đi đường vòng.

---

## Tính năng — Slide 7 · 40 giây

[Slide 7, lướt nhanh]

Slide này em lướt nhanh, ban giám khảo có thể xem lại sau.

Từ một công cụ phân tích ban đầu, nó đã thành một hệ sinh thái: hỏi tiếp bằng chat ngay trên từng kết quả, tự báo qua Teams khi phân tích xong, theo dõi lỗi theo thời gian thực, đo cả độ chậm chứ không chỉ lỗi, và bản đồ mã nguồn phủ bốn ngôn ngữ chính mà công ty đang dùng.

Điểm em muốn nói là cái này không dừng ở mức thử nghiệm. Nó đang chạy thật và đang được dùng thật.

---

## Quyền riêng tư — Slide 8 · 1 phút 40

[Slide 8, sơ đồ PII masking]

Đây là phần em nghĩ ban giám khảo quan tâm nhất, vì chúng ta là công ty chứng khoán.

Mô hình không bao giờ nhìn thấy dữ liệu khách hàng thật.

Mọi lời gọi tới mô hình AI đều đi qua một lớp chặn bắt buộc. Trước khi gửi đi, số tài khoản, tên, số điện thoại, email đều bị che. Nhận về thì khôi phục lại. Bảng ánh xạ chỉ nằm trong bộ nhớ tiến trình, không ghi xuống đĩa, không ghi vào log, không đi đâu cả.

Bộ nhận diện này em không dùng mặc định của thư viện. Các định dạng tài chính Việt Nam — số tiểu khoản, mã hợp đồng — thư viện quốc tế không nhận ra, nên em viết thêm luật riêng cho chúng.

Và toàn bộ mô hình chạy trong chính tài khoản AWS của TCBS. Dữ liệu khách hàng không rời khỏi ranh giới đám mây của mình, kể cả dữ liệu đã che.

[Dừng một nhịp]

Em muốn nói rõ vì sao chỗ này quan trọng. Cách làm phổ biến hiện nay khi gặp lỗi khó là copy log dán vào một chatbot công cộng. Việc đó đang diễn ra, ở khắp nơi, và không ai kiểm soát được. TraceAI thay thế đúng hành vi đó bằng một đường đi có kiểm soát: che dữ liệu trước, chạy trong nhà, ghi lại ai hỏi gì.

Nói cách khác, đây không chỉ là thêm một công cụ. Nó đóng lại một lỗ hổng vốn đã có.

---

## Quản trị — Slide 9 · 40 giây

[Slide 9]

Bốn ràng buộc để hệ thống này chạy được trong môi trường ngân hàng, em nói gọn.

Danh tính thì đăng nhập bằng tài khoản nội bộ của tổ chức, phân vai ngay ở tầng hệ thống chứ không phải ẩn nút trên giao diện.

Thông tin đăng nhập thì mỗi người một bộ riêng, mã hóa khi lưu trữ. Không có tài khoản dùng chung.

Thực thi thì mặc định chỉ đọc. Đường ghi duy nhất là Auto Fix, và phải do người bấm.

Giám sát thì mỗi lần chạy đều được hệ thống tự ghi lại thời lượng và khối lượng xử lý. Chính nhật ký đó là nguồn của mọi con số ở slide tiếp theo.

---

## Kết quả — Slide 10 · 1 phút 30

[Slide 10 — slide quan trọng nhất, nói chậm lại]

Đây là phần con số. Em sẽ nói rõ cái nào là đo được và cái nào là ước tính, để ban giám khảo tự đánh giá.

**Cái đo được, không phụ thuộc giả định nào:**

Thời gian mỗi lần chạy, hệ thống tự ghi. Trung bình khoảng ba phút.

Chi phí xử lý, nhà cung cấp trả về theo từng lần gọi. Mười tám xu phần mô hình, cộng hạ tầng chia đều thành ba mươi hai xu trọn gói.

Số lần chạy, khoảng tám trăm một tháng.

**Cái là ước tính:**

Mốc thủ công sáu mươi phút. Em lấy từ một mẫu các sự cố xử lý tay, không phải thí nghiệm đối chứng. Nếu ban giám khảo cho rằng con số thật khác đi thì kết quả sẽ dịch theo.

Từ đó ra: mỗi lần tiết kiệm năm mươi bảy phút. Tám trăm lần một tháng là bảy trăm sáu mươi giờ. Chia cho một trăm sáu mươi giờ công một tháng, tương đương bốn phẩy bảy lăm FTE.

Quy ra tiền theo đơn giá hai nghìn đô một FTE tháng, được khoảng chín nghìn năm trăm đô mỗi tháng.

So với chi phí vận hành thật là hai trăm năm hai đô.

Tỷ lệ hoàn vốn khoảng ba mươi tám lần.

---

## Chi phí — Slide 11 · 1 phút 30

[Slide 11]

Bóc tách chi phí.

**Xây dựng, trả một lần:**

Nhân sự hai nghìn hai trăm năm mươi đô. Ba kỹ sư, đơn giá hai nghìn một tháng, nhưng làm bán thời gian ba phần tám. Đây không phải dự án chiếm trọn ba người trong một tháng.

Phần mềm sáu trăm đô, là ba tài khoản công cụ hỗ trợ lập trình.

Tổng hai nghìn tám trăm năm mươi đô. Toàn bộ phần còn lại dùng phần mềm mã nguồn mở, không mua bản quyền nào.

**Vận hành, mỗi tháng:**

Mô hình AI một trăm bốn tư đô, ở mức tám trăm lần phân tích.

Hạ tầng một trăm lẻ tám đô, trong đó sáu mươi mốt là compute.

Tổng hai trăm năm hai đô.

[Chỉ vào thanh trượt bên phải]

Bên phải là công cụ tính. Ban giám khảo có thể kéo số lần điều tra để xem chi phí thay đổi thế nào.

Điểm cần nhìn là hình dạng của đường chi phí. Phần mô hình luôn là mười tám xu mỗi lần, ở mọi khối lượng. Không có bậc bản quyền, không tính theo số người dùng. Chỉ hạ tầng cố định là được chia đều, nên càng dùng nhiều thì đơn giá trọn gói càng rẻ.

Và với chi phí xây hai nghìn tám trăm năm mươi đô, so với giá trị tiết kiệm chín nghìn năm trăm một tháng, thì hoàn vốn trong chín ngày đầu vận hành.

---

## So sánh thị trường — Slide 12, 13 · 2 phút

[Slide 12, bảng so sánh]

Câu hỏi hợp lý là: sao không đi mua?

Em đã tra giá niêm yết công khai của ba sản phẩm gần nhất.

Elastic AI Assistant nằm sẵn trong Kibana mình đã trả tiền. Nhưng nó chỉ thấy dữ liệu trong Elastic. Không thấy Sentry, không thấy Matomo, không đọc mã nguồn.

Datadog Bits AI SRE, tính theo AI Credits. Cùng tám trăm lần điều tra là khoảng năm nghìn hai trăm đô một tháng. Và cũng chỉ trong phạm vi telemetry của Datadog.

Sentry Seer thì đọc code và mở được autofix PR, nhưng không đi xuyên nhiều service backend.

Còn cách làm phổ biến nhất hiện nay là dán log vào chatbot. Rẻ nhất về tiền bản quyền, nhưng rủi ro lộ dữ liệu khách hàng là cao nhất, và vẫn tốn giờ người.

[Chỉ vào cột TraceAI]

Không ai trong số này đi từ hành vi khách hàng tới dòng code. Vì để làm được thì phải có sẵn bốn nguồn dữ liệu nội bộ nối với nhau bằng một mã truy vết chung. Đó là thứ không bán ngoài thị trường.

[Bấm sang slide 13]

Slide này quy hết về cùng một khối lượng, tám trăm lần điều tra một tháng, để so cho công bằng.

Điều em muốn ban giám khảo nhìn không phải con số tuyệt đối, mà là hình dạng của nó. TraceAI tăng theo số lần dùng. Tất cả phần còn lại tăng theo số ghế đăng ký. Đội càng đông thì khoảng cách càng giãn ra.

Và có một ràng buộc cứng nữa: dữ liệu khách hàng không được rời khỏi ranh giới đám mây của mình. Riêng điều đó đã loại phần lớn phương án mua.

---

## Mở rộng và lộ trình — Slide 14 · 1 phút

[Slide 14]

Về khả năng mở rộng, điểm em muốn nhấn là thêm một đội chỉ là cấp quyền, không phải dựng hạ tầng. Đội mới được gán vai, tự nhập thông tin đăng nhập của mình, xong.

Bản đồ mã nguồn thiết kế cho khoảng năm trăm kho mã và một triệu hàm, và được thiết kế sao cho càng nhiều kho thì chi phí mỗi lần tra cứu vẫn không tăng.

[Cuộn xuống phần dưới slide 14]

Bốn hướng tiếp theo.

Phân tích chủ động: cảnh báo tự kích hoạt phân tích trước khi có người kịp hỏi.

Trí nhớ sự cố: RAG trên kho báo cáo cũ, lỗi lặp lại được trả lời ngay từ lần điều tra trước.

Test hồi quy: biến các bước tái hiện thành test chạy được, đính kèm luôn trong PR.

Bản tin ưu tiên: tổng hợp hằng ngày, chấm điểm theo mức ảnh hưởng.

---

## Kết — Slide 15 · 1 phút

[Slide 15]

Em xin tóm lại bằng ba ý.

Một, cái này đã chạy thật. Số liệu vận hành lấy từ database production, không phải mô phỏng. Phần quy đổi ra tiền là ước tính, và em đã nói rõ giả định đứng sau nó.

Hai, nó an toàn theo thiết kế chứ không phải theo quy trình. Quyền của chính người dùng, PII che trước mô hình, con người giữ quyền merge. Ba thứ đó nằm trong code, không phải trong tài liệu.

Ba, nó mở rộng được ngay. Thêm một đội là cấp quyền. Thêm một nguồn dữ liệu là thêm một tool vào registry.

Ba phút, ba mươi hai xu, và một bằng chứng luôn chỉ đúng dòng code.

Em xin hết. Rất mong nhận được câu hỏi từ ban giám khảo.

---

# Phần chuẩn bị hỏi đáp

## Câu từ cấp lãnh đạo

Nhóm này khả năng cao hơn nhóm kỹ thuật bên dưới. Trả lời bằng ngôn ngữ kinh doanh, đừng kéo về cơ chế.

**"Sao không thuê thêm người cho rẻ và đơn giản?"**

Một kỹ sư thêm vào chi phí khoảng hai nghìn đô một tháng và làm được việc trong giờ hành chính. TraceAI tốn hai trăm năm hai đô một tháng, chạy hai mươi tư trên bảy, và không quên cái nó từng điều tra.

Nhưng em không đặt nó là thay người. Bảy trăm sáu mươi giờ tiết kiệm được không phải để cắt biên chế, mà là bảy trăm sáu mươi giờ kỹ sư quay lại làm sản phẩm thay vì ngồi dò log.

**"Rủi ro lớn nhất của việc này là gì?"**

Em nghĩ có hai.

Một là phụ thuộc nhà cung cấp mô hình. Nếu AWS đổi giá thì chi phí đổi theo. Nhưng phần mô hình chỉ là một trăm bốn tư đô một tháng, và kiến trúc cho phép đổi sang mô hình khác mà không phải viết lại hệ thống, vì phần mô hình được tách riêng.

Hai là người dùng tin kết quả quá mức. Chỗ này em chặn bằng thiết kế: mọi kết luận phải kèm bằng chứng thật, thiếu thì phải khai là thiếu, và hệ thống không tự sửa production. Nhưng đây là rủi ro cần theo dõi liên tục chứ không phải giải quyết một lần.

**"Nếu người xây nghỉ việc thì hệ thống có chết không?"**

Không. Công nghệ dùng đều là phổ thông, không có gì tự chế. Tài liệu kiến trúc và sơ đồ có sẵn. Thêm một nguồn dữ liệu mới là thêm một tệp cấu hình, không phải đọc hiểu toàn hệ thống.

Nhưng em nói thật là hiện tại nó vẫn phụ thuộc vào một nhóm nhỏ. Nếu muốn nó thành nền tảng dùng chung thì cần chuyển giao chính thức, và đó là việc chưa làm.

**"Có vướng gì về tuân thủ hay pháp lý không?"**

Ba điểm em đã tính. Dữ liệu khách hàng không rời khỏi hạ tầng của mình. Dữ liệu định danh được che trước khi tới mô hình. Và mọi lần chạy đều có nhật ký: ai hỏi, hỏi gì, lúc nào.

Em chưa đưa qua rà soát tuân thủ chính thức. Nếu hội đồng thấy cần thì đó là bước tiếp theo nên làm.

**"Đây là sản phẩm hay là dự án phụ của một nhóm?"**

Hiện tại nó nằm giữa. Nó đã chạy thật, có người dùng thật, có số liệu vận hành thật — không còn là thử nghiệm. Nhưng nó chưa có đội vận hành riêng và chưa nằm trong danh mục hệ thống chính thức.

Em báo cáo kết quả hôm nay để hội đồng thấy nó đang ở đâu, chứ chưa đề xuất đưa nó thành sản phẩm chính thức.

---

## Câu chắc chắn sẽ bị hỏi

**"Làm sao biết mốc sáu mươi phút là đúng?"**

Đây là ước tính từ mẫu sự cố xử lý tay, em không giấu điều đó. Nên cách em kiểm tra là thử hạ mốc xuống xem kết luận có đổ không.

Nếu mốc thật chỉ là hai mươi phút, tức là một phần ba con số em đưa, thì ra bảy trăm sáu mươi giờ giảm còn hai trăm hai mươi bảy giờ, giá trị hai nghìn tám trăm ba ba đô, ROI vẫn mười một phẩy hai lần.

Nếu mốc chỉ là mười phút thì ROI còn bốn phẩy sáu lần. Vẫn dương.

Điểm hòa vốn rơi ở mốc thủ công khoảng bốn phút rưỡi. Mà bốn phút rưỡi thì gần bằng đúng thời gian máy chạy, tức là gần như không còn gì để tiết kiệm.

Nói cách khác, con số tuyệt đối phụ thuộc giả định, nhưng kết luận "đáng làm" thì không đổ kể cả khi em sai ba lần.

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

Nên em nhìn nó theo hướng ngược lại: đây là một lý do cụ thể để đẩy chuẩn hóa tracing rộng ra. Service nào chuẩn hóa xong thì giá trị thu về đo được ngay trên chính service đó.

**"Sao chọn LangGraph mà không tự viết vòng lặp?"**

Cái em cần ở framework chỉ có hai thứ: quản lý trạng thái theo bước, và checkpoint để phục hồi. LangGraph cho sẵn cả hai. Tự viết thì cũng ra, nhưng mất thêm thời gian mà không tạo thêm giá trị nào cho bài toán này. Phần logic riêng của TraceAI nằm ở tool registry và ở chiến lược thu hẹp, không nằm ở vòng lặp.

**"Nếu agent chạy loạn, gọi công cụ mãi không dừng thì sao?"**

Có hai chốt. Ngân sách vòng lặp giới hạn số lần gọi công cụ. Và khi chạm ngưỡng thì có bước kết luận bắt buộc: hệ thống tắt hết công cụ, agent buộc phải chốt bằng dữ liệu đang có, hoặc khai là chưa đủ bằng chứng. Nên chi phí mỗi lần chạy có trần, không có trường hợp một request đốt hết ngân sách tháng.

**"Nếu người xây nghỉ việc thì sao?"**

Stack là công nghệ phổ thông: Python, FastAPI, PostgreSQL, React. Không có framework tự chế. Kiến trúc tool registry nên thêm nguồn dữ liệu là thêm một file, không phải đọc hiểu toàn hệ thống.

---

# Ghi chú cho người trình bày

**Nhịp độ**

Bốn slide cần chậm và rõ, vì đây là chỗ hội đồng ra đánh giá: slide 8 (dữ liệu khách hàng), slide 10 (kết quả), slide 11 (chi phí), slide 12–13 (so với đi mua).

Ba slide có thể lướt: slide 7 (tính năng), slide 9 (quản trị), slide 14 (mở rộng).

Slide 4 và slide 5 đã được rút gọn có chủ đích. Đừng sa vào chi tiết kỹ thuật ở hai slide này — nếu có người muốn đi sâu, hẹn trả lời ở phần hỏi đáp và dùng Phụ lục kỹ thuật.

**Nếu bị hỏi cắt ngang giữa chừng**

Trả lời ngắn rồi quay lại mạch. Nếu câu hỏi rơi đúng vào slide sắp tới thì nói: "Câu này em có một slide riêng, xin phép trả lời ở phần sau ạ."

**Thái độ với con số**

Chủ động nói cái nào là ước tính trước khi bị hỏi. Ban giám khảo tin người tự vạch ra giới hạn của mình hơn người trình bày toàn số đẹp.

Đừng nói "tiết kiệm được rất nhiều". Nói "bảy trăm sáu mươi giờ, dựa trên giả định mốc thủ công sáu mươi phút".

**Ba câu phải nói bằng được, dù có bị cắt thời gian thế nào**

1. Một tiếng xuống ba phút, ba mươi hai xu một lần.
2. Mô hình không bao giờ thấy dữ liệu khách hàng thật.
3. Hoàn vốn trong tuần đầu, ROI ba mươi tám lần.
