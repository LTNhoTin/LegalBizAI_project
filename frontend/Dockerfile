# Sử dụng một phiên bản Node.js cụ thể thay vì 'latest'
FROM node:18-alpine

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép package.json và package-lock.json (nếu có)
COPY package*.json ./

# Cài đặt dependencies
RUN npm install

# Sao chép toàn bộ source code vào thư mục làm việc
COPY . .

# Tăng giới hạn bộ nhớ cho Node.js
ENV NODE_OPTIONS=--max-old-space-size=4096

# Mở cổng 5173
EXPOSE 5173

# Chạy ứng dụng
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
