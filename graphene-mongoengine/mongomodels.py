
from mongoengine import Document
from mongoengine.fields import StringField

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
