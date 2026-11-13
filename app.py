import streamlit as st
import pandas as pd
import pickle
import joblib
import nltk
import sklearn 

st.title("Movie Recommendation System")

with open('movie.pickle','rb') as m:
    movies=pickle.load(m)

similarity=joblib.load('similarity.joblib')    

movies_names=movies['title'].values

def recommend(name_movie):
    movie_index=movies[movies['title']==name_movie].index[0]

    recommendation=similarity[movie_index]

    movie_list=sorted(enumerate(recommendation),reverse=True,key=lambda x:x[1])[1:6]

    r_movie_names=[]
    for i in movie_list :
        r_movie_names.append(movies.iloc[i[0]].title)
    return r_movie_names

name_movies=st.selectbox('Enter Movie Name',movies_names)    

if st.button("Recommend") :
   r=recommend(name_movies)
   st.write("Recommended Movies are :")
   for i in r:
    st.write(i)