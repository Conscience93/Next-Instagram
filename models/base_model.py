import os
import peewee as pw
import datetime
from database import db


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def save2(self, *args, **kwargs):               # update username
        self.errors = []
        self.validate2()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def save_url_profile_picture(self, *args, **kwargs):               # update profile picuter url
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
        

    def validate(self):
        print("debug2222222222222")
        return True

    class Meta:
        database = db
        legacy_table_names = False
