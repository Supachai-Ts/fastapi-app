FROM openjdk:17-slim

# ติดตั้ง Python + venv + git + docker-cli
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง alias python -> python3
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# ตรวจสอบเวอร์ชัน
RUN java -version && python --version && docker --version

