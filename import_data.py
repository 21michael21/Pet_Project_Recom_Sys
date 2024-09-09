import csv
from models import db, Movie, Rating
from app import app

def import_movies(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Проверяем, существует ли фильм с таким же id
            existing_movie = db.session.get(Movie, row['movieId'])
            if existing_movie is None:
                movie = Movie(id=row['movieId'], title=row['title'], genres=row['genres'], overview=row['overview'])
                db.session.add(movie)
        db.session.commit()

def import_ratings(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Проверяем, существует ли рейтинг с таким же id
            existing_rating = db.session.query(Rating).filter_by(user_id=row['userId'], movie_id=row['movieId']).first()
            if existing_rating is None:
                rating = Rating(user_id=row['userId'], movie_id=row['movieId'], rating=float(row['rating']))
                db.session.add(rating)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import_movies('movies.csv')
        import_ratings('ratings.csv')
