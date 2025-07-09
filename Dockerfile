# 🐍 Base image
FROM python:3.10-slim

# ✅ Set workdir
WORKDIR /app

# ✅ Install system dependencies
RUN apt update && \
    apt install -y gcc libffi-dev curl git && \
    apt clean && rm -rf /var/lib/apt/lists/*

# ✅ Copy all files
COPY . .

# ✅ Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Start the bot
CMD ["python3", "main.py"]
