import streamlit as st
import pandas as pd
import pickle
import requests

# 🔧 OMDb API key
OMDB_API_KEY = "e4d2063c"

# 🔧 Fetch movie poster from OMDb API
def fetch_poster_omdb(movie_name):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "Poster" in data and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450.png?text=Error"

# 🔍 Recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        idx = i[0]
        title = movies.at[idx, 'title']
        poster = fetch_poster_omdb(title)

        recommended_titles.append(title)
        recommended_posters.append(poster)

    return recommended_titles, recommended_posters

# 🗂️ Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🎬 UI
st.title('🎥 Movie Recommendation System')

# Movie dropdown
selected_movie_name = st.selectbox(
    'Which movie do you want to get recommendations for?',
    movies['title'].values
)

# Show selected movie poster immediately
if selected_movie_name:
    st.image(fetch_poster_omdb(selected_movie_name), caption=selected_movie_name)

# Show recommendations when button is clicked
if st.button('Recommend'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
