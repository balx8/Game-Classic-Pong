# 🎮 Game Classic Pong (Python + Pygame)

Dự án xây dựng lại game **Pong cổ điển** bằng Python và thư viện **Pygame**.  
Người chơi điều khiển 2 thanh chắn (paddle) để đánh bóng qua lại, ai để bóng lọt qua phía mình thì đối phương được điểm.

---

## 📌 Mục tiêu

- Ôn luyện lập trình Python và Pygame.
- Thực hành lập trình game 2D đơn giản (vòng lặp game, xử lý sự kiện, va chạm…).
- Làm việc nhóm với Git/GitHub (branch, pull request, review, merge, issues…).
- Xây dựng bản demo hoàn chỉnh có tài liệu và hình ảnh minh hoạ.

---

## ✨ Tính năng chính

- Hai người chơi điều khiển paddle ở hai bên màn hình.
- Bóng di chuyển liên tục, bật lại khi chạm paddle hoặc cạnh trên/dưới.
- Tính điểm cho từng người chơi khi bóng lọt qua paddle đối phương.
- Có thể chạy:
  - **Chế độ offline (local)** trên 1 máy.
  - (Tuỳ chọn) **Chế độ chơi mạng (client–server)** nếu bật phần này trong code.

---

## 🧰 Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.x  
- **Thư viện:**  
  - `pygame` – hiển thị đồ hoạ, xử lý input, vòng lặp game  
  - `socket` (hoặc tương tự) – phục vụ chế độ chơi qua mạng (server–client, nếu sử dụng)  

---

## 🖥️ Yêu cầu hệ thống

- Python 3.x  
- Đã cài `pip`  
- Hệ điều hành: Windows / macOS / Linux (cài được Pygame là chạy được).

---

## 🚀 Cài đặt

```bash
# Clone dự án
git clone https://github.com/balx8/Game-Classic-Pong.git
cd Game-Classic-Pong

# (Tuỳ chọn) Tạo môi trường ảo
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

▶️ Hướng dẫn chạy demo
1. Chạy demo offline (local)
python main.py


Sau khi chạy, cửa sổ game Pygame sẽ hiện lên.

Điều khiển (ví dụ – chỉnh lại nếu code khác):

Người chơi 1 (trái):

W – đi lên

S – đi xuống

Người chơi 2 (phải):

↑ – đi lên

↓ – đi xuống

2. Chạy demo chế độ chơi qua mạng (client–server)

Chỉ dùng nếu đã cấu hình chế độ mạng trong code.

Bước 1 – Chạy server (máy chủ)

python pong_server.py
# hoặc:
python server.py   # nếu nhóm dùng file này


Bước 2 – Chạy client (máy người chơi)

Trên từng máy client:

python pong_client.py


Các client kết nối tới địa chỉ IP/port của server (được cấu hình trong code).

Sau khi kết nối thành công, mỗi client điều khiển một paddle.
📁 Cấu trúc thư mục (tham khảo)
Game-Classic-Pong/
├── main.py           # File chạy game offline / demo chính
├── ball.py           # Định nghĩa lớp Ball – logic di chuyển & va chạm của bóng
├── move_paddle.py    # Xử lý di chuyển paddle (input người dùng)
├── pong_client.py    # Logic client khi chơi qua mạng
├── pong_server.py    # Logic server cho chế độ chơi mạng
├── server.py         # Script khởi động server (nếu dùng)
├── requirements.txt  # Danh sách thư viện cần cài
└── README.md         # Tài liệu dự án (file này)

🎮 Cách chơi

Chạy game theo hướng dẫn ở phần Hướng dẫn chạy demo.

Mỗi người chơi dùng bộ phím của mình để di chuyển paddle lên/xuống.

Bóng sẽ:

Bật lại khi chạm paddle.

Bật lại khi chạm cạnh trên/dưới màn hình.

Nếu bóng đi qua biên trái/phải (lọt qua paddle) → người còn lại ghi điểm.

Có thể đặt luật:

Chơi tự do cho tới khi thoát game.

Hoặc ai đạt trước một số điểm (ví dụ 10 điểm) thì thắng.

📝 Tiến độ & kết quả nhóm
Tiến độ thực hiện (tóm tắt theo các issue trên GitHub)

Giai đoạn 1 – Chuẩn bị & khởi tạo dự án

Setup repository & upload code gốc.

Tạo cấu trúc thư mục, khởi tạo main.py.

Tạo .gitignore và môi trường làm việc Python.

Chuẩn bị tài nguyên game (hình ảnh, font, âm thanh… nếu có).

Giai đoạn 2 – Xây dựng tính năng chính

Xây dựng class Ball.

Xây dựng class Paddle.

Xử lý va chạm giữa bóng – paddle – biên.

Thêm điểm số và giao diện hiển thị.

Giai đoạn 3 – Hoàn thiện & tài liệu

Review và merge code từ các nhánh feature/....

Test tổng thể để đảm bảo game chạy ổn định.

Viết README ban đầu, cập nhật README cuối cùng, bổ sung hướng dẫn và hình minh hoạ.

Phân công công việc

Phân chia theo vai trò chính, các thành viên có hỗ trợ lẫn nhau trong quá trình làm việc.

balx8 – Nhóm trưởng

Setup repository, tạo cấu trúc thư mục.

Khởi tạo main.py, tổ chức vòng lặp game.

Quản lý issues, review & merge pull request.

Viết và cập nhật README, tổng hợp báo cáo nhóm.

Cao Sỹ Tuấn Anh (anh16121978-sys)

Xây dựng class Ball, xử lý di chuyển bóng.

Tham gia xử lý va chạm bóng với paddle/biên.

Hỗ trợ test và tối ưu logic game.

Bảo Quân (BaoQuanLee)

Xây dựng class Paddle, điều khiển di chuyển paddle.

Thêm phần giao diện và hiển thị điểm số.

Hỗ trợ chỉnh sửa UI/UX trong game.

Loivo2005

Chuẩn bị và quản lý tài nguyên game (hình ảnh, asset… nếu có).

Thiết lập môi trường, .gitignore, hỗ trợ các bạn run project.

Tham gia test chức năng tổng thể.

ngocongduc2

Hỗ trợ triển khai/khảo sát chế độ chơi mạng (client–server) (nếu enable).

Tham gia kiểm thử, phát hiện và sửa bug.

Góp ý cải tiến hiệu năng và trải nghiệm chơi.

Kết quả đạt được

Hoàn thành game Pong chạy ổn định trên máy local.

Quy trình làm việc nhóm trên GitHub rõ ràng: issues, branches, pull request, review, merge.

Code được tách module (ball, paddle, xử lý input, server/client…) giúp dễ bảo trì và mở rộng.

Có tài liệu README hướng dẫn đầy đủ cách cài đặt, chạy demo và mô tả quá trình làm việc nhóm.

🖼️ Hình ảnh minh hoạ

<img width="1002" height="791" alt="image" src="https://github.com/user-attachments/assets/8da5c5e1-939c-4349-b356-ada180f19f55" />


<img width="997" height="796" alt="image" src="https://github.com/user-attachments/assets/3cf8b4fb-9b53-4906-ae95-6f24f6c21a9e" />


🔮 Hướng phát triển thêm

Thêm menu chính (Start, Settings, Quit).

Thêm AI bot để người chơi solo với máy.

Thêm âm thanh khi bóng chạm paddle/biên, khi ghi điểm.

Thêm tuỳ chọn độ khó (tăng tốc bóng, chỉnh kích thước paddle…).

Cải thiện giao diện: màu sắc, font chữ, hiệu ứng chuyển cảnh.

👥 Thành viên nhóm

balx8 – Nhóm trưởng

Cao Sỹ Tuấn Anh (anh16121978-sys) – Thành viên

Bảo Quân (BaoQuanLee) – Thành viên

Loivo2005 – Thành viên

ngocongduc2 – Thành viên
