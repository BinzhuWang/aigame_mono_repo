FROM python:3.12-slim
# RUN sed -i 's|http://deb.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
#     sed -i 's|http://security.debian.org|https://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources && \
#     apt-get update

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip  ffmpeg
RUN curl -fsSL https://deno.land/install.sh | sh
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple

WORKDIR /app
COPY requirements.lock ./
RUN uv pip install --no-cache --system -r requirements.lock -i https://mirrors.aliyun.com/pypi/simple
COPY prompts ./prompts
COPY models ./models
COPY src .
CMD ["/bin/bash", "-c", "uvicorn tools.main:app --host 0.0.0.0 --port 80 --timeout-keep-alive 60 --log-level info --access-log 2> >(tee -a logs/error.log) | tee -a logs/app.log"]

