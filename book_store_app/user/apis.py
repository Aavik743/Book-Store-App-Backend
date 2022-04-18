import json

from flask import request, render_template
from flask_restful import Resource

from common import logger
from common.exception import NotUniqueException, NotMatchingException, NotFoundException
from common.utils import send_mail, access_token, JWT_required, generate_otp, generate_token, get_short_token, \
    jwt_required
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
        except NotMatchingException as e:
            logger.logging.error('Log Error Message')
            return e.__dict__
        except Exception:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Login_API(Resource):
    def post(self):
        """
            This API is used to authenticate user to access resources
            @param request: user credential like username and password
            @return: Returns success message and access token on successful login
        """
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')
        user = Users.objects.get(username=username)
        if not user.is_verified:
            return {
                'Error': 'Account is not verified', 'status code': 400
            }
        try:
            if password != user.password:
                raise NotMatchingException('password does not match', 400)
            if password == user.password:
                token = get_short_token(access_token(user.id))
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': token
                }
        except NotMatchingException as e:
            logger.logging.error('Log Error Message')
            return e.__dict__
        except Exception:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Reset_Password_API(Resource):
    method_decorators = {'get': [JWT_required]}

    def get(self, decoded_data):
        """
            This API accepts the changes the current password
            @param : current password and new password
            @return: success message and new password
        """
        data = json.loads(request.data)
        password = data.get('password')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = Users.objects.get(id=decoded_data)
        try:
            if user.password != password:
                raise NotFoundException('password does not match', 400)
            if password1 != password2:
                raise NotMatchingException('new passwords does not match', 400)
            if user.password == password:
                if password1 == password2:
                    user.password = password1
                    user.save()
                    return {"message": "new password created", "new password": user.password, 'status code': 200}
                else:
                    logger.logging.warning('Log Error Message')
                    return {"Error": 'new password does not match', 'code': 400}
            else:
                logger.logging.warning('Log Error Message')
                return {"Error": 'password does not match', 'code': 400}
        except NotFoundException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except NotMatchingException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Forgot_Pass_API(Resource):
    def get(self):
        """
            This API accepts the get request hit from the email on clicked on link
            @param : email and token
            @return: success message
        """
        data = json.loads(request.data)
        email_id = data.get('email_id')
        user = Users.objects.get(email_id=email_id)
        try:
            if not user:
                raise NotFoundException('account not available', 400)
            forgot_password_url = get_short_token(access_token(user.id))
            if user:
                template = render_template('forgotpassword.html', url=forgot_password_url)
                send_mail(email_id, template)

                return {"message": "forgot password link sent", 'status code': 200}

        except NotFoundException as e:
            logger.logging.error('Log Error Message')
            return e.__dict__
        except Exception as e:
            logger.logging.error('Log Error Message')
            return {'error': e, 'status code': 400}
