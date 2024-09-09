from flask import Flask, render_template
from config import Config
from models import db, User
from routes import main_bp, recommendations_bp, profile_bp, feedback_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_blueprint(main_bp)
app.register_blueprint(recommendations_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(feedback_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)