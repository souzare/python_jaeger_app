from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import sqlite3
import os
from prometheus_client import Counter, Histogram, Gauge
from prometheus_flask_exporter import PrometheusMetrics
from jaeger_client import Config

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def init_tracer(service):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    return config.initialize_tracer()

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
metrics = PrometheusMetrics(app)

REQUEST = Counter("http_requests_total", "Total number of requests made")
LATENCY = Histogram("http_request_duration_seconds", "Request latency in seconds")
ERRORS = Counter("http_request_errors_total", "Total number of request errors", ["error_type"])
POSTS_COUNT = Gauge("posts_count", "Current number of posts")

tracer = init_tracer('my-python-jaeger-app')

@app.route('/')
def index():
    with tracer.start_span('index_request') as span:
        span.set_tag('http.method', 'GET')
        return render_template('index.html')

# Additional routes and logic would go here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)