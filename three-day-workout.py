import streamlit as st
import streamlit.components.v1 as components
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- APP ICON CONFIGURATION ---
ICON_FILENAME = "app_icon.png" 
GITHUB_USER = "matthewusmith" 
REPO_NAME = "baseball-workout-app"
BRANCH = "main"
APP_ICON_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_FILENAME}?v=2"

# 1. Page Configuration
st.set_page_config(
    page_title="12-Week Strength & Agility",
    page_icon=APP_ICON_URL,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Tabs & UI
st.markdown("""
    <style>
        /* GLOBAL VARIABLES */
        :root {
            --primary-color: #0066cc;
        }

        /* REDUCE TOP PADDING */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }

        /* MAIN HEADER STYLING */
        .main-header {
            text-align: center;
            font-size: 24px;
            font-weight: 800;
            margin-top: 0px; 
            margin-bottom: 10px;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* --- STICKY TABS NAVIGATION --- */
        /* Force the tab container to stick to the top */
        .stTabs {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: white;
            padding-top: 10px;
            padding-bottom: 10px;
        }

        /* Style individual tabs to look like buttons */
        div[data-baseweb="tab-list"] {
            gap: 4px;
            background-color: transparent;
        }

        div[data-baseweb="tab"] {
            flex-grow: 1; /* EXPAND TO FILL WIDTH EQUALLY */
            text-align: center;
            padding: 8px 2px;
            border-radius: 5px;
            background-color: #f0f2f6;
            color: #31333F;
            font-size: 14px;
            font-weight: 600;
            border: 1px solid #e0e0e0;
        }

        /* Active Tab Styling */
        div[data-baseweb="tab"][aria-selected="true"] {
            background-color: #0066cc !important;
            color: white !important;
            border: 1px solid #0066cc !important;
        }
        
        /* Hide the default highlight bar below tabs */
        div[data-baseweb="tab-highlight"] {
            display: none;
        }

        /* --- BIGGER STATS BOX --- */
        .stats-box {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            font-size: 16px;
            font-weight: 500;
        }
        
        /* --- BURNOUT EXPANDER --- */
        div[data-testid="stExpander"] details summary p {
            font-size: 1.1rem;
            font-weight: 800;
            color: #d9534f;
            text-align: center;
            width: 100%;
        }
        
        /* --- CONTACT STYLES --- */
        .contact-header {
            color: #0066cc;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .contact-info {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #0066cc;
        }
        
        /* --- FOOTER --- */
        .footer-container {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            opacity: 0.8;
        }
    </style>
""", unsafe_allow_html=True)

# Helper Functions
def get_youtube_embed(video_url):
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    else:
        return None
    embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=1"
    return f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <iframe src="{embed_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>
    """

# Google Sheets Auth
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
def get_gspread_client():
    try:
        if "gcp_service_account" not in st.secrets:
            creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        else:
            secret_value = st.secrets["gcp_service_account"]
            creds_dict = json.loads(secret_value) if isinstance(secret_value, str) else secret_value
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception:
        return None

def submit_feedback(page_name, rating, comment):
    try:
        client = get_gspread_client()
        if not client: return False
        sheet = client.open("baseball-app-feedback").sheet1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, page_name, rating, comment])
        return True
    except Exception:
        return False

@st.cache_data(ttl=600)
def load_program_from_sheets():
    # Skeleton
    data = {k: {"focus": "", "audio_opening": "", "exercises": [], "burnout": None} 
            for k in ["Mon", "Wed", "Fri", "Stretch"]}
            
    # Add static details
    data["Mon"].update({"focus": "Leg Power & Linear Speed", "audio_opening": "monday_opening.mp3"})
    data["Wed"].update({"focus": "Upper Body Strength & Rotation", "audio_opening": "wednesday_opening.mp3"})
    data["Fri"].update({"focus": "Agility & Conditioning", "audio_opening": "friday_opening.mp3"})
    data["Stretch"].update({"focus": "Arm Care & Recovery", "audio_opening": "stretching_opening.mp3"})

    try:
        client = get_gspread_client()
        if not client: return data
        sheet = client.open("baseball-app-feedback").worksheet("Library")
        records = sheet.get_all_records()
        for row in records:
            day_key = row.get("Day")
            if day_key not in data: continue
            
            ex_obj = {
                "name": row.get("Exercise"),
                "sets": str(row.get("Sets")),
                "reps": str(row.get("Reps")),
                "video": row.get("Video"),
                "why": row.get("Note")
            }
            if str(row.get("Burnout")).upper() == "TRUE":
                data[day_key]["burnout"] = ex_obj
            else:
                data[day_key]["exercises"].append(ex_obj)
        return data
    except Exception:
        return data

# --- MAIN APP LAYOUT ---
BASE_AUDIO_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/audio"
program = load_program_from_sheets()

st.markdown('<div class="main-header">12-Week Strength & Agility Program</div>', unsafe_allow_html=True)

# TABS NAVIGATION
tab_home, tab_mon, tab_wed, tab_fri, tab_str, tab_con = st.tabs(["Home", "Mon", "Wed", "Fri", "Stretch", "Contact"])

# --- HELPER TO RENDER A WORKOUT PAGE ---
def render_workout_page(day_key, title):
    day_data = program[day_key]
    
    # Header
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px;'>{title}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: #555; margin-bottom: 25px;'>Focus: {day_data['focus']}</p>", unsafe_allow_html=True)

    # Audio
    opening_url = f"{BASE_AUDIO_URL}/{day_data['audio_opening']}"
    
    # Timer HTML
    timer_html = """
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; text-align: center; font-family: sans-serif;">
        <h4 style="margin: 0 0 5px 0; color: #333; font-size: 14px;">⏱️ Warm-Up Timer</h4>
        <div id="timer-display" style="font-size: 22px; font-weight: bold; color: #0066cc; margin-bottom: 5px;">06:00</div>
        <button onclick="startTimer()" style="background-color: #0066cc; color: white; border: none; padding: 4px 10px; border-radius: 4px; font-size: 12px; cursor: pointer;">Start</button>
        <button onclick="resetTimer()" style="background-color: #f0f0f0; color: #333; border: 1px solid #ccc; padding: 4px 10px; border-radius: 4px; font-size: 12px; cursor: pointer;">Reset</button>
        <audio id="timer-beep"><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        var timeLeft = 360; var timerId = null; var display = document.getElementById("timer-display"); var beep = document.getElementById("timer-beep");
        function formatTime(s) { var m = Math.floor(s / 60); var sc = s % 60; return (m < 10 ? "0"+m : m) + ":" + (sc < 10 ? "0"+sc : sc); }
        function startTimer() { if(timerId) return; timerId = setInterval(function() { timeLeft--; display.innerHTML = formatTime(timeLeft); if(timeLeft > 0 && timeLeft % 30 === 0) { beep.pause(); beep.currentTime = 0; beep.play(); } if(timeLeft <= 0) { clearInterval(timerId); timerId = null; display.innerHTML = "00:00"; display.style.color = "red"; beep.play(); } }, 1000); }
        function resetTimer() { clearInterval(timerId); timerId = null; timeLeft = 360; display.innerHTML = "06:00"; display.style.color = "#0066cc"; }
    </script>
    """

    # Audio HTML
    audio_html = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Coach D's Audio Corner</p>
        <audio controls style="width: 100%;"><source src="{opening_url}" type="audio/mp3"></audio>
    </div>
    """
    
    components.html(audio_html, height=160)

    # Show Warmup if NOT stretch
    if day_key != "Stretch":
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown("**🔥 Dynamic Warm-Up (2 Rounds)**\n* Jumping Jacks (30s)\n* Arm Circles (30s)\n* High Knees (30s)\n* Butt Kicks (30s)\n* Torso Twists (30s)\n* Leg Swings (30s)")
        with c2:
            components.html(timer_html, height=140)

    # Exercises
    for i, ex in enumerate(day_data['exercises'], 1):
        with st.container():
            st.markdown(f"#### {i}. {ex['name']}")
            st.markdown(f"""<div class="stats-box"><div><strong>Sets:</strong> {ex['sets']}</div><div><strong>Reps:</strong> {ex['reps']}</div></div>""", unsafe_allow_html=True)
            vh = get_youtube_embed(ex['video'])
            if vh: st.markdown(vh, unsafe_allow_html=True)
            else: st.video(ex['video'])
            st.info(f"**💡 Coach's Note:** {ex['why']}")
            st.divider()

    # Burnout
    if day_data['burnout']:
        with st.expander("🔥 OPTIONAL: THE BURNOUT ROUND", expanded=False):
            st.error("⚠️ Warning: This section is for those who want to empty the tank. Proceed with caution!")
            bo = day_data['burnout']
            st.markdown(f"<h2 style='text-align: center; font-weight: 900;'>{bo['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"**Target:** {bo['reps']}")
            vh = get_youtube_embed(bo['video'])
            if vh: st.markdown(vh, unsafe_allow_html=True)
            else: st.video(bo['video'])
            st.write(f"**Why:** {bo['why']}")
            st.markdown("---")

    # Feedback
    st.subheader("📝 Rate this Session")
    with st.form(key=f"fb_{day_key}"):
        st.write("How was the intensity today?")
        rate = st.select_slider("Difficulty", options=["Too Easy", "Just Right", "Too Hard"], value="Just Right", label_visibility="collapsed")
        comm = st.text_area("Notes?", placeholder="Shoulder felt good...")
        if st.form_submit_button("Submit Feedback"):
            if submit_feedback(day_key, rate, comm): st.success("Feedback sent!")
            else: st.error("Connection failed.")
    
    if st.button(f"Mark {title} Complete ✅"):
        st.balloons()

# --- TAB CONTENTS ---
with tab_home:
    st.image("https://images.unsplash.com/photo-1680120846170-cb4bc948c797?q=80&w=1000&auto=format&fit=crop")
    
    # Intro Audio
    opening_url = f"{BASE_AUDIO_URL}/home_intro.mp3"
    intro_html = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Listen: Program Intro</p>
        <audio id="intro_player" controls style="width: 100%;"><source src="{opening_url}" type="audio/mp3"></audio>
        <script>var p = document.getElementById("intro_player"); p.play().catch(e => console.log("Autoplay blocked"));</script>
    </div>
    """
    components.html(intro_html, height=160)
    
    st.markdown("""
    Welcome to Coach D's 12-week program. This program is designed to build:
    * **Speed:** Linear and lateral explosiveness.
    * **Strength:** Core and limb stability.
    * **Durability:** Protecting your throwing arm and knees.
    
    **Instructions:**
    1.  Select your workout day from the menu above.
    2.  Watch the videos for proper form.
    3.  Complete every rep.
    """)
    
    st.markdown("""<div class="footer-container"><p>Powered by</p><a href="https://revealbetter.com" target="_blank"><img src="https://raw.githubusercontent.com/matthewusmith/baseball-workout-app/refs/heads/main/Reveal%20Logo%20(6).png" style="width: 150px;"></a></div>""", unsafe_allow_html=True)

with tab_mon:
    render_workout_page("Mon", "Monday Workout")

with tab_wed:
    render_workout_page("Wed", "Wednesday Workout")

with tab_fri:
    render_workout_page("Fri", "Friday Workout")

with tab_str:
    render_workout_page("Stretch", "Post-workout Stretching")

with tab_con:
    st.title("Contact Reveal")
    video_url = "https://www.youtube.com/watch?v=KKjuRJh_3LY&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=20"
    vh = get_youtube_embed(video_url)
    if vh: st.markdown(vh, unsafe_allow_html=True)
    else: st.video(video_url)
    
    st.markdown("""
    <div class="contact-header">About Reveal</div>
    <p>At Reveal, we believe every athlete has another level they haven't unlocked yet.</p>
    <div class="contact-header">Our Services</div>
    <ul><li>Personalized Coaching</li><li>Strength & Agility Programs</li><li>Remote Programming</li><li>Team Clinics</li></ul>
    <div class="contact-info">
        <div style="font-weight: bold; font-size: 18px;">Reveal, LLC</div>
        <p>📍 6800 Wisconsin Avenue<br>Chevy Chase, Maryland 20815</p>
        <p>📧 <a href="mailto:info@revealbetter.com">info@revealbetter.com</a></p>
        <p>📞 <a href="tel:2027687648">(202) 768-7648</a></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div class="footer-container"><a href="https://revealbetter.com" target="_blank"><img src="https://raw.githubusercontent.com/matthewusmith/baseball-workout-app/refs/heads/main/Reveal%20Logo%20(6).png" style="width: 150px;"></a></div>""", unsafe_allow_html=True)
