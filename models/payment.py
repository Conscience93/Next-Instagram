from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

class Payment(BaseModel):
    sender = pw.ForeignKeyField(User, backref="payment")
    image = pw.ForeignKeyField(Image, backref="payment")
    amount = pw.DecimalField()

