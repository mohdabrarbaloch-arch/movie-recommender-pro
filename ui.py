import streamlit as st
import requests
import pandas as pd
import os

# --- CONFIG ---
API_KEY = "b52d798c1e6170af94d53316a9fc19aa"

st.set_page_config(page_title="CineWatch Pro", page_icon="🎬", layout="wide")

# --- SESSION STATE FOR THEME ---
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "dark"

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(os.path.join(base_dir, "movies.csv"))

movies_df = load_data()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("<h1 style='color:#E50914;'>CINEWATCH AI</h1>", unsafe_allow_html=True)
    
    # Theme Change Logic
    new_theme = st.selectbox("UI Theme", ["dark", "luxury", "black", "dracula", "night", "coffee"])
    if new_theme != st.session_state.current_theme:
        st.session_state.current_theme = new_theme
        st.rerun() # Theme change hotay hi app reload hogi
        
    st.divider()
    st.markdown("### 🛠 Player Settings")
    server_type = st.selectbox("Switch Server", ["Main Engine", "Alternative", "Cloud Mirror"])

# --- CSS & THEME INJECTION ---
# Is logic se DaisyUI poore page ka color badal degi
st.markdown(f"""
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.4.19/dist/full.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .stApp {{ background: none !important; }}
        iframe {{ border-radius: 15px; background: #000; border: 2px solid #333; }}
        .movie-card {{ transition: transform 0.3s; border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; overflow: hidden; }}
        .movie-card:hover {{ transform: scale(1.05); border-color: #E50914; }}
    </style>
    <div data-theme="{st.session_state.current_theme}" class="min-h-screen bg-base-300 p-4 transition-all duration-500">
""", unsafe_allow_html=True)

# --- HELPER: GET MOVIE DATA ---
@st.cache_data(ttl=3600)
def get_info(name):
    try:
        clean = name.split("(")[0].strip()
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean}"
        data = requests.get(url, timeout=5).json()
        if data.get("results"):
            m = data["results"][0]
            return {
                "id": m["id"], 
                "poster": f"https://image.tmdb.org/t/p/w342{m['poster_path']}" if m.get('poster_path') else "https://via.placeholder.com/342x513", 
                "title": m["title"]
            }
    except: pass
    return {"id": None, "poster": "https://via.placeholder.com/342x513", "title": name}

# --- PLAYER SECTION ---
watch = st.query_params.get("watch")
if watch:
    info = get_info(watch)
    if info['id']:
        st.markdown(f"""
            <div class="bg-base-200 p-4 rounded-3xl mb-8 border-2 border-primary/20 shadow-2xl">
                <div class="flex justify-between items-center mb-4 px-2">
                    <h2 class="text-xl font-bold italic">🍿 Streaming: {info['title']}</h2>
                    <a href="/" target="_self" class="btn btn-sm btn-circle btn-error">✕</a>
                </div>
        """, unsafe_allow_html=True)
        
        # Server selection based on engine
        if server_type == "Main Engine":
            url = f"https://vidsrc.pro/embed/movie/{info['id']}"
        elif server_type == "Alternative":
            url = f"https://vidsrc.cc/v2/embed/movie/{info['id']}"
        else:
            url = f"https://multiembed.mov/?video_id={info['id']}&tmdb=1"
            
        st.components.v1.iframe(url, height=550, scrolling=False)
        st.markdown("</div>", unsafe_allow_html=True)

# --- GALLERY ---
st.markdown("<h2 class='text-2xl font-black mb-6 italic border-l-4 border-error pl-4'>EXPLORE MOVIES</h2>", unsafe_allow_html=True)
cols = st.columns(6)

for idx, row in movies_df.head(24).iterrows():
    with cols[idx % 6]:
        m = get_info(row['title'])
        st.markdown(f"""
            <div class="card bg-base-100 shadow-xl movie-card mb-6">
                <figure><img src="{m['poster']}" class="h-64 w-full object-cover" /></figure>
                <div class="p-3 text-center">
                    <p class="font-bold text-[10px] truncate mb-2">{row['title']}</p>
                    <a href="?watch={row['title']}" target="_self" class="btn btn-primary btn-xs w-full text-white font-bold">PLAY</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)