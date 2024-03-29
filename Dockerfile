FROM python:3

# 复制项目文件到容器中
COPY . /app

# 设置工作目录为项目目录
WORKDIR /app

# 安装项目依赖项
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# 运行docker run命令
CMD python main.py
