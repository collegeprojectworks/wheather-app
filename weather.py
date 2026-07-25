from datetime import datetime, timezone
import requests
import streamlit as st
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

# Streamlit Page Config
st.set_page_config(
    page_title="AeroPulse Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header Container */
    .brand-header {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #1D4ED8 100%);
        padding: 24px 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
        margin-top: 4px;
        font-weight: 300;
    }
    
    /* Hero Temperature Display */
    .hero-weather-box {
        background: linear-gradient(135deg, #E0F2FE 0%, #EFF6FF 100%);
        border: 1px solid #BAE6FD;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.8);
    }
    .hero-temp {
        font-size: 3.8rem;
        font-weight: 700;
        color: #0369A1;
        line-height: 1;
        margin: 12px 0 4px 0;
    }
    .hero-feels {
        font-size: 1.1rem;
        color: #0284C7;
        font-weight: 500;
    }
    .status-badge {
        display: inline-block;
        background: #0284C7;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: capitalize;
        margin-top: 8px;
    }
    
    /* Telemetry Cards */
    .telemetry-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .telemetry-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }
    .telemetry-icon {
        font-size: 1.8rem;
        margin-bottom: 4px;
    }
    .telemetry-val {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
    }
    .telemetry-label {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Astronomy Card */
    .astro-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 1px solid #FDE68A;
        border-radius: 16px;
        padding: 18px;
        color: #78350F;
    }
    
    /* Alert Card */
    .alert-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #BBF7D0;
        border-radius: 16px;
        padding: 18px;
        color: #14532D;
    }
    .alert-card.has-alert {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-color: #FCA5A5;
        color: #7F1D1D;
    }

    .stButton button {
        border-radius: 12px !important;
        background-color: #0284C7 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        height: 48px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
    }
    .stButton button:hover {
        background-color: #0369A1 !important;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.35) !important;
    }
</style>
""", unsafe_allow_html=True)

# Fetch secret API Key
api_key = st.secrets["API_KEY"]
sign = u"\N{DEGREE SIGN}"

# --- HEADER BRANDING ---
st.markdown("""
<div class="brand-header">
    <div>
        <div class="brand-title">🌤️ AeroPulse Weather Intelligence</div>
        <div class="brand-subtitle">Universal Telemetry for Every Village, City, District & Country Worldwide</div>
    </div>
    <div style="text-align: right; font-size: 0.9rem; opacity: 0.9;">
        Live Data • OpenWeather API
    </div>
</div>
""", unsafe_allow_html=True)

# --- SINGLE UNIVERSAL SEARCH BAR & BUTTON ---
st.markdown("##### 🌍 Search Any Location Worldwide (City, Village, District, State or PIN Code)")

search_col1, search_col2 = st.columns([4.2, 1])

with search_col1:
    search_query_input = st.text_input(
        "Search Location",
        value=st.session_state.get("location", "Hyderabad"),
        placeholder="Enter any village, town, district, city or PIN code (e.g. Hyderabad, Suryapet, London, 500001)...",
        label_visibility="collapsed"
    )

with search_col2:
    search_clicked = st.button("🔍 Search Location", use_container_width=True)

# Quick Preset Chips for convenience
st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
quick_cols = st.columns(8)
popular_destinations = ["Hyderabad", "Mumbai", "Delhi", "London", "New York", "Tokyo", "Paris", "Sydney"]

for i, dest in enumerate(popular_destinations):
    if quick_cols[i].button(dest, key=f"btn_{dest}"):
        st.session_state["location"] = dest
        search_query_input = dest

# Target location handling
target_location = search_query_input.strip() if search_query_input else "Hyderabad"
st.session_state["location"] = target_location

# --- COMPACT UNIT & GRAPH OPTIONS BAR ---
st.markdown("<br>", unsafe_allow_html=True)
opt_col1, opt_col2, opt_col3 = st.columns([1.5, 1.5, 3])

with opt_col1:
    units = st.selectbox("Temperature Unit", ('celsius', 'fahrenheit'), index=0)

with opt_col2:
    graph = st.selectbox("Forecast Graph Style", ('Bar Graph', 'Line Graph'), index=0)

degree = 'C' if units == 'celsius' else 'F'
unit_param = 'metric' if units == 'celsius' else 'imperial'

# --- OPENWEATHER REST API RESOLVER (NO PKG_RESOURCES DEPENDENCY) ---
def fetch_weather_rest(query, unit_setting):
    query = query.strip()
    if not query:
        raise ValueError("Please enter a location name or PIN code.")

    r_curr = None
    r_fc = None

    # Step 1: Try ZIP Code Lookup first if the query is a number
    if query.isdigit():
        # Specifically try Indian 6-digit PIN codes first
        if len(query) == 6:
            try:
                curr_res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={query},IN&appid={api_key}&units={unit_setting}", timeout=8).json()
                if curr_res.get("cod") == 200:
                    fc_res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?zip={query},IN&appid={api_key}&units={unit_setting}", timeout=8).json()
                    if fc_res.get("cod") == "200":
                        r_curr = curr_res
                        r_fc = fc_res
            except Exception:
                pass
        
        # Fallback to generic ZIP lookup
        if not r_curr or not r_fc:
            try:
                curr_res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={query}&appid={api_key}&units={unit_setting}", timeout=8).json()
                if curr_res.get("cod") == 200:
                    fc_res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?zip={query}&appid={api_key}&units={unit_setting}", timeout=8).json()
                    if fc_res.get("cod") == "200":
                        r_curr = curr_res
                        r_fc = fc_res
            except Exception:
                pass

    # Step 2: Try Place Searches if ZIP lookup failed or it's not a digit
    if not r_curr or not r_fc:
        attempts = [query, query.title()]
        if "," not in query:
            attempts.extend([f"{query},IN", f"{query.title()},IN"])

        for q in attempts:
            try:
                curr_res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={unit_setting}", timeout=8).json()
                if curr_res.get("cod") == 200:
                    fc_res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={q}&appid={api_key}&units={unit_setting}", timeout=8).json()
                    if fc_res.get("cod") == "200":
                        r_curr = curr_res
                        r_fc = fc_res
                        break
            except Exception:
                continue

    if not r_curr or not r_fc:
        raise ValueError(
            f"Could not find weather data for '{query}'.\n\n"
            "**Search Tips:**\n"
            "• **Cities & Villages in India:** Type city/village name e.g. `Hyderabad`, `Suryapet`, `Bhimavaram`, `Warangal`.\n"
            "• **Indian PIN Codes:** Type 6-digit PIN e.g. `500001`, `522002`.\n"
            "• **Global Cities:** Add country code e.g. `London, GB`, `Tokyo, JP`, `Paris, FR`.\n"
        )

    # Process 5-day forecast temperature
    forecast_list = r_fc.get("list", [])
    days_list = []
    dates_list = []
    temp_min = []
    temp_max = []
    humidity_days = []
    h_dates = []
    humidity_max = []

    for item in forecast_list:
        dt_timestamp = item.get("dt")
        day = datetime.fromtimestamp(dt_timestamp, tz=timezone.utc)
        date = day.date()

        # Temp min/max
        if date not in dates_list:
            dates_list.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days_list.append(date)

        t_val = item.get("main", {}).get("temp")
        if temp_min[-1] is None or t_val < temp_min[-1]:
            temp_min[-1] = t_val
        if temp_max[-1] is None or t_val > temp_max[-1]:
            temp_max[-1] = t_val

        # Humidity max
        if date not in h_dates:
            h_dates.append(date)
            humidity_max.append(None)
            humidity_days.append(date)

        h_val = item.get("main", {}).get("humidity")
        if humidity_max[-1] is None or h_val > humidity_max[-1]:
            humidity_max[-1] = h_val

    return r_curr, r_fc, days_list, temp_min, temp_max, humidity_days, humidity_max

# --- MAIN DASHBOARD DISPLAY ---
if not target_location:
    st.info("💡 Enter a city, village, district, or PIN code above and click Search Location.")
else:
    try:
        r_curr, r_fc, days, temp_min, temp_max, h_days, humidity_max = fetch_weather_rest(target_location, unit_param)

        weather_icon_code = r_curr["weather"][0]["icon"]
        icon = f"https://openweathermap.org/img/wn/{weather_icon_code}@4x.png"
        status_desc = r_curr["weather"][0]["description"].title()

        temp = r_curr["main"]["temp"]
        temp_felt = r_curr["main"]["feels_like"]
        cloud = r_curr["clouds"]["all"]
        wind = r_curr["wind"]["speed"]
        humidity = r_curr["main"]["humidity"]
        pressure = r_curr["main"]["pressure"]
        visibility = round(r_curr.get("visibility", 10000) / 1000, 1)

        city_display_name = r_curr.get("name", target_location.title())

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown(f"### 📍 Weather Intelligence for **{city_display_name}**")

        # --- SECTION 1: HERO OVERVIEW & TELEMETRY CARDS ---
        hero_col, telem_col = st.columns([1.2, 2.8])

        with hero_col:
            st.markdown(f"""
            <div class="hero-weather-box">
                <img src="{icon}" width="100" style="margin-bottom: -10px;">
                <div class="hero-temp">{round(temp)}{sign}{degree}</div>
                <div class="hero-feels">Feels like {round(temp_felt)}{sign}{degree}</div>
                <div class="status-badge">{status_desc}</div>
            </div>
            """, unsafe_allow_html=True)

        with telem_col:
            m_col1, m_col2 = st.columns(2)
            m_col3, m_col4 = st.columns(2)

            with m_col1:
                st.markdown(f"""
                <div class="telemetry-card">
                    <div class="telemetry-icon">💨</div>
                    <div class="telemetry-val">{wind} m/s</div>
                    <div class="telemetry-label">Wind Speed</div>
                </div>
                """, unsafe_allow_html=True)

            with m_col2:
                st.markdown(f"""
                <div class="telemetry-card">
                    <div class="telemetry-icon">💧</div>
                    <div class="telemetry-val">{humidity}%</div>
                    <div class="telemetry-label">Relative Humidity</div>
                </div>
                """, unsafe_allow_html=True)

            with m_col3:
                st.markdown(f"""
                <div class="telemetry-card">
                    <div class="telemetry-icon">⏲️</div>
                    <div class="telemetry-val">{pressure} hPa</div>
                    <div class="telemetry-label">Air Pressure</div>
                </div>
                """, unsafe_allow_html=True)

            with m_col4:
                st.markdown(f"""
                <div class="telemetry-card">
                    <div class="telemetry-icon">☁️</div>
                    <div class="telemetry-val">{cloud}%</div>
                    <div class="telemetry-label">Cloud Coverage</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- SECTION 2: 5-DAY TEMPERATURE TREND CHART ---
        st.markdown("### 📈 5-Day Temperature Forecast")
        
        days_num = mdates.date2num(days)

        fig, ax = plt.subplots(figsize=(10, 3.8), facecolor='white')
        ax.set_facecolor('#F8FAFC')
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %b %d'))
        ax.set_xticks(days_num)
        
        if graph == 'Bar Graph':
            bar_w = 0.25
            bar_min = ax.bar(days_num - bar_w/2, temp_min, width=bar_w, color='#38BDF8', label=f'Min Temp ({sign}{degree})', edgecolor='#0284C7', linewidth=1)
            bar_max = ax.bar(days_num + bar_w/2, temp_max, width=bar_w, color='#F43F5E', label=f'Max Temp ({sign}{degree})', edgecolor='#E11D48', linewidth=1)
            
            for bar in bar_min:
                h = bar.get_height()
                if h is not None:
                    ax.annotate(f'{int(h)}{sign}', (bar.get_x() + bar.get_width()/2, h),
                                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0369A1')
            for bar in bar_max:
                h = bar.get_height()
                if h is not None:
                    ax.annotate(f'{int(h)}{sign}', (bar.get_x() + bar.get_width()/2, h),
                                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#BE123C')
        else:
            ax.plot(days_num, temp_min, label=f'Min Temp ({sign}{degree})', color='#0284C7', marker='o', linewidth=2.5, markersize=7)
            ax.plot(days_num, temp_max, label=f'Max Temp ({sign}{degree})', color='#E11D48', marker='s', linewidth=2.5, markersize=7)
            ax.fill_between(days_num, temp_min, temp_max, color='#38BDF8', alpha=0.15)
            
            for d, mn, mx in zip(days_num, temp_min, temp_max):
                if mn is not None:
                    ax.annotate(f'{int(mn)}{sign}', (d, mn), xytext=(0, -12), textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#0369A1')
                if mx is not None:
                    ax.annotate(f'{int(mx)}{sign}', (d, mx), xytext=(0, 6), textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#BE123C')

        ax.set_ylabel(f'Temperature ({sign}{degree})', fontsize=10, fontweight='bold', color='#334155')
        ax.tick_params(axis='both', colors='#475569', labelsize=9)
        ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
        ax.legend(frameon=True, facecolor='white', edgecolor='#E2E8F0', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- SECTION 3: HUMIDITY CHART & ASTRONOMY/ALERTS ---
        bot_col1, bot_col2 = st.columns([1.5, 1])

        with bot_col1:
            st.markdown("### 💧 5-Day Humidity Telemetry")
            h_days_num = mdates.date2num(h_days)

            fig_h, ax_h = plt.subplots(figsize=(7, 3.5), facecolor='white')
            ax_h.set_facecolor('#F8FAFC')
            ax_h.xaxis.set_major_formatter(mdates.DateFormatter('%a, %b %d'))
            ax_h.set_xticks(h_days_num)

            bars_h = ax_h.bar(h_days_num, humidity_max, width=0.4, color='#0ea5e9', edgecolor='#0284c7', linewidth=1)
            for bar in bars_h:
                h = bar.get_height()
                if h is not None:
                    ax_h.annotate(f'{int(h)}%', (bar.get_x() + bar.get_width()/2, h),
                                  xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0369A1')

            ax_h.set_ylabel('Humidity (%)', fontsize=10, fontweight='bold', color='#334155')
            ax_h.tick_params(axis='both', colors='#475569', labelsize=9)
            ax_h.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
            plt.tight_layout()
            st.pyplot(fig_h)

        with bot_col2:
            st.markdown("### 🌅 Astronomy & Alerts")
            
            # Sunrise & Sunset
            sunrise_ts = r_curr.get("sys", {}).get("sunrise", 0)
            sunset_ts = r_curr.get("sys", {}).get("sunset", 0)

            sunrise_unix = datetime.fromtimestamp(sunrise_ts, tz=timezone.utc)
            sunset_unix = datetime.fromtimestamp(sunset_ts, tz=timezone.utc)
            daylight_duration = sunset_unix - sunrise_unix
            hours, remainder = divmod(daylight_duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            st.markdown(f"""
            <div class="astro-card">
                <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;">☀️ Solar Timeline</div>
                <div>🌅 <b>Sunrise:</b> {sunrise_unix.strftime('%H:%M:%S UTC')}</div>
                <div>🌇 <b>Sunset:</b> {sunset_unix.strftime('%H:%M:%S UTC')}</div>
                <div style="margin-top: 6px; font-size: 0.9rem; opacity: 0.9;">
                    ⏳ <b>Total Daylight:</b> {hours}h {minutes}m
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # Weather Hazards Scan
            active_alerts = []
            fc_list = r_fc.get("list", [])
            for f_item in fc_list:
                for w_obj in f_item.get("weather", []):
                    w_main = w_obj.get("main", "").lower()
                    if "rain" in w_main and "Rain Expected 🌧️" not in active_alerts:
                        active_alerts.append("Rain Expected 🌧️")
                    if "snow" in w_main and "Snow Hazard ❄️" not in active_alerts:
                        active_alerts.append("Snow Hazard ❄️")
                    if "thunderstorm" in w_main and "Storm Alert ⛈️" not in active_alerts:
                        active_alerts.append("Storm Alert ⛈️")
                    if ("fog" in w_main or "mist" in w_main or "haze" in w_main) and "Fog / Reduced Visibility 🌫️" not in active_alerts:
                        active_alerts.append("Fog / Reduced Visibility 🌫️")
                    if "clouds" in w_main and "Cloud Coverage ⛅" not in active_alerts:
                        active_alerts.append("Cloud Coverage ⛅")

            if active_alerts:
                alert_list_html = "".join([f"<li><b>{alt}</b></li>" for alt in active_alerts])
                st.markdown(f"""
                <div class="alert-card has-alert">
                    <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px;">⚠️ Weather Hazards Detected</div>
                    <ul style="margin: 0; padding-left: 20px;">
                        {alert_list_html}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-card">
                    <div style="font-weight: 700; font-size: 1.05rem;">✅ Fair Weather Conditions</div>
                    <div style="font-size: 0.9rem; margin-top: 4px;">No severe weather hazards forecasted for the next 5 days.</div>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ {e}")

st.markdown("<hr style='margin: 30px 0 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>AeroPulse Weather Intelligence • Universal Support for All Villages, Towns, Cities & Countries</div>", unsafe_allow_html=True)
