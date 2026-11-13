import streamlit as st
import pandas as pd
import pickle
import joblib

st.title("Movie Recommendation System")


# Load files only once
@st.cache_resource
def load_data():
    with open("movie.pickle", "rb") as m:
        movies = pickle.load(m)

    similarity = joblib.load("similarity.joblib")

    return movies, similarity


try:
    movies, similarity = load_data()
    st.success("Movie data loaded successfully!")

except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()


movies_names = movies["title"].dropna().values


def recommend(name_movie):

    matched_movies = movies[
        movies["title"] == name_movie
    ].index

    if len(matched_movies) == 0:
        return []

    movie_index = matched_movies[0]

    recommendation = similarity[movie_index]

    movie_list = sorted(
        enumerate(recommendation),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_names = []

    for i in movie_list:
        recommended_names.append(
            movies.iloc[i[0]].title
        )

    return recommended_names


name_movies = st.selectbox(
    "Enter Movie Name",
    movies_names
)

if st.button("Recommend"):

    with st.spinner("Finding recommended movies..."):

        try:
            results = recommend(name_movies)

            st.subheader("Recommended Movies")

            if results:
                for movie in results:
                    st.write(movie)
            else:
                st.warning("No recommendations found.")

        except Exception as e:
            st.error(f"Recommendation error: {e}")