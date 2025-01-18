from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app, request
from werkzeug.security import check_password_hash
from functools import wraps


def get_jwt_config():
    """
    Fetches the JWT config values from the current app context.

    :return: SECRET_KEY and EXPIRATION_TIME
    """
    return current_app.config.get('JWT_SECRET_KEY', None), current_app.config.get('JWT_EXPIRATION_TIME', None)


def generate_jwt_token(user_id):
    """
    Generates a JWT token for the given user ID.

    :param user_id: The user ID to be embedded in the token
    :return: The encoded JWT token
    """
    JWT_SECRET_KEY, EXPIRATION_TIME = get_jwt_config()
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRATION_TIME)
    token = jwt.encode(
        {"sub": str(user_id), "exp": expiration_time},
        JWT_SECRET_KEY,
        algorithm="HS256"
    )
    return token

def verify_jwt_token(token):
    """
    Verifies the provided JWT token.

    :param token: The JWT token to verify
    :return: The decoded token payload if valid, otherwise None
    """
    SECRET_KEY, _ = get_jwt_config()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def jwt_required(f):
    """
    Decorator to enforce JWT authentication on protected routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return create_response(message="Token is missing", success=False), 401

        user_data = verify_jwt_token(token)
        if user_data is None:
            return create_response(message="Token is invalid or expired", success=False), 401

        request.user_id = user_data['sub']
        return f(*args, **kwargs)

    return decorated_function


def hash_password(password: str) -> str:
    """
    Hashes a plain text password.
    """
    return generate_password_hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """
    Verifies a hashed password with the plain text version.
    """
    return check_password_hash(hashed_password, password)


def create_response(**kwargs):
    """
    A utility function to format responses consistently across the app.

    :param kwargs: Dynamic arguments to include in the response.
        - data: The main response data (optional).
        - message: Message to be included in the response (optional).
        - success: Whether the operation was successful or not (default: True).
        - error: Any error message (optional).
        - total_count: Total count of records (for pagination) (optional).
        - page: The current page of the data (optional).
        - limit: The number of items per page (optional).
        - token: JWT token to include in the response (optional).
    :return: A structured JSON response.
    """
    response = {
        "success": kwargs.get("success", True),  
        "message": kwargs.get("message", None),  
        "data": kwargs.get("data", None)   
    }

    if "total_count" in kwargs:
        response["pagination"] = {
            "total_count": kwargs["total_count"],
            "page": kwargs.get("page"),
            "limit": kwargs.get("limit")
        }

    if "error" in kwargs:
        response["error"] = kwargs["error"]

    if "token" in kwargs:
        response["token"] = kwargs["token"]

    return response
