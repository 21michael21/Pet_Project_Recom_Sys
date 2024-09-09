from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    reviews = db.relationship('Review', backref='user', lazy=True)
    watched_movies = db.relationship('WatchedMovie', backref='user', lazy=True)
    search_history = db.relationship('SearchHistory', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    genres = db.Column(db.String(150), nullable=False)
    overview = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, default=0.0)
    reviews = db.relationship('Review', backref='movie', lazy=True)
    watched_movies = db.relationship('WatchedMovie', backref='movie', lazy=True)

    def update_average_rating(self):
        ratings = Rating.query.filter_by(movie_id=self.id).all()
        if ratings:
            average_rating = sum([rating.rating for rating in ratings]) / len(ratings)
            self.rating = round(average_rating, 2)
            db.session.commit()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Columnrating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class WatchedMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    watched_date = db.Column(db.DateTime, server_default=db.func.now())

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    @staticmethod
    def update_movie_ratings():
        movies = Movie.query.all()
        for movie in movies:
            ratings = Rating.query.filter_by(movie_id=movie.id).all()
            if ratings:
                average_rating = sum([rating.rating for rating in ratings]) / len(ratings)
                movie.rating = round(average_rating, 2)
        db.session.commit()