# Hướng dẫn vận hành Lab 04
# (Đóng gói ứng dụng bằng Docker)

Đây là tài liệu hướng dẫn
vận hành chi tiết nhất.
Tài liệu này được soạn thảo
dành riêng cho phân hệ
Analytics Service (B5).

## Thông tin dự án

Mã nguồn ứng dụng chạy thật
nằm tại `src/analytics_app/`.
Trong khi đó, thư mục
`src/iot_app/` được giữ lại
để làm mẫu đối chiếu.
Cổng chạy mạng mặc định
của container là 8000.

## Hướng dẫn từng bước

### Bước 1: Môi trường

Hãy sao chép tệp cấu hình
từ bản mẫu chuẩn bị sẵn:

```bash
cp .env.example .env
```

### Bước 2: Cài thư viện

Tải và cài đặt tất cả
các thư viện cần thiết:

```bash
npm install
```

### Bước 3: Build Image

Chạy lệnh sau để tiến hành
đóng gói thành Docker image:

```bash
docker build \
  -t fit4110/analytics-service:lab04 \
  .
```

### Bước 4: Run Container

Bắt đầu khởi chạy container
dựa trên image vừa tạo ra:

```bash
docker run -d \
  --name fit4110-analytics-lab04 \
  -p 8000:8000 \
  --env-file .env \
  fit4110/analytics-service:lab04
```

### Bước 5: Healthcheck

Gọi API để kiểm tra xem
ứng dụng đã sẵn sàng chưa:

```bash
curl http://localhost:8000/health
```

## Phần kiểm thử Newman

Tiến hành chạy bộ kiểm thử
bằng phần mềm Newman ở local:

```bash
npm run test:local
```

Sau khi chạy hoàn tất,
các báo cáo kết quả
sẽ được tự động xuất ra
bên trong thư mục `reports/`.

## Phần Gắn tag lớp học và push

Thực hiện gắn tag lớp học
và đẩy image lên registry:

```bash
docker tag \
  fit4110/analytics-service:lab04 \
  ghcr.io/connectivity-services-ad-pt/team-analytics:v0.1.0-team-analytics

docker push \
  ghcr.io/connectivity-services-ad-pt/team-analytics:v0.1.0-team-analytics
```

## Phần dọn dẹp hệ thống

Cuối cùng, hãy dọn dẹp
hệ thống bằng các lệnh sau:

```bash
docker stop \
  fit4110-analytics-lab04

docker rm \
  fit4110-analytics-lab04
```
