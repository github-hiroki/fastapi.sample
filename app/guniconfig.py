# Copyright 2020- hiroki.h Inc.

import multiprocessing


# Host
bind = '127.0.0.1:80'

# Process Naming
name = 'gunicorn'
proc_name = 'fastapi_app_wsgi'

# Worker Processes
worker_class = 'uvicorn.workers.UvicornWorker'
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 120
keepalive = 2

# Logging
accesslog = '/var/log/fastapi_app.access.log'
errorlog = '/var/log/fastapi_app.error.log'
loglevel = 'info'
