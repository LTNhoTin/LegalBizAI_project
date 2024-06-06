Hướng dẫn sử dụng công cụ gán ID và loại câu hỏi
Công cụ này được thiết kế để giúp bạn gán ID và xác định loại câu hỏi dựa trên các điều luật và nghị định có sẵn trong dữ liệu. Dưới đây là các bước hướng dẫn chi tiết để sử dụng công cụ này:

Bước 1: Chuẩn bị dữ liệu
qaset.json: File chứa danh sách câu hỏi và câu trả lời.
all_chunk.json: File chứa danh sách các điều luật và nghị định với các ID tương ứng.
Đảm bảo rằng cả hai file đều nằm trong cùng một thư mục với tệp mã nguồn Python.

Bước 2: Chạy công cụ
Mở tệp mã nguồn Python.
Chạy tệp mã nguồn bằng cách sử dụng trình biên dịch Python hoặc IDE ưa thích của bạn. Ví dụ: python script.py.
Bước 3: Giao diện công cụ
Khi công cụ được chạy, một cửa sổ giao diện sẽ xuất hiện với các phần chính sau:

Khung câu hỏi và câu trả lời:

Question: Hiển thị câu hỏi hiện tại.
Answer: Hiển thị câu trả lời cho câu hỏi đó.
Reference: Hiển thị các điều luật và nghị định liên quan đến câu hỏi.
Khung các khớp có thể:

ID: Hiển thị các ID của các điều luật và nghị định khớp với câu hỏi.
Title: Hiển thị tiêu đề của điều luật và nghị định.
Passage: Hiển thị đoạn văn bản của điều luật và nghị định.
Khung nhập ID và loại câu hỏi:

Nhập ID: Ô nhập cho phép bạn nhập ID cho câu hỏi hiện tại.
Loại câu hỏi: Ô nhập cho phép bạn nhập loại câu hỏi.
Nút lưu và điều hướng:

Lưu ID và loại câu hỏi: Nút này cho phép bạn lưu ID và loại câu hỏi sau khi nhập.
Quay lại câu hỏi trước: Nút này cho phép bạn quay lại câu hỏi trước đó nếu cần chỉnh sửa.
Bước 4: Gán ID và loại câu hỏi
Chọn câu hỏi từ danh sách. Công cụ sẽ hiển thị câu hỏi, câu trả lời và các điều luật liên quan.
Nhập ID vào ô "Nhập ID". Nếu câu hỏi có nhiều hơn một reference, công cụ sẽ hiển thị cảnh báo bằng dòng text màu đỏ.
Nhập loại câu hỏi vào ô "Loại câu hỏi".
Nhấn nút "Lưu ID và loại câu hỏi" để lưu thông tin.
Nhấn nút "Quay lại câu hỏi trước" nếu cần chỉnh sửa câu hỏi trước đó.
Bước 5: Lưu dữ liệu
Khi bạn đã gán ID và loại câu hỏi cho tất cả các câu hỏi, công cụ sẽ tự động lưu dữ liệu vào file qaset.json.

Lưu ý
Đảm bảo rằng bạn đã nhập đúng ID và loại câu hỏi trước khi lưu.
Nếu bạn gặp bất kỳ lỗi nào hoặc cần hỗ trợ, vui lòng không liên lạc hỗ trợ.



Ví dụ cụ thể
Chạy công cụ và chọn câu hỏi đầu tiên.
Xem câu hỏi và câu trả lời cùng với các điều luật liên quan.
Nhập ID tương ứng vào ô "Nhập ID".
Nhập loại câu hỏi vào ô "Loại câu hỏi".
Nhấn nút "Lưu ID và loại câu hỏi".
Tiếp tục với các câu hỏi tiếp theo cho đến khi hoàn tất.
Chúc bạn sử dụng công cụ thành công!