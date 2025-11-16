# Game Classic Pong – Lập Trình Mạng

Đồ án môn **Lập Trình Mạng**: Xây dựng game Pong cổ điển bằng **Python + Pygame**, kết hợp:

- Chế độ **chơi local (offline)** với AI, menu chính, chọn độ khó, âm thanh.
- Chế độ **chơi mạng (client–server)** với 2 người chơi điều khiển từ 2 client khác nhau, có âm thanh và luật thắng.

---

## 1. Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.x (đã test với Python 3.11)
- **Thư viện:**
  - `pygame` – hiển thị đồ họa, xử lý input, âm thanh.
  - `socket` – lập trình mạng TCP (server–client).
  - `threading` – xử lý đa luồng (server phục vụ nhiều client, client vừa nhận state vừa render).

Cài đặt thư viện:

```bash
pip install -r requirements.txt

2.Cấu trúc thư mục
Game-Classic-Pong/
├─ main.py             # Chế độ chơi local (menu, AI, độ khó, âm thanh)
├─ ball.py             # Lớp Ball: quản lý bóng
├─ move_paddle.py      # Lớp Paddle + AI paddle
├─ pong_server.py      # Server TCP cho chế độ chơi mạng
├─ pong_client.py      # Client Pygame kết nối server, hiển thị game
├─ sounds/
│   ├─ hit.wav         # Âm thanh bóng chạm paddle
│   └─ score.wav       # Âm thanh ghi điểm
├─ README.md           # Tài liệu mô tả (file này)
└─ requirements.txt

3. Chế độ chơi local – main.py
3.1. Tính năng

Menu chính:

ENTER – Bắt đầu chơi.

S – Vào màn Settings (chọn độ khó).

Q – Thoát game.

Settings (cài đặt độ khó):

1 – Easy: bóng chậm, AI yếu.

2 – Medium: cân bằng.

3 – Hard: bóng nhanh, AI phản xạ tốt.

ESC – Quay lại menu.

Trong game (local):

Một người chơi vs AI bot (paddle bên kia).

Bóng di chuyển, va chạm tường, va chạm paddle, tính điểm.

Âm thanh:

hit.wav – bóng chạm paddle.

score.wav – khi một bên ghi điểm.

Giao diện đơn giản, có đường kẻ giữa, màu nền tối, paddle trắng.

Lưu ý: Bản local không có giới hạn điểm, chơi đến khi người chơi nhấn ESC để quay về menu hoặc tắt cửa sổ.

3.2. Điều khiển (local)

Paddle người chơi:

W / S hoặc ↑ / ↓

Phím khác:

ESC – Tạm dừng và quay về menu chính (khi đang chơi).

Alt + F4 / nút close (X) – Thoát game.

3.3. Cách chạy chế độ local

Tại thư mục project (nơi có main.py):

python main.py

4. Chế độ chơi mạng – pong_server.py & pong_client.py

Ở chế độ này, game chạy theo mô hình:

Server:

Quản lý trạng thái game chung: vị trí bóng, paddle, điểm số.

Nhận vị trí paddle từ 2 client.

Cập nhật logic, xử lý va chạm, tính điểm.

Gửi trạng thái game (game_state) về cho tất cả client ~30 FPS.

Mỗi client:

Kết nối tới server qua TCP.

Gửi vị trí paddle của mình lên server.

Nhận game_state từ server và vẽ lên màn hình.

Phát âm thanh:

Bóng chạm paddle → hit.wav.

Một bên ghi điểm → score.wav.

Áp dụng luật thắng: ai đạt 5 điểm trước thì thắng.

4.1. Luật chơi (network)

Mỗi client sẽ là một Player:

Player 1 → paddle bên trái.

Player 2 → paddle bên phải.

Server cập nhật bóng, paddle, điểm giống bản local.

Khi một bên đạt 5 điểm:

Cả 2 client sẽ hiển thị:

YOU WIN! cho bên thắng.

YOU LOSE! cho bên thua.

Game dừng, người chơi nhấn ESC để thoát client.

Muốn chơi ván mới → mở lại client.

4.2. Điều khiển (client)

Paddle:

↑ / ↓ – di chuyển paddle của client đó.

Phím khác:

ESC – Thoát game (nhất là sau khi ván đấu kết thúc).

Đóng cửa sổ – thoát client.

4.3. Cách chạy server & 2 client (trên cùng 1 máy)

Chạy server:

python pong_server.py


Console sẽ hiện:

Server started on localhost:5555

Waiting for players...

Chạy client 1 (Player 1 – bên trái):

Mở terminal thứ 2:

python pong_client.py


Cửa sổ sẽ báo Connected as Player 1.

Chạy client 2 (Player 2 – bên phải):

Mở terminal thứ 3:

python pong_client.py


Cửa sổ sẽ báo Connected as Player 2.

Sắp xếp cửa sổ để dễ chơi (Windows):

Chọn cửa sổ Player 1 → bấm Windows + ←.

Chọn cửa sổ Player 2 → bấm Windows + →.

Giờ bạn có thể chơi Pong 2 người qua server: mỗi bên điều khiển paddle của mình, có âm thanh và luật thắng 5 điểm.

4.4. Chạy server & client trên nhiều máy khác nhau

Ở máy chạy server:

Đảm bảo firewall cho phép Python nhận kết nối TCP cổng 5555.

Tìm địa chỉ IP của máy (ví dụ: 192.168.1.10).

Ở client:

Trong pong_client.py, khi tạo client:

client = PongClient(host="192.168.1.10", port=5555)


Hoặc sửa sẵn host="192.168.1.10" trong file.

5. Yêu cầu hệ thống

Python 3.10+ (khuyến nghị 3.11).

Đã cài Pygame và các thư viện trong requirements.txt.

Thư mục sounds/ phải tồn tại với:

sounds/hit.wav

sounds/score.wav

6. Cách chạy nhanh (tóm tắt)
6.1. Local game (vs AI):
python main.py

6.2. Online game (2 người qua server):

Terminal 1:

python pong_server.py


Terminal 2:

python pong_client.py


Terminal 3:

python pong_client.py

7. Thành viên nhóm 
balx8 – Nhóm trưởng

Cao Sỹ Tuấn Anh (anh16121978-sys) – Thành viên

Bảo Quân (BaoQuanLee) – Thành viên

Loivo2005 – Thành viên

ngocongduc2 – Thành viên