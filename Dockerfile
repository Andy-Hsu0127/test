# 使用官方 Python 映像作為基礎映像
FROM python:3.11-slim

# 安裝系統依賴，包括 git 和編譯工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 暴露應用程式的埠（根據您的設定，例如 2000）
EXPOSE 2000

# 啟動應用程式
CMD ["python", "run_waitress.py"]
