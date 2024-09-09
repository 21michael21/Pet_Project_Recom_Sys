from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, SearchHistory, Review, WatchedMovie, Movie
from routes import profile_bp
import os

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    search_history = db.session.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).order_by(SearchHistory.timestamp.desc()).all()
    reviews = db.session.query(Review).filter(Review.user_id == current_user.id).order_by(Review.created_at.desc()).all()
    watched_movies = db.session.query(WatchedMovie).filter(WatchedMovie.user_id == current_user.id).order_by(WatchedMovie.watched_date.desc()).all()
    movies_info = {movie.id: movie for movie in Movie.query.all()}
    return render_template('profile.html', search_history=search_history, reviews=reviews, watched_movies=watched_movies, movies_info=movies_info)

@profile_bp.route('/review_movie/<int:movie_id>', methods=['POST'])
@login_required
def review_movie(movie_id):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Фильм не найден.')
        return redirect(url_for('profile_bp.profile'))

    if rating:
        try:
            review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
            if review:
                review.rating = int(rating)
                review.comment = comment
            else:
                review = Review(user_id=current_user.id, movie_id=movie_id, rating=int(rating), comment=comment)
                db.session.add(review)
            db.session.commit()
            movie.update_average_rating()
            flash('Отзыв успешно сохранен.')
        except ValueError:
            flash('Некорректное значение рейтинга.')
    else:
        flash('Пожалуйста, укажите рейтинг.')

    return redirect(url_for('profile_bp.profile'))

@profile_bp.route('/watch_movie/<int:movie_id>', methods=['POST'])
@login_required
def watch_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Фильм не найден.')
        return redirect(url_for('profile_bp.profile'))

    watched_movie = WatchedMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if not watched_movie:
        watched_movie = WatchedMovie(user_id=current_user.id, movie_id=movie_id)
        db.session.add(watched_movie)
        db.session.commit()
        flash('Фильм добавлен в список просмотренных.')
    else:
        flash('Фильм уже в списке просмотренных.')

    return redirect(url_for('profile_bp.profile'))

@profile_bp.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('Нет выбранного файла.')
        return redirect(url_for('profile_bp.profile'))

    file = request.files['avatar']
    if file.filename == '':
        flash('Файл не выбран.')
        return redirect(url_for('profile_bp.profile'))

    if file:
        filename = f"{current_user.id}_avatar.png"
        filepath = os.path.join('static/images', filename)
        file.save(filepath)
        flash('Аватар успешно загружен.')
        return redirect(url_for('profile_bp.profile'))
