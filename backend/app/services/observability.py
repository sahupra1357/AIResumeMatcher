from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)
from openinference.instrumentation.openai import OpenAIInstrumentor
import os
from dotenv import load_dotenv

def init_observability():
    """Initialize Arize Phoenix observability for OpenAI."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if Phoenix API key is set
    phoenix_api_key = os.getenv("PHOENIX_API_KEY")
    if not phoenix_api_key:
        print("Warning: PHOENIX_API_KEY not set in .env file. Observability disabled.")
        return
    
    try:
        # Set up OpenTelemetry headers with Phoenix API key
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={phoenix_api_key}"
        
        # Create span exporter to Phoenix
        span_exporter = HTTPSpanExporter(
            endpoint="https://llamatrace.com/v1/traces"
        )
        
        # Set up span processor
        span_processor = SimpleSpanProcessor(span_exporter)
        
        # Create tracer provider
        tracer_provider = trace_sdk.TracerProvider()
        tracer_provider.add_span_processor(span_processor=span_processor)
        
        # Instrument OpenAI
        OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
        
        print("✅ Arize Phoenix observability initialized successfully")
    except Exception as e:
        print(f"Warning: Failed to initialize observability: {e}")
