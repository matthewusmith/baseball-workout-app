import streamlit as st
import streamlit.components.v1 as components
import json

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

        /* MAIN HEADER STYLING */
        .main-header {
            text-align: center;
            font-size: 26px;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 20px;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* --- MODERN STICKY MENU BAR --- */
        div[data-testid="stRadio"] {
            position: sticky;
            top: 15px; 
            z-index: 1000;
            background-color: transparent;
            padding-bottom: 10px;
            /* CENTER ALIGNMENT FIX */
            display: flex;
            justify-content: center;
            width: 100%;
        }

        div[role="radiogroup"] {
            background-color: rgba(128, 128, 128, 0.1);
            padding: 5px;
            border-radius: 15px;
            display: flex;
            flex-wrap: nowrap !important;
            overflow-x: auto;
            justify-content: center;
            margin: 0 auto;
            width: fit-content;
            max-width: 100%;
            gap: 5px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        div[role="radiogroup"] label {
            background-color: transparent;
            border: none;
            border-radius: 10px;
            padding: 8px 15px;
            margin: 0;
            flex-grow: 0;
            text-align: center;
            font-weight: 600;
            font-size: 14px;
            color: var(--text-color);
            transition: all 0.2s ease;
            white-space: nowrap;
            min-width: 60px;
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

# --- AUDIO CONFIGURATION ---
GITHUB_USER = "matthewusmith" 
REPO_NAME = "baseball-workout-app"
BRANCH = "main"
BASE_AUDIO_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/audio"

# 3. Main Header
st.markdown('<div class="main-header">12-Week Strength & Agility Program</div>', unsafe_allow_html=True)

# 4. Top Navigation Menu
page = st.radio(
    "Navigation", 
    ["Home", "Monday", "Wednesday", "Friday"], 
    horizontal=True,
    label_visibility="collapsed"
)

# 5. Define the Workout Data (Removed Tips Lists)
program = {
    "Monday": {
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
        ]
    },
    "Wednesday": {
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
        ]
    },
    "Friday": {
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
        ]
    }
}

# 6. Main App Logic
if page == "Home":
    st.image("https://images.unsplash.com/photo-1680120846170-cb4bc948c797?q=80&w=1000&auto=format&fit=crop", caption="Train Hard, Play Hard")
    
    # --- AUDIO INTRO SECTION (With Autoplay) ---
    opening_url = f"{BASE_AUDIO_URL}/home_intro.mp3"
    
    # We use the same HTML/JS injection as the workout pages to enable autoplay
    html_code = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Listen: Program Intro from Coach D</p>
        <!-- The Audio Element -->
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
        
        // 1. Try to Autoplay
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
    
    # Footer Section with Logo and Link
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
    
    # Centered Page Title
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px;'>{page} Workout</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: #555; margin-bottom: 25px;'>Focus: {day_data['focus']}</p>", unsafe_allow_html=True)
    
    # --- AUDIO COACH SECTION (Opening Only) ---
    
    # 1. Prepare URL
    opening_url = f"{BASE_AUDIO_URL}/{day_data['audio_opening']}"
    
    # 2. Inject HTML/JS for Autoplay (No looping tips)
    # We use st.components.v1.html to create an isolated frame that handles the audio events
    html_code = f"""
    <div style="background-color: #e8f4fd; border-left: 5px solid #0066cc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: sans-serif;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🔊 Coach D's Audio Corner</p>
        <!-- The Audio Element -->
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
        
        // 1. Try to Autoplay the Opening immediately
        // Note: Browsers may block this until user interaction. 
        // We catch the error to show a friendly status.
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
    
    components.html(html_code, height=160)
    
    # Loop through exercises and display them
    for i, ex in enumerate(day_data['exercises'], 1):
        with st.container():
            # Exercise Name
            st.markdown(f"#### {i}. {ex['name']}")
            
            # Sets/Reps Box (Updated with larger font)
            st.markdown(f"""
            <div class="stats-box">
                <div><strong>Sets:</strong> {ex['sets']}</div>
                <div><strong>Reps:</strong> {ex['reps']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Video Embed
            video_html = get_youtube_embed(ex['video'])
            if video_html:
                st.markdown(video_html, unsafe_allow_html=True)
            else:
                st.video(ex['video'])
            
            # Coach's Note
            st.info(f"**💡 Coach's Note:** {ex['why']}")
            
            st.divider()

    # Completion Button
    if st.button(f"Mark {page} Complete ✅"):
        st.balloons()
        st.success("Workout Recorded! Great job today.")
