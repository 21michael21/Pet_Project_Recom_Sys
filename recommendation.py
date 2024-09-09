import pandas as pd
from models import Movie

movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')

def get_recommendations(title, n=5):
    title = title.lower()
    movie = movies_df[movies_df['title'].str.lower().str.contains(title)]
    if movie.empty:
        return []

    movie_id = movie.iloc[0]['movieId']
    user_ids = ratings_df[ratings_df['movieId'] == movie_id]['userId'].unique()
    similar_ratings = ratings_df[ratings_df['userId'].isin(user_ids)]
    similar_movies = similar_ratings['movieId'].value_counts().index.tolist()
    
    recommended_movies = [Movie.query.get(mid) for mid in similar_movies if mid != movie_id]
    return recommended_movies[:n]