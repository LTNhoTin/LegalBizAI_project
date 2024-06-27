# Sử dụng Node.js image chính thức từ Docker Hub
FROM node:18-alpine

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file package.json và package-lock.json vào container
COPY package*.json ./

# Cài đặt các dependencies
RUN npm install

# Sao chép tất cả các file từ máy chủ vào container
COPY . .

# Expose port 5000
EXPOSE 5000

# Chạy ứng dụng
CMD ["node", "src/index.js"]
