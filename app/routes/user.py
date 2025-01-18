from flask  import request
from flask_restx import Namespace, Resource
from werkzeug.security import check_password_hash, generate_password_hash
from logs import log, log_error
from app.repository import Repository
from app.models import User
from app.utils import create_response, generate_jwt_token  

user_namespace = Namespace('users', description='User management')

@user_namespace.route('/signup')
class SignUpAPI(Resource):
    def post(self):
        """
        Sign up a new user.

        :return: JSON response indicating the success or failure of the signup process.
        """
        try:
            # Log entry into the function
            log("Entering the signup function")

            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            log(f"Received data - username: {username}, password: {password}")

            if not username or not password or not confirm_password:
                log("Validation failed: All fields are required")
                return create_response(
                    message="All fields are required",
                    success=False
                ), 400

            if password != confirm_password:
                log("Validation failed: Passwords do not match")
                return create_response(
                    message="Passwords do not match",
                    success=False
                ), 400

            existing_user = Repository.get_record_by_field(User, 'username', username, {'single': True})
            if existing_user:
                log(f"User with username {username} already exists")
                return create_response(
                    message="User already exists",
                    success=False
                ), 400

            hashed_password = generate_password_hash(password)

            new_user = Repository.create_record(User, username=username, password=hashed_password)

            log(f"User {new_user.username} created successfully")

            return create_response(
                message=f"User {new_user.username} created successfully",
                success=True
            ), 201

        except Exception as e:
            log_error(f"Error during signup: {e}")
            return create_response(
                message="An error occurred during signup",
                success=False,
                error=str(e)
            ), 500


@user_namespace.route('/login')
class LoginAPI(Resource):
    def post(self):
        """
        Log in an existing user.

        :return: JSON response containing the JWT token if login is successful.
        """
        try:
            log("Entering the login function")

            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            log(f"Received data - username: {username}, password: {password}")

            if not username or not password:
                log("Validation failed: Username and password are required")
                return create_response(
                    message="Username and password are required",
                    success=False
                ), 400

            user = Repository.get_record_by_field(User, 'username', username, {'single': True})

            if user and check_password_hash(user.password, password):
                token = generate_jwt_token(user.id)

                log(f"Login successful for user {username}")

                return create_response(
                    message="Login successful",
                    success=True,
                    token=token
                ), 200

            log(f"Invalid credentials for user {username}")
            return create_response(
                message="Invalid credentials, please try again",
                success=False
            ), 401

        except Exception as e:
            log_error(f"Error during login: {e}")
            return create_response(
                message="An error occurred during login",
                success=False,
                error=str(e)
            ), 500
