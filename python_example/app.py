import uuid
from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Configure OpenTelemetry
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "ms-api"})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Configure the trace processor
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Flask
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    with trace.get_tracer(__name__).start_as_current_span("hello") as span:
        tracking_id = str(uuid.uuid4())
        span.set_attribute("tracking_id", tracking_id)
        return jsonify({"message": "Hello from Flask API!", "tracking_id": tracking_id})

@app.route("/api")
def api():
    with trace.get_tracer(__name__).start_as_current_span("api") as span:
        tracking_id = str(uuid.uuid4())
        span.set_attribute("tracking_id", tracking_id)
        return jsonify({"result": "You are at the API endpoint.", "tracking_id": tracking_id})

if __name__ == "__main__":
    app.run(debug=True)

# Uninstrument Flask when the application closes
FlaskInstrumentor().uninstrument_app(app)
