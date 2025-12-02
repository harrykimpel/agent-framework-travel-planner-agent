# Architecture

This document explains the high-level architecture and data flow of the AI Travel Planner sample.

## Overview

The Travel Planner is a Streamlit web UI that uses the Microsoft Agent Framework to generate AI-powered travel itineraries. It exposes a small set of tool functions the agent can call (destination selection, weather lookup, date/time) and uses OpenTelemetry for observability.

Components:

- `web_app.py` — Streamlit front-end, UI components, CSS theming, user input collection, and orchestration of agent prompts.
- `app.py` — Original CLI-style script that demonstrates agent usage and contains the same tool functions.
- `agent framework` — `ChatAgent` from the Microsoft Agent Framework which executes prompts and can call local Python tool functions.
- `OpenAIChatClient` (in-tree `agent_framework.openai`) — client wrapper for a GitHub Models / OpenAI-compatible API.
- `Tool functions` — small, synchronous Python functions the agent may call:
  - `get_selected_destination(destination: str)` — returns/validates the user-selected destination.
  - `get_weather(location: str)` — calls OpenWeather API and returns a short weather summary.
  - `get_datetime()` — returns current date/time string.
- `static/assets` — static assets such as `newrelic-logo.png` used by the UI.
- `OpenTelemetry` — used to create spans around operations (agent run, weather call) and export telemetry via OTLP to New Relic.

## Data Flow

1. User selects options in the Streamlit UI and presses "Generate My Travel Plan".
2. `web_app.py` constructs a detailed user prompt including destination, interests, duration, and special requests.
3. The `ChatAgent`'s `run()` method is invoked asynchronously with the prompt. The agent can call local tool functions (for example, to request weather data, or a confirmation of the destination).
4. Tool functions perform work and return structured text back to the agent, which can be incorporated into the final response.
5. The agent returns a composed message (day-by-day plan, weather, tips) which `web_app.py` renders in the UI and stores in `st.session_state`.
6. Telemetry (spans, logs, metrics) are emitted via OpenTelemetry for each interaction.

## Observability

- The application calls `setup_observability(enable_sensitive_data=True, exporters=["otlp"])` to enable OTLP export.
- Important spans include `main`, `plan_generation`, and `get_selected_destination` / `get_weather`.
- Logs contain structured metadata including `span_id` and `trace_id` to tie UI actions to backend traces.

## Extension Points

- Add new tool functions: create additional Python functions and include them in the `tools=[...]` list when creating the `ChatAgent`.
- Swap the model: change `GITHUB_MODEL_ID` or client configuration for different model behavior.
- Add caching: cache weather responses to reduce API calls.
- Add richer UI components: integrate maps, images, or booking links.

## Security Considerations

- Keep API keys out of source control; use environment variables or secrets stores.
- When enabling `enable_sensitive_data=True` for observability, be mindful of PII being sent to telemetry backends.

## File References

- `web_app.py` — main UI and orchestration
- `app.py` — CLI example and tool implementations
- `requirements.txt` — dependencies
- `static/assets/newrelic-logo.png` — branding asset

---

For deeper diagrams or deployment topology, see `DEPLOYMENT.md`.
