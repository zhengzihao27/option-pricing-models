FROM python:3.12-slim

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "--server.port", "8080", "--server.address", "0.0.0.0", "streamlit_app.py"]

# 构建镜像命令
# docker build -t options-pricing:latest .

# 运行容器命令
# docker run -p 8080:8080 options-pricing:latest
