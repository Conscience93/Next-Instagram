from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin

def has_lower(word):
    return re.search("[a-z]", word)

def has_upper(word):
    return re.search("[A-Z]", word)

def has_special(word):
    return re.search("[\W]", word)


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=True, null=False)
    url_profile_picture = pw.CharField(null=True)
    is_private = pw.BooleanField(default=False)
    

    def validate(self):
        existing_user = User.get_or_none(name=self.name)

        if existing_user != None:
            self.errors.append("The username has been taken! Try something creative!")

        if len(self.name) < 4:
            self.errors.append("Username must have at least 4 characters!")

        if len(self.password) < 7:
            self.errors.append("Password must have at least 6 characters!")

        if not has_lower(self.password):
            self.errors.append("Password must have at least a lower character!")

        if not has_upper(self.password):
            self.errors.append("Password must have at least an upper character!")

        if not has_special(self.password):
            self.errors.append("Password must have at least a special character!")

        if len(self.errors) == 0:
            self.password = generate_password_hash(self.password)

    def validate2(self):                    # edit username only
        existing_user = User.get_or_none(name=self.name)

        if existing_user != None:
            self.errors.append("The username has been taken! Try something creative!")


