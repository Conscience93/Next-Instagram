from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, login_manager, current_user, login_required, logout_user
from models.user import User
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])      # login page
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/create', methods=['POST'])     # login process
def create():
    check_username = request.form['username']
    check_password = request.form['password']
    user = User.get_or_none(name=check_username)

    if user:
        result = check_password_hash(user.password, check_password)
        if result:
            login_user(user)
            flash("You have successfully logged in. Whew what a journey")
            return redirect( url_for('home'))
        else:
            flash("Your password is incorrect!")
            return redirect(url_for("sessions.new"))
    else:
        flash("Your username is not found or something!")
        return redirect(url_for("sessions.new"))


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
def index():
    pass


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@sessions_blueprint.route('/logout', methods=['GET'])       # log out
@login_required
def destroy():
    logout_user()
    flash("You have log out. :(")
    return redirect(url_for("home"))

## GOOGLE LOGIN
@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash('you logged in through google')
        return redirect(url_for('home'))
    else:
        flash("GOOGLE EMAIL IS NOT FOUND OR SOMETHING")
        return redirect(url_for('home'))
