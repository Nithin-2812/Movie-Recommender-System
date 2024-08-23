import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .stButton button:hover {
        background-color: #FF6B6B;
        color: white;
    }
    .movie-card {
        text-align: center;
        padding: 15px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        border-radius: 8px;
        background-color: white;
        transition: transform 0.2s ease;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .movie-title {
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }
    .movie-poster {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page header
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>Get personalized movie recommendations based on your favorite movies!</p>", unsafe_allow_html=True)

# Banner Image
banner_image = "banner-4.png"  # Replace with your image file or URL
st.image(banner_image, use_column_width=True, width=-500)

# Load movie data and similarity model
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in a visually appealing layout
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='movie-card'><img class='movie-poster' src='{recommended_movie_posters[i]}' width='150'><div class='movie-title'>{recommended_movie_names[i]}</div></div>", unsafe_allow_html=True)
