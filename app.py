import streamlit as st
import pandas as pd
import pickle
import requests as rq

df = pickle.load(open('df.pkl', 'rb'))
df = pd.DataFrame(df)

similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(name):
    index = df[df['title'] == name].index[0]
    distance = similarity[index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    movies = []
    movies_image = []

    for i in movie_list:
        movies.append(df['title'][i[0]])
        movies_image.append(fetch_Image(df['id'][i[0]]))
    return movies, movies_image


def fetch_Image(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=2c3da76a1596fa7fedc48da47c5b5250&language=en-US".format(
        movie_id)
    data = rq.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# st.markdown("""
#             <style>
#             .custom-title {
#                 text-decoration: underline;
#             }
#             </style>
#             """, unsafe_allow_html=True
# )
# st.markdown('<h1 class="custom-title">Movie Recommendation System</h1>', unsafe_allow_html=True)
st.title("Movie Recommendation System")
st.subheader("Enter to get Best Recommendation")

col1, col2 = st.columns([3, 1])
with col1:
    option = st.selectbox("",
                          df['title'].values)
with col2:
    st.markdown("""
            <style>
            .stButton > button {
                width: 200px;
                height: 50px;
            }
            </style>
            """, unsafe_allow_html=True)
    button = st.button("Recommend")

if button:
    st.subheader('\n\nSimilar Movies\n\n')
    movie_list, movie_image = recommend(option)

    c1, c2, c3, c4, c5 = st.columns(5)
    columns = [c1, c2, c3, c4, c5]
    for i, j, k in zip(movie_list, movie_image, columns):
        with k:
            st.write(i)
            st.image(j)
    # for i in movie_image:
    #     st.image(i)
