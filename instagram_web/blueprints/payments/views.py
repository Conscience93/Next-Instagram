from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
import braintree
import os

from models.payment import Payment
from models.user import User
from models.image import Image

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BT_MERCHANT_KEY'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)

# client_token = gateway.client_token.generate({
#     "customer_id": 1
# })

payments_blueprint = Blueprint('payments',
                            __name__,
                            template_folder='templates')


@payments_blueprint.route('/new/<image_id>', methods=['GET'])
def new(image_id):
    client_token=gateway.client_token.generate()
    return render_template('payments/new.html', client_token=client_token, image_id=image_id)


@payments_blueprint.route('/create/<image_id>', methods=['POST'])        # donate money
@login_required
def create(image_id):
    donated_amount=request.form["amount"]
    print(donated_amount)
    print(request.form)
    result = gateway.transaction.sale({
    "amount": donated_amount,
    "payment_method_nonce": request.form["payment_method_nonce"],
    "options": {
      "submit_for_settlement": True
        }
    })
    if result.is_success:
        flash(donated_amount + "Donated")
        payment = Payment(amount=donated_amount, sender=User.get_by_id(current_user.id), image=image_id)
        payment.save_url_profile_picture()
        image = Image.get_or_none(id=image_id)
        return redirect(url_for("images.show", id=image))
    else:
        flash("Something happened. ")
        print(result.errors)
        return redirect(url_for("payments.new", image_id=image_id))



@payments_blueprint.route('/<id>', methods=["GET"])
def show(id):
    pass


@payments_blueprint.route('/', methods=["GET"])
def index():
    pass


@payments_blueprint.route('/<id>/edit', methods=['GET'])            # will use this to send message hehe
def edit(id):
    # return requests.post(
    # "https://api.mailgun.net/v3/" + os.environ.get("MAILGUN_DOMAIN") + "/messages",
    # auth=("api", os.environ.get("MAILGUN_KEY")),
    # data={"from": "Excited User <mailgun@" + os.environ.get("MAILGUN_DOMAIN") +">",
    #         "to": ["mansonkho@yahoo.com"],
    #         "subject": "Test Mailgun",
    #         "text": "Testing some Mailgun awesomness!"})
    pass


@payments_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass