from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms import FeedbackForm
from models import db, Review, Movie
from routes import feedback_bp

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        rating = form.rating.data
        message = form.message.data
        movie_id = form.movie_id.data

        review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if review:
            review.rating = rating
            review.comment = message
        else:
            review = Review(user_id=current_user.id, movie_id=movie_id, rating=rating, comment=message)
            db.session.add(review)
        db.session.commit()
        Movie.query.get(movie_id).update_average_rating()

        with open('feedbacks.txt', 'a') as f:
            f.write(f"{current_user.email}: {message}\n")

        flash('Спасибо за ваш отзыв!')
        return redirect(url_for('feedback_bp.feedback'))

    return render_template('feedback.html', form=form)