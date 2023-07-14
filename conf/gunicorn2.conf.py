bind = "0.0.0.0:80"
workers = 1
accesslog = "/root/logs/http.gunicorn.access.log"
errorlog = "/root/logs/http.gunicorn.info.log"
capture_output = True
loglevel = "debug"