import streamlit as st

# 1. Page Configuration (Browser Tab Title and Icon)
st.set_page_config(
    page_title="Next Level Baseball",
    page_icon="⚾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Define the Workout Data
# This dictionary holds all the exercises, sets, reps, and video links.
program = {
    "Monday": {
        "focus": "Leg Power & Linear Speed",
        "exercises": [
            {
                "name": "Bodyweight Squat Jumps",
                "sets": "3",
                "reps": "10 reps",
                "video": "https://www.youtube.com/watch?v=XOTO2qWRy9U",
                "why": "Builds explosive power for sprinting and jumping."
            },
            {
                "name": "Alternating Reverse Lunges",
                "sets": "3",
                "reps": "12 reps (each leg)",
                "video": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmFuaDVtY3hyajd3NHdqY2xpa2twYmQ3a3M5bGs4Y3M5Zmg2ZTd4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUA7aKLaNYyiHljyeY/giphy.gif",
                "why": "Protects knees while building single-leg stability needed for throwing."
            },
            {
                "name": "Single-Leg Glute Bridges",
                "sets": "3",
                "reps": "12 reps (each leg)",
                "video": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzg0bTBjY2didmx0aHZyeG80NTdocmRrNTR0bDRmZms0Y2VtMTFybyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SJWtWnRFsTiNVSECVP/giphy.gif",
                "why": "Strengthens hamstrings to prevent injury and improves running mechanics."
            },
            {
                "name": "10-Yard Sprints (or High Knees)",
                "sets": "5",
                "reps": "10 yards (or 15s in place)",
                "video": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTk0YTVhaGIyOW56ZzRlenJuc25sdW9nZWkxNHp4MjZybTZhbHF0eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/J8sWMdmYJxtGIPM4d3/giphy.gif",
                "why": "Teaches explosive first-step acceleration."
            },
            {
                "name": "Bear Plank to Push-Up",
                "sets": "3",
                "reps": "30 seconds",
                "video": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZG9vYWI3emY4NmM3YWtmcG9mdDR5NXUyYXJncnZxcWlqZW92M2NiNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kF5qEWbthUjQUeXPYi/giphy.gif",
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

# 3. Sidebar Navigation
st.sidebar.title("⚾ Training Menu")
page = st.sidebar.radio("Go to:", ["Home", "Monday", "Wednesday", "Friday"])

st.sidebar.markdown("---")
st.sidebar.info("**Coach's Tip:** consistency is key. Don't skip the warm-up!")

# 4. Main App Logic
if page == "Home":
    st.title("Next Level Baseball ⚾")
    st.subheader("12-Week Bodyweight Regimen")
    st.image("https://images.unsplash.com/photo-1594470117722-de4b9a02ebed?auto=format&fit=crop&q=80&w=1000", caption="Train Hard, Play Hard")
    
    st.markdown("""
    Welcome to the team. This program is designed to build:
    * **Speed:** Linear and lateral explosiveness.
    * **Strength:** Core and limb stability.
    * **Durability:** Protecting your throwing arm and knees.
    
    **Instructions:**
    1.  Select your workout day from the sidebar (top left on mobile).
    2.  Watch the videos for proper form.
    3.  Complete every rep.
    """)

else:
    # Get the data for the selected day
    day_data = program[page]
    
    st.title(f"{page} Workout")
    st.subheader(f"Focus: {day_data['focus']}")
    st.markdown("---")

    # Loop through exercises and display them
    for i, ex in enumerate(day_data['exercises'], 1):
        # Container for each exercise card
        with st.container():
            st.markdown(f"### {i}. {ex['name']}")
            
            # Columns for Sets and Reps
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Sets", value=ex['sets'])
            with col2:
                st.metric(label="Reps", value=ex['reps'])
            
            # Video Embed
            st.video(ex['video'])
            
            # Coach's Note Expander
            with st.expander(f"💡 Why do we do this?"):
                st.write(ex['why'])
            
            st.divider()

    # Completion Button
    if st.button(f"Mark {page} Complete ✅"):
        st.balloons()
        st.success("Workout Recorded! Great job today.")