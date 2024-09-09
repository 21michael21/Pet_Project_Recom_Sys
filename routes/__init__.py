from flask import Blueprint

main_bp = Blueprint('main_bp', __name__, template_folder='../templates')
recommendations_bp = Blueprint('recommendations_bp', __name__, template_folder='../templates')
profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates')
feedback_bp = Blueprint('feedback_bp', __name__, template_folder='../templates')

from . import main, recommendations, profile, feedback