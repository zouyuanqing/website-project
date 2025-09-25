# Gunicorn配置文件
# 用于生产环境部署

import os
import multiprocessing

# 基本配置
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# 超时配置
timeout = 30
keepalive = 2

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程配置
daemon = False
pidfile = "logs/gunicorn.pid"
user = None
group = None

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 预加载应用
preload_app = True

# 钩子函数
def when_ready(server):
    """服务器启动完成时调用"""
    server.log.info("服务器启动完成")

def on_starting(server):
    """服务器启动时调用"""
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    server.log.info("正在启动服务器...")

def on_reload(server):
    """重载时调用"""
    server.log.info("服务器重载中...")

def worker_int(worker):
    """工作进程收到SIGINT信号时调用"""
    worker.log.info("工作进程 %s 收到中断信号", worker.pid)

def pre_fork(server, worker):
    """fork工作进程前调用"""
    server.log.info("正在启动工作进程 %s", worker.pid)

def post_fork(server, worker):
    """fork工作进程后调用"""
    server.log.info("工作进程 %s 已启动", worker.pid)

def worker_abort(worker):
    """工作进程异常退出时调用"""
    worker.log.info("工作进程 %s 异常退出", worker.pid)
