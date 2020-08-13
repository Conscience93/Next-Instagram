from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Following(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)

