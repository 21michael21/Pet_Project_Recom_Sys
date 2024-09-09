from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import SearchForm
from models import db, SearchHistory, Movie, WatchedMovie, Rating
from recommendation import get_recommendations
from routes import recommendations_bp

@recommendations_bp.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():
    form = SearchForm()
    movies = []
    if form.validate_on_submit():
        query = form.movie_title.data
        movies = get_recommendations(query)
        if movies:
            history = SearchHistory(user_id=current_user.id, query=query)
            db.session.add(history)
            db.session.commit()
        else:
            flash('Фильмы с таким названием не найдены.')
    return render_template('recommendations.html', form=form, movies=movies)

@recommendations_bp.route('/rate_movie/<int:movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    rating_value = request.form.get('rating')
    if rating_value:
        rating_value = float(rating_value)
        rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if rating:
            rating.rating = rating_value
        else:
            rating = Rating(user_id=current_user.id, movie_id=movie_id, rating=rating_value)
            db.session.add(rating)
        db.session.commit()
        Movie.query.get(movie_id).update_average_rating()
        flash('Рейтинг успешно сохранен.')
    return redirect(url_for('recommendations_bp.recommendations'))