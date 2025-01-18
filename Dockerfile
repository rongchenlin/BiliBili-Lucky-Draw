FROM python:3.11.6

# 复制项目文件到容器中
COPY . /app

# 设置工作目录为项目目录
WORKDIR /app

# 更新python安装依赖
RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 安装项目依赖项
RUN pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 运行docker run命令
CMD python main.py
