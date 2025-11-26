import streamlit as st

# 1. Page Configuration (Browser Tab Title and Icon)
st.set_page_config(
    page_title="Next Level Baseball",
    page_icon="⚾",
    layout="centered",
    initial_sidebar_state="collapsed" # Hide sidebar by default since we are using top nav
)

# 2. Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        /* CSS to center the main header */
        .main-header {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        /* Menu Bar Optimization for Mobile */
        div.row-widget.stRadio > div {
            flex-direction: row;
            justify-content: center;
            align-items: center;
            background-color: #f0f2f6;
            padding: 5px;
            border-radius: 10px;
            width: 100%;
            flex-wrap: nowrap; /* Forces buttons to stay on one line */
            overflow-x: auto; /* Adds scroll if screen is EXTREMELY small */
        }
        
        div.row-widget.stRadio > div > label {
            background-color: white;
            padding: 4px 10px; /* Smaller padding */
            border-radius: 5px;
            margin: 0 2px;
            border: 1px solid #ddd;
            font-size: 14px; /* Smaller font for menu items */
            white-space: nowrap; /* Prevents text wrapping inside buttons */
        }

        /* Hide the label "Go to" */
        label.css-1qg05tj {
            display: none;
        }
        
        /* Custom Box for Sets/Reps to ensure they stay side-by-side */
        .stats-box {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            padding: 8px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to create the Youtube Embed code with Autoplay/Loop
def get_youtube_embed(video_url):
    """
    Parses a standard YouTube URL, extracts the ID, and returns
    an HTML iframe with autoplay, mute, and loop enabled.
    """
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    else:
        return None

    embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=1"

    return f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 10px; margin-bottom: 10px;">
        <iframe src="{embed_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>
    """

# 3. Top Navigation Menu
# Centered Header
st.markdown('<div class="main-header">⚾ Next Level Baseball</div>', unsafe_allow_html=True)

page = st.radio(
    "Go to:", 
    ["Home", "Monday", "Wednesday", "Friday"], 
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("---")

# 4. Define the Workout Data
program = {
    "Monday": {
        "focus": "Leg Power & Linear Speed",
        "exercises": [
            {
                "name": "Burpee Broad Jumps",
                "sets": "3",
                "reps": "10 reps",
                "video": "https://www.youtube.com/watch?v=dzZZAuVbkvI",
                "why": "Builds explosive power for sprinting and jumping."
            },
            {
                "name": "Alternating Reverse Lunges",
                "sets": "3",
                "reps": "12 reps (each leg)",
                "video": "https://www.youtube.com/watch?v=OX0fKkaY6_c",
                "why": "Protects knees while building single-leg stability needed for throwing."
            },
            {
                "name": "Dumbbell Straight Leg Jackknives",
                "sets": "3",
                "reps": "12 reps (each leg)",
                "video": "https://www.youtube.com/watch?v=1Q_yf422K1U",
                "why": "Strengthens hamstrings to prevent injury and improves running mechanics."
            },
            {
                "name": "Tuck Jumps",
                "sets": "5",
                "reps": "10 yards (or 15s in place)",
                "video": "https://www.youtube.com/watch?v=5S8i5PMatX0",
                "why": "Teaches explosive first-step acceleration."
            },
            {
                "name": "Box Jumps",
                "sets": "3",
                "reps": "30 seconds",
                "video": "https://www.youtube.com/watch?v=_VxxejUIIXM",
                "why": "Builds core stability while arms are moving—mimics throwing posture."
            }
        ]
    },
    "Wednesday": {
        "focus": "Upper Body Strength & Rotational Control",
        "exercises": [
            {
                "name": "Push-Ups with T-Rotation",
                "sets": "3",
                "reps": "10 reps total",
                "video": "https://www.youtube.com/watch?v=q6g4X23wJQM",
                "why": "Builds pushing strength and thoracic mobility for throwing."
            },
            {
                "name": "Prone Y-T-W (Superman)",
                "sets": "3",
                "reps": "10 reps per letter",
                "video": "https://www.youtube.com/watch?v=2n7bFivHlC0",
                "why": "Bulletproofs the shoulder blades and rotator cuff."
            },
            {
                "name": "Bear Crawls",
                "sets": "3",
                "reps": "30 seconds",
                "video": "https://www.youtube.com/watch?v=t_o7a_Yt0_o",
                "why": "Full body coordination and shoulder stability."
            },
            {
                "name": "Russian Twists",
                "sets": "3",
                "reps": "20 touches total",
                "video": "https://www.youtube.com/watch?v=wkD8rjkodUI",
                "why": "Rotational core power for bat speed."
            },
            {
                "name": "Wall Sits",
                "sets": "3",
                "reps": "45 seconds",
                "video": "https://www.youtube.com/watch?v=-cdph8hv0O0",
                "why": "Leg endurance and mental toughness."
            }
        ]
    },
    "Friday": {
        "focus": "Agility, Lateral Movement & Conditioning",
        "exercises": [
            {
                "name": "Skater Jumps (Lateral Bounds)",
                "sets": "3",
                "reps": "16 reps (8 per side)",
                "video": "https://www.youtube.com/watch?v=4R2K9o-n1cM",
                "why": "Lateral power for fielding range and stealing bases."
            },
            {
                "name": "Burpees (No Push-up)",
                "sets": "3",
                "reps": "10 reps",
                "video": "https://www.youtube.com/watch?v=x0e7wP2i71w",
                "why": "Conditioning and 'get up' speed."
            },
            {
                "name": "Lateral Line Hops",
                "sets": "3",
                "reps": "20 seconds (Max Speed)",
                "video": "https://www.youtube.com/watch?v=Gk6WdXqYg9c",
                "why": "Improves foot speed and ankle stiffness."
            },
            {
                "name": "Dead Bugs",
                "sets": "3",
                "reps": "12 reps",
                "video": "https://www.youtube.com/watch?v=g_BYB0R-4vs",
                "why": "Separates limb movement from core stability."
            },
            {
                "name": "Broad Jumps",
                "sets": "3",
                "reps": "6 jumps (Stick landing)",
                "video": "https://www.youtube.com/watch?v=V-XjIAlF1J8",
                "why": "Full body power. Focus on balance."
            }
        ]
    }
}

# 5. Main App Logic
if page == "Home":
    st.markdown("<h3 style='text-align: center;'>12-Week Bodyweight Regimen</h3>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1594470117722-de4b9a02ebed?auto=format&fit=crop&q=80&w=1000", caption="Train Hard, Play Hard")
    
    st.markdown("""
    Welcome to the team. This program is designed to build:
    * **Speed:** Linear and lateral explosiveness.
    * **Strength:** Core and limb stability.
    * **Durability:** Protecting your throwing arm and knees.
    
    **Instructions:**
    1.  Select your workout day from the menu above.
    2.  Watch the videos for proper form.
    3.  Complete every rep.
    
    **Coach's Tip:** consistency is key. Don't skip the warm-up!
    """)

else:
    # Get the data for the selected day
    day_data = program[page]
    
    # Smaller, centered Header for the page title
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 5px;'>{page} Workout</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: #555;'>Focus: {day_data['focus']}</p>", unsafe_allow_html=True)
    
    # Loop through exercises and display them
    for i, ex in enumerate(day_data['exercises'], 1):
        with st.container():
            # Smaller Header for Exercise Name
            st.markdown(f"#### {i}. {ex['name']}")
            
            # Custom HTML Box for Sets and Reps (Side-by-side on Mobile)
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
            
            # Open Box for Coach's Notes (No clicks needed)
            st.info(f"**💡 Coach's Note:** {ex['why']}")
            
            st.divider()

    # Completion Button
    if st.button(f"Mark {page} Complete ✅"):
        st.balloons()
        st.success("Workout Recorded! Great job today.")
