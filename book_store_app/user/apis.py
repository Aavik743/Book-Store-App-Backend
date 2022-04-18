import json

from flask import request, render_template
from flask_restful import Resource

from common import logger
from common.exception import NotUniqueException, NotMatchingException
from common.utils import send_mail, generate_otp, generate_token, get_short_token, jwt_required
from .models import Users


class Register_API(Resource):
    def post(self):
        """
            This api is for user registration to this application
            @param request: user registration data like username, email, password
            @return: account verification link and OTP to registered email once registration is successful
        """
        data = json.loads(request.data)
        email_id = data.get('email_id')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')
        address = data.get('address')
        pincode = data.get('pincode')

        user = Users(name=name, username=username, password=password, email_id=email_id, address=address,
                     pincode=pincode)
        otp = generate_otp()
        token = generate_token(otp, user.id)
        short_token = get_short_token(token)
        verification_url = r"http://127.0.0.1:5000/activate?token=" + f"{short_token}"
        try:
            if Users.check_username(username) or Users.check_email(email_id):
                raise NotUniqueException('user already exists', 400)
            else:
                template = render_template('verification.html', data={'otp': otp, 'verification_url': verification_url})
                send_mail(email_id, template)
                user.save()
                return {'message': 'confirmation email sent', 'status code': 200, 'short token': short_token}
        except NotUniqueException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except Exception:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Verification_API(Resource):
    method_decorators = {'get': [jwt_required]}

    def get(self, otp, user_id):

        """
         This Api verifies the user_id and otp sent to the email and activates the account
            @param otp & user_id: Get request hits with jwt token which contains user_id and otp
            @return: Account activation confirmation
        """
        data = json.loads(request.data)
        otp_ = data.get('otp')
        try:
            if otp != otp_:
                raise NotMatchingException('OTP does not match', 400)
            user = Users.objects.get(id=user_id)
            user['is_verified'] = True
            user.save()
            return {"message": "Your account is now verified", 'status code': 200}
        except NotMatchingException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except Exception:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}
