# AeroPulse Weather Intelligence – Project Documentation

## 1. What This Project Does

**AeroPulse Weather Intelligence** is a state-of-the-art Python web application built with Streamlit. It delivers real-time weather telemetry and 5-day environmental forecasting for cities worldwide using the OpenWeatherMap API, styled in a clean, light-mode glassmorphic dashboard.

When a user searches for a city or selects a quick preset chip:

- Displays **Current Weather Telemetry** — dynamic temperature, feels-like, wind speed, relative humidity, air pressure, cloud coverage, and condition icon.
- Renders an interactive **5-Day Min/Max Temperature Trend Chart** (Bar or Line view with value callouts).
- Visualises a **5-Day Humidity Index Bar Chart**.
- Tracks the **Solar Timeline** (Sunrise, Sunset, and Total Daylight Hours).
- Detects and highlights **Severe Weather Hazards** (rain, snow, storm, fog, etc.).

---

## 2. Technology Stack & Key Libraries

### 2.1 Python 3.9+
- Serves as the core runtime.
- Leverages mature Python packages for data parsing, data manipulation, HTTP communication, plotting, and UI rendering.

### 2.2 Streamlit (`streamlit`)
- Provides the web application structure and widget system.
- Injects custom light-themed CSS (`Outfit` font family, sky blue gradients `#0284C7`, white glass cards `#FFFFFF`, and slate typography `#0F172A`).
- Manages state via `st.session_state` and secret credentials via `st.secrets["API_KEY"]`.

### 2.3 PyOWM (`pyowm`)
- Official Python client library for the OpenWeatherMap API.
- `weather_manager()` handles current conditions (`weather_at_place()`) and 3-hour step forecasts (`forecast_at_place()`).
- High-level alert detection (`will_have_rain()`, `will_have_storm()`, etc.).

### 2.4 Matplotlib (`matplotlib`)
- Generates polished, light-themed date-aware charts for 5-day temperature trends and humidity index.
- Uses `matplotlib.dates` (`mdates`) for formatting timeline x-axes (`%a, %b %d`).

---

## 3. Architecture Overview

```
weather.py
│
├── 1. Custom CSS & Config Setup
│   ├── Page configuration (AeroPulse Weather Intelligence)
│   ├── Light theme styling (Gradients, Glass Cards, Telemetry Badges)
│   └── Secret API Key retrieval (`st.secrets["API_KEY"]`)
│
├── 2. Header & Control Components
│   ├── AeroPulse Brand Banner
│   ├── Popular Quick-City Selection Pills (Hyderabad, Mumbai, London, New York, Tokyo, Paris, Sydney)
│   └── Compact Control Bar (City search text box, °C/°F unit selector, Bar/Line chart toggle)
│
├── 3. Unified Dashboard Telemetry
│   ├── Hero Weather Card & Current Telemetry Metrics (Wind, Humidity, Pressure, Clouds)
│   ├── 5-Day Min/Max Temperature Forecast Chart (Bar / Line)
│   ├── 5-Day Humidity Index Bar Chart
│   └── Astronomy Solar Timeline & Weather Hazards Card
│
└── 4. Error Diagnostics & Fallback Handling
    └── Comprehensive user tips for exact city searches (e.g., `City, CountryCode`)
```
