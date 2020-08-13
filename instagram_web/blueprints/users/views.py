from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_manager, current_user, login_required


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])    # sign up page
def new():
    return render_template('users/new.html')


from models.user import User
from models.follower import Following

@users_blueprint.route('/create', methods=['POST'])      # create new user
def create():
    new_username = request.form['username']
    new_email = request.form['email']
    new_password = request.form['password']

    user = User(name=new_username, email=new_email, password=new_password)
    user.save()
    
    if len(user.errors) == 0:
        flash("You have successfully registered! oh no")
        return redirect(url_for("home"))
    else:
        return render_template("users/new.html", errors = user.errors)


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    user = User.get_or_none(id=id)
    follower = Following.get_or_none(Following.follower_id == current_user.id)
    list_of_followers = Following.select().where(Following.user_id == id)
    return render_template('users/show.html', user=user, follower=follower, list=list_of_followers )


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/home.html')


@users_blueprint.route('<id>/edit', methods=['GET'])       # edit page
@login_required
def edit(id):
    user = User.get_by_id(current_user.id)
    if user:
        if current_user.id == int(id):
            return render_template('users/edit.html', user=user)
        else:
            flash("You cannot edit other people's profile!")
            return redirect(url_for("home"))
    else:
        flash("User not found! Also it's illegal!")
        return redirect(url_for("home"))


@users_blueprint.route('/update', methods=['POST'])       # update username
@login_required
def update():
    update_name = request.form['username']

    if current_user.name == update_name and "private" not in request.form:
        flash("u click button")
        return redirect(url_for("users.edit", id=current_user.id))
    elif len(update_name) < 5:
        flash("whoa pls. Need at least 4 characters")
        return redirect(url_for("users.edit", id=current_user.id))
    elif current_user.name == update_name:
        is_private = request.form['private']

        user = User.get_by_id(current_user.id)
        user.is_private = is_private
        user.save_url_profile_picture()
        if is_private == True:
            flash("You are currently set your profile to private")
        else:
            flash("You are currently set your profile to public")
        return redirect(url_for("users.edit", id=current_user.id))
    else:
        is_private = request.form['private']

        user = User.get_by_id(current_user.id)
        user.name = update_name
        user.is_private = is_private
        user.save2()

        if len(user.errors) == 0:
            current_user.name = update_name
            flash("Your username has been edited")
            return redirect(url_for("users.edit", id=current_user.id))
        else:
            return render_template("users/edit.html", errors = user.errors)
        
        
# not restful :(
import boto3, botocore
from config import AWS_KEY, AWS_SECRET, AWS_BUCKET, AWS_LOCATION
from werkzeug import secure_filename

s3 = boto3.client(
   "s3",
   aws_access_key_id=AWS_KEY,
   aws_secret_access_key=AWS_SECRET
)

@users_blueprint.route('/upload', methods=['POST'])   
def upload():
    if "file_profile_picture" not in request.files:      # also contains filename, content_type, content_length, mimetype 
        flash("PLS UPLOAD SOMETHING")
        return redirect(url_for("users.edit", id=current_user.id))

    else:
        file = request.files["file_profile_picture"]

        try:
            s3.upload_fileobj(
                file,
                AWS_BUCKET,
                file.filename,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
            })

            user = User.get_by_id(current_user.id)
            user.url_profile_picture = f"{AWS_LOCATION}{file.filename}"
            user.save_url_profile_picture()
            flash("Your profile picture has been uploaded!")
            return redirect(url_for("users.edit", id=current_user.id))

        except Exception as e:
            print(e)
            flash("Something Happened.")
            return redirect(url_for("users.edit", id=current_user.id))



@users_blueprint.route('/follow/<id>', methods=['POST'])             # follow user
def follow(id):
    user = User.get_or_none(id=id)
    follow = Following(user=user.id, follower = current_user.id)
    follow.save_url_profile_picture()

    flash("you are now following user " + user.name + "!")
    return redirect(url_for("users.show", id = id))


@users_blueprint.route('/unfollow/<id>', methods=['POST'])             # unfollow user
def unfollow(id):
    user = User.get_or_none(id=id)
    unfollow = Following.get(Following.follower_id == current_user.id)
    unfollow.delete_instance()

    flash("you have unfollowed user " + user.name + "!")
    return redirect(url_for("users.show", id = id))
