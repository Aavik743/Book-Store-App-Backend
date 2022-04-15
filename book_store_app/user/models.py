from mongoengine import Document, StringField, EmailField, BooleanField, SequenceField


class Users(Document):
    id = SequenceField(primary_key=True)
    name = StringField()
    username = StringField()
    password = StringField()
    email_id = EmailField()

    def to_dict(self):
        user_dict = {
            'name': self.name,
            'username': self.username,
            'email_id': self.email_id,
            'password': self.password
        }
        return user_dict

    @classmethod
    def check_username(cls, username):
        data1 = Users.objects.filter(username=username)
        return data1

    @classmethod
    def check_email(cls, email_id):
        return Users.objects.filter(email_id=email_id)
