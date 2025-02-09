FROM python:3.9-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
	portaudio19-dev \
	gcc \
	&& rm -rf /var/lib/apt/lists/*

# Python の依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY src/ .

CMD ["python", "realtime_transcription.py"]
