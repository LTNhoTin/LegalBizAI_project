# Sử dụng image python chính thức
FROM python:3.9-slim-buster

# Cài đặt các dependencies cần thiết
RUN apt-get update && apt-get install -y build-essential curl

# Cài đặt Rust cho maturin
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Nâng cấp pip và cài đặt maturin
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir maturin

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt underthesea với --no-build-isolation
RUN pip install --no-cache-dir underthesea --no-build-isolation

# Sao chép tất cả các file vào container
COPY . .

# Thiết lập biến môi trường PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
