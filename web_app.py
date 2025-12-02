"""
🌍 Beautiful Travel Planner Web UI
A Streamlit-based web application for planning vacations with AI assistance
"""

import streamlit as st
import asyncio
import os
import logging
import uuid
from dotenv import load_dotenv
from datetime import datetime
import time

# 🤖 Import Microsoft Agent Framework Components
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework.observability import setup_observability, get_tracer, get_meter

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv._incubating.attributes.service_attributes import SERVICE_NAME
from opentelemetry.trace.span import format_trace_id

import requests
from random import uniform
import base64

# 🎨 Set Streamlit Page Configuration
st.set_page_config(
    page_title="✈️ AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔧 Load Environment Variables
load_dotenv()

# 📊 Setup Logging and Observability
serviceName = os.environ.get("OTEL_SERVICE_NAME", "travel-planner-web")
resource = Resource.create({SERVICE_NAME: serviceName})

logger = logging.getLogger()

def setup_logging():
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    handler = LoggingHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

setup_observability(enable_sensitive_data=True, exporters=["otlp"])
setup_logging()
tracer = get_tracer()
meter = get_meter()

# 🌏 Predefined Destinations with Descriptions
DESTINATIONS = {
    "Garmisch-Partenkirchen, Germany": "🏔️ Alpine village with stunning mountain views",
    "Munich, Germany": "🍺 Bavarian capital famous for culture and beer",
    "Barcelona, Spain": "🏖️ Coastal city with stunning architecture",
    "Paris, France": "🗼 The City of Light, romantic and iconic",
    "Berlin, Germany": "🎨 Historic and vibrant cultural hub",
    "Tokyo, Japan": "🗾 Bustling metropolis with ancient temples",
    "Sydney, Australia": "🦘 Opera House and beautiful beaches",
    "New York, USA": "🗽 The city that never sleeps",
    "Cairo, Egypt": "🔺 Gateway to ancient wonders",
    "Cape Town, South Africa": "🌅 Scenic beauty and Table Mountain",
    "Rio de Janeiro, Brazil": "🎭 Vibrant culture and beaches",
    "Bali, Indonesia": "🌴 Tropical paradise and spiritual haven"
}

# 🔌 Tool Functions for the Agent

def get_selected_destination(destination: str) -> str:
    """Return the selected destination.
    
    Args:
        destination: The selected destination
    Returns:
        str: Confirmation of the selected destination
    """
    delay_seconds = uniform(0, 0.99)
    time.sleep(delay_seconds)
    
    with tracer.start_as_current_span("get_selected_destination") as current_span:
        logger.info("[get_selected_destination] selected", extra={"destination": destination})
        current_span.set_attribute("destination", destination)
    
    return destination


def get_weather(location: str) -> str:
    """Get the weather for a given location.

    Args:
        location: The location to get the weather for.
    Returns:
        A short weather description string.
    """
    delay_seconds = uniform(0.3, 3.7)
    time.sleep(delay_seconds)

    # Fail every now and then to simulate real-world API unreliability
    if __import__('random').randint(1, 10) > 7:
        raise Exception("Weather service is currently unavailable. Please try again later.")

    request_id = str(uuid.uuid4())
    t0 = time.time()
    logger.info("[get_weather] start", extra={"request_id": request_id, "city": location})
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("[get_weather] missing API key", extra={"request_id": request_id})
        raise ValueError("Weather service not configured. OPENWEATHER_API_KEY environment variable is required.")
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        result = f"Weather in {location}: {weather}, Temperature: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%"
        elapsed_ms = int((time.time() - t0) * 1000)
        logger.info(
            "[get_weather] complete",
            extra={"request_id": request_id, "city": location, "weather": weather, "temp": temp, "elapsed_ms": elapsed_ms},
        )
        return result
    except requests.exceptions.RequestException as e:
        logger.error("[get_weather] request_error", extra={"request_id": request_id, "city": location, "error": str(e)})
        return f"Error fetching weather data for {location}. Please check the city name."
    except KeyError as e:
        logger.error("[get_weather] parse_error", extra={"request_id": request_id, "city": location, "error": str(e)})
        return f"Error parsing weather data for {location}."


def get_datetime() -> str:
    """Return the current date and time as an ISO-like string."""
    delay_seconds = uniform(0.10, 5.0)
    time.sleep(delay_seconds)
    return datetime.now().isoformat(sep=' ', timespec='seconds')


# ⚙️ Initialize Streamlit Session State
if "agent" not in st.session_state:
    model_id = os.environ.get("GITHUB_MODEL_ID", "gpt-4o-mini")
    openai_chat_client = OpenAIChatClient(
        base_url=os.environ.get("GITHUB_ENDPOINT"),
        api_key=os.environ.get("GITHUB_TOKEN"),
        model_id=model_id
    )
    
    st.session_state.agent = ChatAgent(
        chat_client=openai_chat_client,
        instructions="You are a helpful AI travel planning agent. Help users plan vacations with detailed itineraries, activities, and travel tips.",
        tools=[get_selected_destination, get_weather, get_datetime]
    )
    st.session_state.model_id = model_id
    st.session_state.travel_plan = None


# 🎨 Custom CSS Styling with New Relic Colors
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #00AC69 0%, #00ce7c 100%);
    }
    .stContainer {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .header-wrapper {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding: 15px;
        background: linear-gradient(135deg, #00AC69 0%, #00ce7c 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 206, 124, 0.3);
    }
    .logo-section {
        font-size: 2.5em;
    }
    .branding-text {
        color: white;
        font-weight: bold;
    }
    .branding-title {
        font-size: 1.8em;
        margin: 0;
        color: white;
    }
    .branding-subtitle {
        font-size: 0.9em;
        color: #00FF8C;
        margin: 5px 0 0 0;
    }
    .destination-card {
        background: linear-gradient(135deg, #00ce7c 0%, #00FF8C 100%);
        color: #001f3f;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.2s;
        font-weight: 600;
    }
    .destination-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 206, 124, 0.3);
        background: linear-gradient(135deg, #00FF8C 0%, #00ce7c 100%);
    }
    .header-title {
        text-align: center;
        background: linear-gradient(135deg, #00AC69 0%, #00ce7c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em;
        font-weight: bold;
        margin: 20px 0;
    }
    .result-container {
        background: linear-gradient(135deg, #00ce7c 0%, #00FF8C 100%);
        color: #001f3f;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 206, 124, 0.2);
    }
    .result-container h2 {
        color: #00AC69;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00AC69 0%, #00ce7c 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #00FF8C 0%, #00ce7c 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 206, 124, 0.3) !important;
    }
    /* Slider styling: target common browsers and Streamlit wrapper */
    .stSlider input[type=range], input[type=range] {
        -webkit-appearance: none !important;
        appearance: none !important;
        width: 100% !important;
        height: 10px !important;
        background: linear-gradient(90deg, #00ce7c, #00AC69) !important;
        border-radius: 10px !important;
        outline: none !important;
        border: none !important;
    }
    /* Webkit track */
    input[type=range]::-webkit-slider-runnable-track {
        height: 10px;
        background: linear-gradient(90deg, #00ce7c, #00AC69) !important;
        border-radius: 10px;
        border: none;
    }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none !important;
        appearance: none !important;
        width: 20px !important;
        height: 20px !important;
        background: #00FF8C !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
        border: 2px solid #00AC69 !important;
        margin-top: -5px; /* center thumb on track */
    }
    /* Firefox */
    input[type=range]::-moz-range-track {
        height: 10px;
        background: linear-gradient(90deg, #00ce7c, #00AC69) !important;
        border-radius: 10px;
        border: none;
    }
    input[type=range]::-moz-range-thumb {
        width: 20px !important;
        height: 20px !important;
        background: #00FF8C !important;
        border-radius: 50% !important;
        border: 2px solid #00AC69 !important;
    }
    /* IE/Edge */
    input[type=range]::-ms-track {
        height: 10px;
        background: transparent;
        border-color: transparent;
        color: transparent;
    }
    input[type=range]::-ms-fill-lower {
        background: linear-gradient(90deg, #00ce7c, #00AC69) !important;
        border-radius: 10px;
    }
    input[type=range]::-ms-thumb {
        width: 20px !important;
        height: 20px !important;
        background: #00FF8C !important;
        border-radius: 50% !important;
        border: 2px solid #00AC69 !important;
    }
    /* Remove focus ring red / ensure focus shows green accent */
    input[type=range]:focus, .stSlider input[type=range]:focus {
        outline: none !important;
        box-shadow: 0 0 0 4px rgba(0,206,124,0.15) !important;
    }
    .st-emotion-cache-11xx4re {
        background-color: #00FF8C !important;
    }
    .st-emotion-cache-jigjfz {
        color: #00FF8C !important;
    }
    /* Stronger overrides for Streamlit slider variants */
    .stSlider input[type=range], div[data-testid*="stSlider"] input[type=range], input[type=range] {
        accent-color: #00ce7c !important;
        -webkit-appearance: none !important;
        background: linear-gradient(135deg, #00FF8C, #00ce7c) !important;
    }
    /* Ensure any numeric label or value near the slider uses primary text color */
    div[data-testid*="stSlider"] span, .stSlider span {
        color: #001f3f !important;
    }
    /* Multi-select / select list styling */
    div[role="listbox"] {
        background: linear-gradient(135deg, rgba(0,206,124,0.08), rgba(0,255,140,0.06));
        border: 1px solid rgba(0,172,105,0.15);
        border-radius: 8px;
    }
    div[role="option"] {
        padding: 6px 8px;
    }
    /* Selected tokens (tags) */
    .css-1xt0rr2, .css-1v0mbdj { /* token classnames may vary between Streamlit versions; these are common */
        background: linear-gradient(135deg, #00FF8C, #00ce7c) !important;
        color: #00303a !important;
        border-radius: 6px !important;
    }
    /* Streamlit theme variable overrides to apply New Relic primary color */
    :root {
        --primaryColor: #00ce7c !important;
        --secondaryBackgroundColor: #ffffff !important;
        --primaryTextColor: #001f3f !important;
    }

    /* Force form controls and multiselect tokens into New Relic palette */
    .stSelectbox, .stSlider, .stMultiSelect, .stTextArea {
        color: #00AC69 !important;
    }

    /* Broad override to prevent any red text inside the multiselect component */
    .stMultiSelect * {
        color: #001f3f !important;
    }

    /* Tag/token styling inside multiselect (more specific targets may be needed per Streamlit version) */
    .stMultiSelect [data-baseweb="tag"], .stMultiSelect .css-1xt0rr2, .stMultiSelect .css-1v0mbdj {
        background: linear-gradient(135deg, #00FF8C, #00ce7c) !important;
        color: #00303a !important;
        border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🏠 Main UI Layout - Header with New Relic Branding
logo_path = os.path.join(os.path.dirname(__file__), "static", "assets", "newrelic-logo.png")
# Render header in a single column: embed logo as base64 to guarantee display and allow inline HTML
def _img_to_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return encoded
    except Exception:
        return ""

b64 = _img_to_base64(logo_path)
header_html = f"""
<div class="header-wrapper" style="display:flex; align-items:center; gap:12px;">
  {f'<img src="data:image/png;base64,{b64}" style="height:40px;" />' if b64 else ''}
  <div>
    <h1 class="branding-title" style="margin:0;">New Relic</h1>
    <p class="branding-subtitle" style="margin:4px 0 0 0;">DevRel AI Samples</p>
  </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

st.markdown('<div class="header-title">✈️ AI Travel Planner</div>', unsafe_allow_html=True)

st.markdown("---")

# 📍 Destination Selection Section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🌍 Select Your Destination")
    st.markdown("Choose from our curated list of amazing travel destinations!")
    
    selected_destination = st.selectbox(
        "Pick a destination:",
        options=list(DESTINATIONS.keys()),
        format_func=lambda x: f"{x} {DESTINATIONS[x]}",
        key="destination_select"
    )
    
    # Display destination details
    if selected_destination:
        st.info(f"📌 {DESTINATIONS[selected_destination]}")

with col2:
    st.subheader("✨ Trip Details")
    
    # Trip duration
    trip_duration = st.slider(
        "How many days for your trip?",
        min_value=1,
        max_value=14,
        value=3,
        step=1
    )
    
    # Travel interests
    interests = st.multiselect(
        "What are you interested in?",
        ["🏖️ Beach & Relaxation", "🎭 Culture & History", "🍽️ Food & Dining", 
         "🏔️ Adventure & Hiking", "🛍️ Shopping", "🎨 Art & Museums"],
        default=["🏖️ Beach & Relaxation"]
    )
    
    # Special requests
    special_requests = st.text_area(
        "Any special requests or requirements?",
        placeholder="E.g., budget-friendly, family-friendly, etc.",
        height=80
    )

st.markdown("---")

# 🤖 Generate Travel Plan
if st.button("🚀 Generate My Travel Plan", use_container_width=True, type="primary"):
    with st.spinner("✨ Planning your amazing trip..."):
        try:
            with tracer.start_as_current_span("plan_generation") as current_span:
                # Build the prompt with selected options
                interests_str = ", ".join(interests) if interests else "general sightseeing"
                special_requests_str = f"\nSpecial requests: {special_requests}" if special_requests else ""
                
                user_prompt = f"""Plan a {trip_duration}-day trip to {selected_destination}.

Interests: {interests_str}
{special_requests_str}

Please provide:
1. A detailed day-by-day itinerary with activities
2. Current weather information for the destination
3. Local cuisine recommendations
4. Best times to visit specific attractions
5. Travel tips and budget estimates
6. Current date and time reference"""

                logger.info("[plan_generation] starting", extra={"destination": selected_destination, "duration": trip_duration})
                current_span.set_attribute("destination", selected_destination)
                current_span.set_attribute("duration", trip_duration)
                
                # Run the agent asynchronously
                response = asyncio.run(st.session_state.agent.run(user_prompt))
                
                # Extract travel plan
                last_message = response.messages[-1]
                text_content = last_message.contents[0].text
                
                st.session_state.travel_plan = text_content
                
                # Log metrics
                span_id = format(current_span.get_span_context().span_id, "016x")
                trace_id = format_trace_id(current_span.get_span_context().trace_id)
                
                logger.info("[plan_generation] complete", extra={
                    "destination": selected_destination,
                    "span_id": span_id,
                    "trace_id": trace_id,
                    "model": st.session_state.model_id
                })
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            logger.error("[plan_generation] error", extra={"error": str(e)})

# 📋 Display Travel Plan
if st.session_state.travel_plan:
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.subheader("🏖️ Your Personalized Travel Plan")
    st.markdown(st.session_state.travel_plan)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download option
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download Plan as Text",
            data=st.session_state.travel_plan,
            file_name=f"travel_plan_{selected_destination.replace(',', '').replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 30px;">
    Made with ❤️ using AI Travel Planner | Powered by Microsoft Agent Framework
</div>
""", unsafe_allow_html=True)
