from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import request
from flask_restx import Api, Resource, fields

import jwt

from auth.models import db, Users, JWTTokenBlocklist
from auth.config import BaseConfig

router = Api(
    version="1.0", title="Flask API", description="A simple Flask API", doc="/docs"
)

signup_model = router.model(
    "SignUpModel",
    {
        "username": fields.String(required=True, min_length=2, max_length=32),
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16),
    },
)

login_model = router.model(
    "LoginModel",
    {
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16),
    },
)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]

        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 400

        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_email(data["email"])

            if not current_user:
                return {
                    "success": False,
                    "msg": "Sorry. Wrong auth token. This user does not exist.",
                }, 400

            token_expired = (
                db.session.query(JWTTokenBlocklist.id)
                .filter_by(jwt_token=token)
                .scalar()
            )

            if token_expired is not None:
                return {"success": False, "msg": "Token revoked."}, 400

            if not current_user.check_jwt_auth_active():
                return {"success": False, "msg": "Token expired."}, 400

        except:
            return {"success": False, "msg": "Token is invalid"}, 400

        return f(current_user, *args, **kwargs)

    return decorator


@router.route("/api/auth/register")
class Register(Resource):
    @router.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False, "msg": "Email already taken"}, 400

        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {
            "success": True,
            "userID": new_user.id,
            "msg": "The user was successfully registered",
        }, 200


@router.route("/api/auth/login")
class Login(Resource):
    @router.expect(login_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)

        if not user_exists:
            return {"success": False, "msg": "This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False, "msg": "Wrong credentials."}, 400

        token = jwt.encode(
            {"email": _email, "exp": datetime.utcnow() + timedelta(minutes=30)},
            BaseConfig.SECRET_KEY,
        )

        user_exists.set_jwt_auth_active(True)
        user_exists.save()

        return {"success": True, "token": token, "user": user_exists.toJSON()}, 200


@router.route("/api/auth/logout")
class LogoutUser(Resource):
    @token_required
    def post(self, current_user):
        _jwt_token = request.headers["authorization"]

        jwt_block = JWTTokenBlocklist(
            jwt_token=_jwt_token, created_at=datetime.now(timezone.utc)
        )
        jwt_block.save()

        self.set_jwt_auth_active(False)
        self.save()

        return {"success": True}, 200
