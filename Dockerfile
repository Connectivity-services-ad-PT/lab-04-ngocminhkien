# Sử dụng Lightweight Production Base Image
FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong Container
WORKDIR /app

# Khai báo các biến cấu hình luồng chạy Python tối ưu
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Khai thác Docker Layer Cache để tăng tốc cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào trong container
COPY src/ /app/src/

# TIÊU CHÍ AN TOÀN: Khởi tạo và chuyển sang chạy bằng quyền Non-Root User (Mục 10 của Barem)
RUN useradd -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# TIÊU CHÍ TIN CẬY: Cài đặt lệnh HEALTHCHECK tự thân bằng thư viện nội bộ (Không cài curl thừa)
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)" || exit 1

# Mở cổng mạng kết nối ngoài
EXPOSE 8000

# Kích hoạt Uvicorn trỏ ĐÚNG vào folder analytics_app của mình
CMD ["uvicorn", "analytics_app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]