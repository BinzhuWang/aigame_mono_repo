FROM ubuntu:22.04
RUN apt-get update -y && \
    apt-get install -y ffmpeg libasound2-dev && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY target/fast/aigame-backend /app
RUN chmod +x /app

ENTRYPOINT ["/app"]
