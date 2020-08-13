from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
from models.user import User
from models.image import Image
from models.payment import Payment

import boto3, botocore
from config import AWS_KEY, AWS_SECRET, AWS_BUCKET, AWS_LOCATION

s3 = boto3.client(
   "s3",
   aws_access_key_id=AWS_KEY,
   aws_secret_access_key=AWS_SECRET
)

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('create/', methods=['POST'])       # upload image
def create():
    if "image_picture" not in request.files:      # also contains filename, content_type, content_length, mimetype 
        flash("PLS UPLOAD SOMETHING")
        return redirect(url_for("images.new"))

    else:
        file = request.files["image_picture"]
        file_description = request.form["image_description"]
        if file_description == "" or file_description == None:
            file_description = "None"
        try:
            s3.upload_fileobj(
                file,
                AWS_BUCKET,
                file.filename,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
            })

            image = Image(  user=current_user.id, 
                            image_url=f"{AWS_LOCATION}{file.filename}", 
                            image_description=file_description
                        )
            image.save_url_profile_picture()
        
            flash("Your profile picture has been uploaded!")
            return redirect(url_for("images.new"))

        except Exception as e:
            print(e)
            flash("Something Happened.")
            return redirect(url_for("images.new"))


@images_blueprint.route('/<id>', methods=["GET"])
def show(id):
    image = Image.get_or_none(id=id)
    return render_template('images/show.html', image=image)


@images_blueprint.route('/', methods=["GET"])
def index():
    pass


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass