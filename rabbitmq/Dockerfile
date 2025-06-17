FROM rabbitmq:management

# 启用 rabbitmq_stream 插件
RUN rabbitmq-plugins enable --offline rabbitmq_stream


# 运行 RabbitMQ 服务器
CMD ["rabbitmq-server"]

