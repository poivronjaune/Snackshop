from unicodedata import name
from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", name=current_user.username)

