import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_posters(movie_id):

    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    response = requests.get(url)
    data = response.json()
    print(data)
    # return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # return placeholder image if poster not available
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

import gzip

with gzip.open('data.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

st.title('Film Friend')

selected_movie_name = st.selectbox(
    "Choose a movie",
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

st.markdown("""
    <style>
    .footer {
        text-align: center;
        padding: 20px;
        color: gray;
        font-size: 14px;
        margin-top: 50px;
    }
    </style>

    <div class="footer">
        Built by Parth Chavare
    </div>
""", unsafe_allow_html=True)
