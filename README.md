# 🌐 Flask Web Application Guide

## Overview

The Travel Planner has been converted from a CLI application to a beautiful Flask-based web application with a modern, responsive UI featuring the New Relic theme.

## ✨ Features

### Web Interface

- **Beautiful Modern UI**: Clean, responsive design with New Relic branding
- **Interactive Form**: User-friendly travel planning form with:
  - Origin and destination selection
  - Date picker with calendar
  - Trip duration selector
  - Multi-select interests
  - Special requests text area
- **Real-time Feedback**: Loading indicators while AI generates plans
- **Result Display**: Formatted travel plans with easy-to-read layout
- **Error Handling**: Graceful error messages with retry options

### API Endpoints

- `GET /` - Home page with travel planning form
- `POST /plan` - Generate travel plan (returns HTML)
- `POST /api/plan` - Generate travel plan (returns JSON for API consumers)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Ensure your `.env` file contains:

```bash
OPENAI_API_KEY=your_openai_api_key
GITHUB_MODEL_ID=gpt-4o-mini
OTEL_SERVICE_NAME=travel-planner-web
# Optional: for real weather data
OPENWEATHER_API_KEY=your_weather_api_key
# Optional: New Relic configuration
NEW_RELIC_ENTITY_GUID=your_entity_guid
NEW_RELIC_ACCOUNT=your_account
NEW_RELIC_ACCOUNT_ID=your_account_id
NEW_RELIC_TRUSTED_ACCOUNT_ID=your_trusted_account_id
```

### 3. Run the Web Application

**Option A: Using the run script (recommended)**

```bash
./run_web.sh
```

**Option B: Direct Python execution**

```bash
python app.py
```

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

## 📁 Project Structure

```
travel-planner-agent/
├── app.py                 # Flask application (converted from CLI)
├── requirements.txt       # Python dependencies (Flask added)
├── run_web.sh            # Script to run the web app
├── templates/
│   ├── index.html        # Main form page
│   ├── result.html       # Travel plan display page
│   └── error.html        # Error page
├── static/
│   ├── styles.css        # Enhanced CSS with responsive design
│   └── assets/
│       └── newrelic-logo.png
└── .env                  # Environment variables
```

## 🎨 UI Features

### Design Highlights

- **New Relic Branding**: Consistent use of New Relic colors (#00AC69, #00ce7c, #00FF8C)
- **Gradient Backgrounds**: Modern gradient effects throughout
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Accessibility**: Proper labels, focus states, and semantic HTML

### Form Features

- **Smart Defaults**: Today's date pre-selected
- **Input Validation**: Required fields marked and validated
- **Multiple Selections**: Easy multi-select for interests
- **Loading State**: Visual feedback during AI processing

## 🔌 API Usage

### HTTP API Example

```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York, USA",
    "destination": "Paris, France",
    "date": "2025-12-15",
    "duration": "5",
    "interests": ["Culture & History", "Food & Dining"],
    "special_requests": "Looking for romantic spots"
  }'
```

### Response Format

```json
{
  "success": true,
  "travel_plan": "Detailed AI-generated travel plan...",
  "destination": "Paris, France",
  "duration": "5"
}
```

## 🛠️ Development

### Running in Debug Mode

The Flask app runs with `debug=True` by default in development:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Customization

- **Colors**: Update CSS variables in `styles.css`
- **Destinations**: Modify `DESTINATIONS` dict in `app.py`
- **Agent Instructions**: Update the agent prompt in the route handlers

## 📝 Migration from CLI

### Key Changes

1. **Added Flask Framework**: Web server with routing
2. **Created Templates**: HTML pages for UI
3. **Enhanced Styling**: Responsive CSS with New Relic theme
4. **Added CORS**: Support for API consumption
5. **Async Handling**: Event loop management for Flask
6. **Form Processing**: Extract data from POST requests
7. **Error Handling**: User-friendly error pages

### Preserved Features

- ✅ Microsoft Agent Framework integration
- ✅ OpenAI/GitHub Models support
- ✅ Weather API integration
- ✅ OpenTelemetry observability
- ✅ New Relic logging
- ✅ All tool functions (get_weather, get_datetime, get_random_destination)

## 🌟 Usage Tips

1. **Select Multiple Interests**: Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple interests
2. **Date Selection**: Click the calendar icon for easy date picking
3. **Loading Time**: AI generation typically takes 10-30 seconds depending on complexity
4. **Special Requests**: Use this field for budget constraints, accessibility needs, or specific preferences
5. **Error Recovery**: If something fails, use the "Try Again" button to return to the form

## 🔒 Security Notes

- API keys are loaded from environment variables
- CORS is enabled for API endpoints
- Input validation on both client and server side
- Error messages don't expose sensitive information

## 🐛 Troubleshooting

**Port Already in Use**

```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Module Not Found**

```bash
pip install --upgrade -r requirements.txt
```

**Weather API Errors**

- The app works without OPENWEATHER_API_KEY (uses fake data)
- Set the key in .env for real weather data

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [New Relic Python Agent](https://docs.newrelic.com/docs/apm/agents/python-agent/)

## 🎉 Enjoy

Your CLI application is now a beautiful, modern web application! Visit <http://localhost:5000> to start planning trips with AI.
