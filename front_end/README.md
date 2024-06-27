## Build và chạy ứng dụng bằng Docker Compose

### Bước 1: Mở Terminal và điều hướng đến thư mục gốc của dự án

Trước tiên, mở Terminal và điều hướng đến thư mục gốc của dự án, nơi bạn đã tạo file `Dockerfile` và `docker-compose.yml`.

### Bước 2: Build Docker image và khởi chạy container

Để build Docker image và khởi chạy container, chạy lệnh sau trong Terminal:

```bash
docker-compose up --build
```
### Bước 3: Truy cập vào ứng dụng
Sau khi container đã chạy, bạn có thể truy cập vào ứng dụng frontend của mình từ trình duyệt với địa chỉ http://localhost:3000.
