import streamlit as st
import pickle
import pandas as pd
import requests
import asyncio
import aiohttp
import bz2

# ---------------- 1. PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"  # Forces the sidebar to stay open explicitly
)

# ---------------- 2. PREMIUM MODERN LIGHT CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Global Styles */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background-color: #fafafa; /* Pure soft minimal light background */
    color: #1a1a1a;
}

.block-container {
    padding-top: 3rem !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
}

/* ================= TOP BAR & LAYOUT CLEANUP ================= */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

div[data-testid="stSidebarHeader"] {
    background-color: #ffffff !important;
    border-bottom: 1px solid #f3f4f6 !important;
}

button[data-testid="stSidebarCollapseButton"] svg {
    color: #4b5563 !important;
    fill: #4b5563 !important;
}

div[data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem !important;
}
/* ============================================================ */

/* Main Dashboard Typography */
h1 {
    text-align: center;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: #111111;
    font-size: 54px;
    margin-bottom: 8px;
    margin-top: 1rem;
}

.subtitle {
    text-align: center;
    color: #666666;
    margin-bottom: 45px;
    font-size: 19px;
    font-weight: 400;
}

/* ================= THE ULTIMATE NO-DOUBLE-BORDER SEARCHBAR FIX ================= */
.stSelectbox label {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #4b5563 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 10px !important;
}

/* 1. Nuke EVERY nested border/glow layer that Streamlit natively creates */
div[data-baseweb="select"], 
div[data-baseweb="select"] *, 
.stSelectbox div {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* 2. Apply exactly ONE custom border wrapper around the actual element box base */
div[data-baseweb="select"] > div:first-child {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 2px 6px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.2s ease-in-out !important;
}

/* 3. Give it a beautiful, single red glow when active without nested overlap */
div[data-baseweb="select"]:focus-within > div:first-child,
div[data-baseweb="select"] > div:first-child:hover {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.08) !important;
}
/* ==================================================================== */

/* Premium Red Interaction Button */
.stButton>button {
    width: 100%;
    background: #e50914 !important; /* Clean Netflix Red Accent */
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    height: 3.4em;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.2);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton>button:hover {
    background: #cc0812 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(229, 9, 20, 0.3);
}

.stButton>button:active {
    transform: translateY(0px);
}

/* Premium Sidebar Formatting - FIXED COLOR PROFILE */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #f3f4f6 !important;
    visibility: visible !important; /* Ensures layout calculations don't drop it */
}

section[data-testid="stSidebar"] h1 {
    font-size: 24px !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    color: #111111 !important;
    text-align: left !important;
    margin-bottom: 20px !important;
    margin-top: 0px !important;
    padding-bottom: 10px;
}

section[data-testid="stSidebar"] .stMarkdown p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] div {
    color: #4b5563 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

section[data-testid="stSidebar"] strong {
    color: #111111 !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    margin-bottom: 16px !important;
}

section[data-testid="stSidebar"] em {
    color: #e50914 !important;
    font-style: normal !important;
    font-weight: 700;
}

/* Modern Movie Card Design - HIGH-END ELEVATION */
.movie-card {
    background: #ffffff !important;
    padding: 0px !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    height: 100% !important;
}

.movie-card:hover {
    transform: translateY(-10px) !important;
    border-color: rgba(0,0,0,0.08) !important;
    box-shadow: 0 30px 60px rgba(0,0,0,0.08) !important;
}

/* Movie Title container padding wrapper */
.movie-card-body {
    padding: 16px !important;
    text-align: left !important;
    background: #ffffff !important;
}

.movie-title {
    color: #111111 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    line-height: 1.4 !important;
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    
    min-height: 42px !important;
    height: auto !important;
}

img {
    border-radius: 0px !important; 
    width: 100% !important;
    aspect-ratio: 2 / 3 !important;
    object-fit: cover !important;
    display: block !important;
}

/* PREMIUM SKELETON LOADER PULSE EFFECT */
@keyframes pulse {
    0% { background-color: #f1f5f9; }
    50% { background-color: #e2e8f0; }
    100% { background-color: #f1f5f9; }
}
.skeleton-card {
    height: 380px;
    border-radius: 20px;
    animation: pulse 1.5s infinite ease-in-out;
    border: 1px solid #e2e8f0;
}

/* Horizontal Divider Fix */
hr {
    border: 0 !important;
    height: 1px !important;
    background: #eeeeee !important;
    margin: 3.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- 3. ASYNC POSTER FETCH ----------------
@st.cache_data(show_spinner=False)
def get_cached_poster_url(movie_id, data):
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

async def fetch_single_poster(session, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75bb0a2989475f038c93c83705ec4467&language=en-US"
    try:
        async with session.get(url, timeout=4) as response:
            if response.status == 200:
                data = await response.json()
                return get_cached_poster_url(movie_id, data)
    except:
        pass
    return "https://via.placeholder.com/500x750?text=Error"

async def fetch_all_posters(movie_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_poster(session, m_id) for m_id in movie_ids]
        return await asyncio.gather(*tasks)


# ---------------- 4. LOAD DATA (MUST RUN BEFORE UI COMPONENTS) ----------------
# @st.cache_data
# def load_data():
#     try:
#         movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
#         movies_df = pd.DataFrame(movies_dict)
#         similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
        
#         if isinstance(similarity_matrix, pd.DataFrame):
#             similarity_matrix = similarity_matrix.values
            
#         return movies_df, similarity_matrix
#     except FileNotFoundError as e:
#         st.error(f"Could not find required files in directory! Error details: {e}")
#         st.stop()

# # Load globally
# movies, similarity = load_data()

@st.cache_data
def load_data():
    try:
        # 1. Load the movies dictionary
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies_df = pd.DataFrame(movies_dict)
        
        # 2. Open and decompress the similarity matrix on the fly
        with bz2.BZ2File('similarity.pbz2', 'rb') as f:
            similarity_matrix = pickle.load(f)
        
        # Safe-guarding matrix format
        if isinstance(similarity_matrix, pd.DataFrame):
            similarity_matrix = similarity_matrix.values
            
        return movies_df, similarity_matrix

    except FileNotFoundError as e:
        st.error(f"Could not find required files in directory! Error details: {e}")
        st.stop()

# CHANGE HERE: Assigned the output directly to 'movies' instead of 'movies_df'
movies, similarity = load_data()


# ---------------- 5. RECOMMEND FUNCTION ----------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    clean_distances = []
    for val in distances:
        try:
            clean_distances.append(float(val))
        except (ValueError, TypeError):
            clean_distances.append(0.0)

    movies_list = sorted(
        list(enumerate(clean_distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movie_ids = []

    for i in movies_list:
        recommended_movie_ids.append(movies.iloc[i[0]].movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        
    recommended_movies_posters = asyncio.run(fetch_all_posters(recommended_movie_ids))
    return recommended_movies, recommended_movies_posters


# ---------------- 6. SIDEBAR ----------------
with st.sidebar:
    st.title("🎬 Navigator")
    st.markdown("""
    🍿 **Movie Recommender**
    
    Not sure what to watch next? This app helps you quickly discover hidden gems based on your mood.
    
    Choose your favorite film from the dropdown, hit the button, and let the algorithm do the work.
    
    ✨ *Sleek. Fast. Intelligent.*
    """)


# ---------------- 7. MAIN DASHBOARD HEADER ----------------
st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Instant cinematic matches tailored for you</div>",
    unsafe_allow_html=True
)


# ---------------- 8. CENTERED SEARCH COMPONENT ----------------
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    selected_movie_name = st.selectbox(
        "Select a movie you love:",
        movies['title'].values
    )
    st.write("")
    button_pressed = st.button("✨ Discover Recommendations")

st.markdown("<hr>", unsafe_allow_html=True)


# ---------------- 9. DISPLAY RECOMMENDATIONS ----------------
if button_pressed:
    placeholder = st.empty()
    
    # Render elegant Light Mode Skeleton Loaders
    with placeholder.container():
        st.markdown("<h3 style='color: #111111; font-weight:800; font-size:22px; margin-bottom: 25px; letter-spacing:-0.03em;'>🍿 Finding Matches...</h3>", unsafe_allow_html=True)
        skeleton_cols = st.columns(5)
        for col in skeleton_cols:
            with col:
                st.markdown('<div class="skeleton-card"></div>', unsafe_allow_html=True)
                
    names, posters = recommend(selected_movie_name)
    
    # Overwrite placeholders with crisp movie tiles
    with placeholder.container():
        st.markdown(f"<h3 style='color: #111111; font-weight:800; font-size:22px; margin-bottom: 25px; letter-spacing:-0.03em;'>🍿 Top Picks For You</h3>", unsafe_allow_html=True)
        
        columns = st.columns(5)
        for idx, col in enumerate(columns):
            with col:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{posters[idx]}" alt="{names[idx]}">
                        <div class="movie-card-body">
                            <div class="movie-title">{names[idx]}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )