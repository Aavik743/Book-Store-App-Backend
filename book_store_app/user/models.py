from mongoengine import Document, StringField, EmailField, SequenceField, BooleanField, IntField


class Users(Document):
    id = SequenceField(primary_key=True)
    name = StringField()
    username = StringField()
    password = StringField()
    email_id = EmailField()
    address = StringField()
    pincode = IntField()
    is_verified = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    def to_dict(self):
        user_dict = {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'email_id': self.email_id,
            'address': self.address,
            'pincode': self.pincode,
            'is_verified': self.is_verified,
            'is_admin': self.is_admin
        }
        return user_dict

    @classmethod
    def check_username(cls, username):
        data1 = Users.objects.filter(username=username)
        return data1

    @classmethod
    def check_email(cls, email_id):
        return Users.objects.filter(email_id=email_id)
