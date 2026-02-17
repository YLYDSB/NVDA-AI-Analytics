# 使用官方 Python 3.11 镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件（requirements.txt）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有项目文件到容器里
COPY . .

# 暴露端口（8000 是后端，8501 是前端）
EXPOSE 8000 8501

# 默认命令（会被 docker-compose 覆盖）
CMD ["python", "main.py"]