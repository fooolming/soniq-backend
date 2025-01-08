# 使用 Python 官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 将后端代码拷贝到容器中
COPY . .

# 暴露 Flask 的 5000 端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]
