import streamlit as st
import streamlit.components.v1 as components
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Configuration
st.set_page_config(
    page_title="12-Week Strength & Agility",
    page_icon="⚾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Modern UI & Sticky Menu
st.markdown("""
    <style>
        /* GLOBAL VARIABLES */
        :root {
            --primary-color: #0066cc;
            --bg-color-light: #ffffff;
            --bg-color-dark: #0e1117;
            --text-color-light: #1E1E1E;
            --text-color-dark: #FAFAFA;
        }

        /* REDUCE TOP PADDING */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* MAIN HEADER STYLING */
        .main-header {
            text-align: center;
            font-size: 26px;
            font-weight: 800;
            margin-top: 0px; /* Reduced margin */
            margin-bottom: 20px;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* --- MODERN STICKY MENU BAR --- */
        
        /* 1. Target the main Streamlit Radio container */
        div[data-testid="stRadio"] {
            position: sticky;
            top: 10px; 
            z-index: 1000;
            background-color: transparent;
            padding-bottom: 10px;
            
            /* FORCE CENTER ALIGNMENT */
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }

        /* 2. Style the inner radiogroup (the 'pill' itself) */
        div[role="radiogroup"] {
            background-color: rgba(128, 128, 128, 0.1);
            padding: 5px;
            border-radius: 15px;
            display: flex;
            flex-wrap: nowrap !important;
            overflow-x: auto;
            
            /* Center items inside the pill */
            justify-content: center;
            align-items: center;
            
            /* Center the pill itself */
            margin: 0 auto;
            width: fit-content;
            max-width: 98%; /* Prevent overflow on very small screens */
            
            gap: 5px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        div[role="radiogroup"] label {
            background-color: transparent;
            border: none;
            border-radius: 10px;
            padding: 8px 12px; /* Slightly reduced horizontal padding for better fit */
            margin: 0;
            flex-grow: 0;
            text-align: center;
            font-weight: 600;
            font-size: 14px;
            color: var(--text-color);
            transition: all 0.2s ease;
            white-space: nowrap;
            min-width: 40px; /* reduced min-width */
            display: flex;
            justify-content: center;
            align-items: center;
        }

        div[role="radiogroup"] label:hover {
            background-color: rgba(128, 128, 128, 0.2);
        }

        div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        label[data-testid="stWidgetLabel"] {
            display: none;
        }
        
        /* --- BIGGER STATS BOX --- */
        .stats-box {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            font-size: 18px;
            font-weight: 500;
        }
        
        .stats-box strong {
            font-weight: 700;
            color: #0066cc;
        }

        /* --- AUDIO PLAYER CARD --- */
        .audio-card {
            background-color: #e8f4fd; /* Light blue background */
            border-left: 5px solid #0066cc;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        @media (prefers-color-scheme: dark) {
            .audio-card { background-color: #1e293b; border-left: 5px solid #4da6ff; }
        }

        /* --- FOOTER --- */
        .footer-container {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
            opacity: 0.8;
        }
        .footer-link {
            color: #0066cc;
            text-decoration: none;
            font-weight: bold;
        }
        @media (prefers-color-scheme: dark) {
            .footer-link { color: #4da6ff; }
        }
        
        /* --- CONTACT PAGE STYLES --- */
        .contact-header {
            color: var(--primary-color);
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .contact-info {
            background-color: var(--secondary-background-color);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid var(--primary-color);
        }
        
        /* --- FEEDBACK FORM STYLES --- */
        .stSelectSlider {
            padding-top: 10px;
            padding-bottom: 20px;
        }

        /* --- BURNOUT EXPANDER STYLING --- */
        /* Targets the text inside the expander summary */
        div[data-testid="stExpander"] details summary p {
            font-size: 1.2rem;
            font-weight: 800;
            color: #d9534f; /* Intense Red */
            text-align: center;
            width: 100%;
        }
        
        /* Optional: Center the chevron arrow as well */
        div[data-testid="stExpander"] details summary {
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function for YouTube
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

# --- GOOGLE SHEETS SETUP ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def submit_feedback(page_name, rating, comment):
    """
    Connects to Google Sheets and appends the feedback using Streamlit Secrets.
    Handles both Dictionary and String formats for secrets.
    """
    try:
        if "gcp_service_account" not in st.secrets:
            # Fallback for local testing
            creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        else:
            secret_value = st.secrets["gcp_service_account"]
            if isinstance(secret_value, str):
                creds_dict = json.loads(secret_value)
            else:
                creds_dict = secret_value
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            
        client = gspread.authorize(creds)
        sheet = client.open("baseball-app-feedback").sheet1
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, page_name, rating, comment])
        return True
    except Exception as e:
        return False

# --- AUDIO CONFIGURATION ---
GITHUB_USER = "matthewusmith" 
REPO_NAME = "baseball-workout-app"
BRANCH = "main"
BASE_AUDIO_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/audio"

# 3. Main Header
st.markdown('<div class="main-header">12-Week Strength & Agility Program</div>', unsafe_allow_html=True)

# 4. Main Navigation
page = st.radio(
    "Navigation", 
    ["Home", "Mon", "Wed", "Fri", "Stretch", "Contact"], 
    horizontal=True,
    label_visibility="collapsed"
)

# 5. Define the Workout Data (Added "burnout" key to workouts)
program = {
    "Mon": {
        "focus": "Leg Power & Linear Speed",
        "audio_opening": "monday_opening.mp3",
        "exercises": [
            {
                "name": "Burpee Broad Jumps",
                "sets": "3",
                "reps": "10",
                "video": "https://www.youtube.com/watch?v=dzZZAuVbkvI",
                "why": "Builds explosive power for sprinting and jumping."
            },
            {
                "name": "Alternating Reverse Lunges",
                "sets": "3",
                "reps": "12/leg",
                "video": "https://www.youtube.com/watch?v=OX0fKkaY6_c",
                "why": "Protects knees while building single-leg stability needed for throwing."
            },
            {
                "name": "DB Straight Leg Jackknives",
                "sets": "3",
                "reps": "12/leg",
                "video": "https://www.youtube.com/watch?v=1Q_yf422K1U",
                "why": "Strengthens hamstrings to prevent injury and improves running mechanics."
            },
            {
                "name": "Tuck Jumps",
                "sets": "5",
                "reps": "10 yds",
                "video": "https://www.youtube.com/watch?v=5S8i5PMatX0",
                "why": "Teaches explosive first-step acceleration."
            },
            {
                "name": "Box Jumps",
                "sets": "3",
                "reps": "30 sec",
                "video": "https://www.youtube.com/watch?v=_VxxejUIIXM",
                "why": "Builds core stability while arms are moving—mimics throwing posture."
            }
        ],
        "burnout": {
            "name": "Jump Lunges (Alternating)",
            "reps": "Max Effort (Empty the tank!)",
            "video": "https://www.youtube.com/watch?v=1erexKvIARE",
            "why": "A final push to build lactic threshold and mental toughness."
        }
    },
    "Wed": {
        "focus": "Upper Body Strength & Rotational Control",
        "audio_opening": "wednesday_opening.mp3",
        "exercises": [
            {
                "name": "Push-Ups with T-Rotation",
                "sets": "3",
                "reps": "10 total",
                "video": "https://www.youtube.com/watch?v=q6g4X23wJQM",
                "why": "Builds pushing strength and thoracic mobility for throwing."
            },
            {
                "name": "Prone Y-T-W (Superman)",
                "sets": "3",
                "reps": "10 ea",
                "video": "https://www.youtube.com/watch?v=2n7bFivHlC0",
                "why": "Bulletproofs the shoulder blades and rotator cuff."
            },
            {
                "name": "Bear Crawls",
                "sets": "3",
                "reps": "30 sec",
                "video": "https://www.youtube.com/watch?v=t_o7a_Yt0_o",
                "why": "Full body coordination and shoulder stability."
            },
            {
                "name": "Russian Twists",
                "sets": "3",
                "reps": "20 total",
                "video": "https://www.youtube.com/watch?v=wkD8rjkodUI",
                "why": "Rotational core power for bat speed."
            },
            {
                "name": "Wall Sits",
                "sets": "3",
                "reps": "45 sec",
                "video": "https://www.youtube.com/watch?v=-cdph8hv0O0",
                "why": "Leg endurance and mental toughness."
            }
        ],
        "burnout": {
            "name": "Diamond Push-Ups",
            "reps": "1 Set: To Failure",
            "video": "https://www.youtube.com/watch?v=J0DnG1_S92I",
            "why": "Blast the triceps for throwing velocity."
        }
    },
    "Fri": {
        "focus": "Agility, Lateral Movement & Conditioning",
        "audio_opening": "friday_opening.mp3",
        "exercises": [
            {
                "name": "Skater Jumps (Lateral)",
                "sets": "3",
                "reps": "16 total",
                "video": "https://www.youtube.com/watch?v=4R2K9o-n1cM",
                "why": "Lateral power for fielding range and stealing bases."
            },
            {
                "name": "Burpees (No Push-up)",
                "sets": "3",
                "reps": "10",
                "video": "https://www.youtube.com/watch?v=x0e7wP2i71w",
                "why": "Conditioning and 'get up' speed."
            },
            {
                "name": "Lateral Line Hops",
                "sets": "3",
                "reps": "20 sec",
                "video": "https://www.youtube.com/watch?v=Gk6WdXqYg9c",
                "why": "Improves foot speed and ankle stiffness."
            },
            {
                "name": "Dead Bugs",
                "sets": "3",
                "reps": "12",
                "video": "https://www.youtube.com/watch?v=g_BYB0R-4vs",
                "why": "Separates limb movement from core stability."
            },
            {
                "name": "Broad Jumps",
                "sets": "3",
                "reps": "6 jumps",
                "video": "https://www.youtube.com/watch?v=V-XjIAlF1J8",
                "why": "Full body power. Focus on balance."
            }
        ],
        "burnout": {
            "name": "Mountain Climbers",
            "reps": "1 Set: 60 Seconds",
            "video": "https://www.youtube.com/watch?v=nmwgirgXLIg",
            "why": "Core stability and cardio burnout."
        }
    },
    "Stretch": {
        "focus": "Arm Care & Hip Mobility",
        "audio_opening": "stretching_opening.mp3",
        "exercises": [
            {
                "name": "Cross-Body Shoulder Stretch",
                "sets": "2",
                "reps": "30 sec/arm",
                "video": "https://www.youtube.com/watch?v=PD3gQO5d9h8",
                "why": "Loosens the posterior shoulder capsule, crucial for throwers."
            },
            {
                "name": "Kneeling Hip Flexor Stretch",
                "sets": "2",
                "reps": "45 sec/leg",
                "video": "https://www.youtube.com/watch?v=YQmpO9VT2X4",
                "why": "Opens tight hips to allow for better rotation when hitting and throwing."
            },
            {
                "name": "Seated T-Spine Twist",
                "sets": "2",
                "reps": "30 sec/side",
                "video": "https://www.youtube.com/watch?v=1f33p89jX7E",
                "why": "Improves thoracic mobility, essential for safe rotation."
            },
            {
                "name": "Wrist & Forearm Stretch",
                "sets": "2",
                "reps": "30 sec/arm",
                "video": "https://www.youtube.com/watch?v=0P9X_X0q0Jg",
                "why": "Prevents elbow strain by keeping the forearm muscles loose."
            },
            {
                "name": "Child's Pose",
                "sets": "2",
                "reps": "60 seconds",
                "video": "https://www.youtube.com/watch?v=2MJGg-dUKh0",
                "why": "Decompresses the spine and relaxes the lats after a long week."
            }
        ]
    }
}

# 6. Main App Logic
if page == "Home":
    st.image("https://images.unsplash.com/photo-1680120846170-cb4bc948c797?q=80&w=1000&auto=format&fit=crop", caption="Train Hard, Play Hard")
    
    # --- AUDIO INTRO SECTION (With Autoplay) ---
    opening_url = f"{BASE_AUDIO_URL}/home_intro.mp3"
    
    html_code = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Listen: Program Intro from Coach D</p>
        <audio id="player" controls style="width: 100%;">
            <source src="{opening_url}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 5px; font-style: italic;">
            Playing Intro...
        </p>
    </div>

    <script>
        var player = document.getElementById("player");
        var statusLabel = document.getElementById("status");
        
        var promise = player.play();
        if (promise !== undefined) {{
            promise.then(_ => {{
                console.log("Autoplay started!");
                statusLabel.innerHTML = "Playing Intro...";
            }}).catch(error => {{
                console.log("Autoplay prevented.");
                statusLabel.innerHTML = "Autoplay blocked by browser. Please press Play to start.";
            }});
        }}

        player.onended = function() {{
            statusLabel.innerHTML = "Intro finished. Let's get to work!";
        }};
    </script>
    """
    components.html(html_code, height=160)
    
    st.markdown("""
    Welcome to Coach D's 12-week program. This program is designed to build:
    * **Speed:** Linear and lateral explosiveness.
    * **Strength:** Core and limb stability.
    * **Durability:** Protecting your throwing arm and knees.
    
    **Instructions:**
    1.  Select your workout day from the menu above.
    2.  Watch the videos for proper form.
    3.  Complete every rep.
    
    **Coach's Tip:** consistency is key. Don't skip a day, don't cheat yourself!  Results guaranteed after 12 weeks.
    """)
    
    # Footer Section
    st.markdown("""
        <div class="footer-container">
            <p>Powered by</p>
            <a href="https://revealbetter.com" target="_blank">
                <img src="https://raw.githubusercontent.com/matthewusmith/baseball-workout-app/refs/heads/main/Reveal%20Logo%20(6).png" alt="Reveal Better Logo" style="width: 150px; border-radius: 5px; margin-bottom: 10px;">
            </a>
            <p style="font-size: 14px;">Unlock your athletic potential with personalized coaching and programs.</p>
            <a class="footer-link" href="https://revealbetter.com" target="_blank">Visit revealbetter.com</a>
        </div>
    """, unsafe_allow_html=True)

elif page == "Contact":
    # --- CONTACT PAGE ---
    st.title("Contact Reveal")
    
    # Placeholder Video for "Learn about Reveal"
    # Using a high-quality baseball training related video as a placeholder since a specific one wasn't provided
    video_url = "https://www.youtube.com/watch?v=KKjuRJh_3LY&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=20"
    
    # Use custom embed function to enable looping and autoplay
    video_html = get_youtube_embed(video_url)
    if video_html:
        st.markdown(video_html, unsafe_allow_html=True)
    else:
        st.video(video_url)
    
    st.markdown("""
    <div class="contact-header">About Reveal</div>
    <p>At Reveal, we believe every athlete has another level they haven't unlocked yet. We combine data-driven training with old-school work ethic to help athletes from 5 to 85 maximize their potential. From youth development and elite performance to entire body wellness, we provide the roadmap; you provide the effort.</p>
    
    <div class="contact-header">Our Services</div>
    <ul>
        <li><strong>Personalized Coaching:</strong> 1-on-1 instruction tailored to your specific mechanical needs and goals.</li>
        <li><strong>Strength & Agility Programs:</strong> Comprehensive gym and field work designed to translate directly to game performance.</li>
        <li><strong>Remote Programming:</strong> Get elite coaching anywhere in the world with our app-based training plans.</li>
        <li><strong>Team Clinics:</strong> Specialized workshops for teams looking to gain a competitive edge.</li>
    </ul>
    
    <div class="contact-info">
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px;">Reveal, LLC</div>
        <p>📍 6800 Wisconsin Avenue<br>Chevy Chase, Maryland 20815<br>United States</p>
        <p>📧 <a href="mailto:info@revealbetter.com">info@revealbetter.com</a></p>
        <p>📞 <a href="tel:2027687648">(202) 768-7648</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer Section (Reused)
    st.markdown("""
        <div class="footer-container">
            <p>Powered by</p>
            <a href="https://revealbetter.com" target="_blank">
                <img src="https://raw.githubusercontent.com/matthewusmith/baseball-workout-app/refs/heads/main/Reveal%20Logo%20(6).png" alt="Reveal Better Logo" style="width: 150px; border-radius: 5px; margin-bottom: 10px;">
            </a>
            <p style="font-size: 14px;">Unlock your athletic potential with personalized coaching and programs.</p>
            <a class="footer-link" href="https://revealbetter.com" target="_blank">Visit revealbetter.com</a>
        </div>
    """, unsafe_allow_html=True)

else:
    # Get the data for the selected day
    day_data = program[page]
    
    # Map short menu names to full titles
    page_titles = {
        "Mon": "Monday Workout",
        "Wed": "Wednesday Workout",
        "Fri": "Friday Workout",
        "Stretch": "Post-workout Stretching"
    }
    title_text = page_titles.get(page, f"{page} Workout")
    
    # Centered Page Title
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px;'>{title_text}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: #555; margin-bottom: 25px;'>Focus: {day_data['focus']}</p>", unsafe_allow_html=True)
    
    # --- AUDIO COACH SECTION ---
    opening_url = f"{BASE_AUDIO_URL}/{day_data['audio_opening']}"
    
    # --- DYNAMIC WARM UP TIMER HTML/JS ---
    # Defines a timer block with Start/Reset buttons and audio element for the buzzer.
    timer_html = """
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 5px; text-align: center; font-family: sans-serif;">
        <h4 style="margin: 0 0 5px 0; color: #333; font-size: 16px;">⏱️ Warm-Up Timer (Intervals)</h4>
        <div id="timer-display" style="font-size: 24px; font-weight: bold; color: #0066cc; margin-bottom: 5px;">06:00</div>
        
        <button onclick="startTimer()" style="background-color: #0066cc; color: white; border: none; padding: 5px 12px; border-radius: 5px; cursor: pointer; font-size: 12px; margin-right: 5px;">Start</button>
        <button onclick="resetTimer()" style="background-color: #f0f0f0; color: #333; border: 1px solid #ccc; padding: 5px 12px; border-radius: 5px; cursor: pointer; font-size: 12px;">Reset</button>

        <audio id="timer-beep">
            <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3">
        </audio>
    </div>

    <script>
        var timeLeft = 360; // 6 minutes in seconds
        var timerId = null;
        var display = document.getElementById("timer-display");
        var beep = document.getElementById("timer-beep");

        function formatTime(seconds) {
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            return (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        }

        function startTimer() {
            if (timerId) return; // Prevent multiple clicks
            
            timerId = setInterval(function() {
                timeLeft--;
                display.innerHTML = formatTime(timeLeft);
                
                // Play sound every 30 seconds (Interval Logic)
                if (timeLeft > 0 && timeLeft % 30 === 0) {
                    beep.pause();
                    beep.currentTime = 0;
                    beep.play();
                }
                
                if (timeLeft <= 0) {
                    clearInterval(timerId);
                    timerId = null;
                    display.innerHTML = "00:00";
                    display.style.color = "red";
                    beep.play();
                }
            }, 1000);
        }

        function resetTimer() {
            clearInterval(timerId);
            timerId = null;
            timeLeft = 360;
            display.innerHTML = "06:00";
            display.style.color = "#0066cc";
        }
    </script>
    """

    # --- MAIN AUDIO PLAYER HTML/JS ---
    audio_player_html = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Coach D's Audio Corner</p>
        <audio id="player" controls style="width: 100%;">
            <source src="{opening_url}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 5px; font-style: italic;">
            Playing Opening...
        </p>
    </div>

    <script>
        var player = document.getElementById("player");
        var statusLabel = document.getElementById("status");
        
        var promise = player.play();
        if (promise !== undefined) {{
            promise.then(_ => {{
                console.log("Autoplay started!");
                statusLabel.innerHTML = "Playing Opening...";
            }}).catch(error => {{
                console.log("Autoplay prevented.");
                statusLabel.innerHTML = "Autoplay blocked by browser. Please press Play to start.";
            }});
        }}

        player.onended = function() {{
            statusLabel.innerHTML = "Opening finished. Good luck with the workout!";
        }};
    </script>
    """
    
    # Render Audio Player first
    components.html(audio_player_html, height=160)
    
    # Only show Dynamic Warm-Up on workout days, NOT on Stretch page
    if page != "Stretch":
        # Columns for Side-by-Side Layout
        w_col1, w_col2 = st.columns([1.5, 1])
        
        with w_col1:
            # Warm Up Instructions
            st.markdown("""
            **🔥 Dynamic Warm-Up (6 Min - 2 Rounds)**
            * **Jumping Jacks** (30s)
            * **Arm Circles** (30s)
            * **High Knees** (30s) 
            * **Butt Kicks** (30s)
            * **Torso Twists** (30s)
            * **Leg Swings** (30s)
            """)

        with w_col2:
            # Render Timer
            components.html(timer_html, height=135)
    
    # Loop through exercises
    for i, ex in enumerate(day_data['exercises'], 1):
        with st.container():
            st.markdown(f"#### {i}. {ex['name']}")
            
            st.markdown(f"""
            <div class="stats-box">
                <div><strong>Sets:</strong> {ex['sets']}</div>
                <div><strong>Reps:</strong> {ex['reps']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            video_html = get_youtube_embed(ex['video'])
            if video_html:
                st.markdown(video_html, unsafe_allow_html=True)
            else:
                st.video(ex['video'])
            
            st.info(f"**💡 Coach's Note:** {ex['why']}")
            st.divider()

    # --- BURNOUT SECTION (Optional) ---
    if "burnout" in day_data:
        # Use an Expander so it's hidden/optional by default
        with st.expander("🔥🔥🔥 OPTIONAL: THE BURNOUT ROUND 🔥🔥🔥", expanded=False):
            # Styling container using st.error for red alert look
            st.error("⚠️ Warning: This section is for those who want to empty the tank. Proceed with caution!")
            
            bo = day_data['burnout']
            st.markdown(f"### {bo['name']}") # Reverted to simple header
            st.markdown(f"**Target:** {bo['reps']}")
            
            # Embed video
            video_html = get_youtube_embed(bo['video'])
            if video_html:
                st.markdown(video_html, unsafe_allow_html=True)
            else:
                st.video(bo['video'])
                
            st.write(f"**Why:** {bo['why']}")
            st.markdown("---")

    # --- FEEDBACK FORM ---
    st.subheader("📝 Rate this Session")
    
    # We use a form so the page doesn't reload on every input change
    with st.form(key=f"feedback_form_{page}"):
        st.write("How was the intensity today?")
        
        # Select Slider for Rating
        rating = st.select_slider(
            "Difficulty Rating",
            options=["Too Easy", "Just Right", "Too Hard"],
            value="Just Right",
            label_visibility="collapsed"
        )
        
        # Text Area for Comments
        comment = st.text_area(
            "Any pain, issues, or notes?", 
            placeholder="Shoulder felt good, burpees were tough..."
        )
        
        # Submit Button
        submit_btn = st.form_submit_button("Submit Feedback")
        
        if submit_btn:
            if submit_feedback(page, rating, comment):
                st.success("Thanks! Feedback sent to Coach D.")
            else:
                st.error("Could not connect to database. Please check your internet connection or API setup.")

    # Mark Complete Button (Visual only)
    if st.button(f"Mark {page} Complete ✅"):
        st.balloons()
        st.success("Workout Recorded! Great job today.")
