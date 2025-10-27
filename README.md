# Pong Game (client-server)

Hướng dẫn này mô tả cách cài đặt và chạy game Pong có sẵn trong thư mục.

Yêu cầu
- Windows (PowerShell) hoặc bất kỳ hệ điều hành có Python
- Python 3.8+ (bản này đã kiểm tra với Python 3.11)
- pip (đi kèm Python)
- pygame (đã thêm vào `requirements.txt`)

Các file chính
- `pong_server.py` - server quản lý trạng thái trò chơi
- `pong_client.py` - client hiển thị game và gửi vị trí paddle
- `requirements.txt` - phụ thuộc (pygame)

Chạy nhanh (PowerShell)

1) (Tùy chọn) Tạo virtual environment và kích hoạt (khuyến nghị):

```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
```

2) Cài phụ thuộc:

```powershell
pip install -r .\requirements.txt
```

3) Mở terminal 1: chạy server

```powershell
python .\pong_server.py
```

Bạn sẽ thấy: "Server started on localhost:5555". Giữ terminal này mở.

4) Mở terminal 2 và terminal 3 (mỗi terminal một client) và chạy:

```powershell
python .\pong_client.py
```

Khi cả hai client kết nối, game sẽ tự động bắt đầu. Dùng phím mũi tên LÊN/XUỐNG để điều khiển paddle.

Chạy trên hai máy khác nhau
- Nếu muốn cho 2 máy khác nhau chơi, thay `host='localhost'` trong `pong_client.py` bằng địa chỉ IP của máy chạy server (ví dụ `host='192.168.1.5'`).
- Mở port 5555 trên firewall của máy server nếu cần (xem phần Troubleshooting).

Troubleshooting (lỗi thường gặp)
- ModuleNotFoundError: No module named 'pygame' → chạy `pip install pygame` (hoặc `pip install -r requirements.txt`).
- OSError: [WinError 10048] address already in use → port 5555 đã dùng; đổi port trong `pong_server.py` và `pong_client.py` hoặc dừng process khác.
- ConnectionRefusedError → server chưa chạy hoặc firewall chặn; kiểm tra server đang chạy và tắt tường lửa tạm thời để thử.
- Nếu một client bị đóng, game sẽ dừng cho cả hai — khởi lại client hoặc server nếu cần.

Dừng server
- Nhấn Ctrl+C trong terminal server để dừng.

Ghi chú
- `requirements.txt` đã có `pygame>=2.1.0`; dự án này đã được kiểm tra với pygame 2.6.1 và Python 3.11.

Nếu bạn muốn, tôi có thể:
- Tạo script .bat để khởi server và 2 client tự động (trên cùng máy),
- Hoặc tạo virtualenv và cài pygame vào venv cho bạn ngay bây giờ.

Chúc bạn chơi vui!
