import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
                        # find the docs
                        # ^ these are functions that return/check hashed pw
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user
                        # login_user will be used to do the session
                        # stuff we manually did in express

# make this a blueprint
user = Blueprint('users','user')

@user.route('/', methods=['GET'])
def test_user_resource():
    return "user resource works"


@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    # print(payload)

    # since emails are case insensitive in the world
    payload['email'] = payload['email'].lower()
    # we will do the same with username
    payload['username'] = payload['username'].lower()
    # print(payload)
    try:
    # .get is nice -- http://docs.peewee-orm.com/en/latest/peewee/querying.html#selecting-a-single-record
        models.User.get(models.User.email == payload['email'])
        # this will throw an error ("models.DoesNotExist exception")

        # if so -- we don't want to create the user
        # response: "user with that email already exists"
        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401

    except models.DoesNotExist: # except is like catch in JS
        # the user does not exist
        # scramble the password with bcrypt
        pw_hash = generate_password_hash(payload['password'])

        # create them
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )
        # respond with new object and success message
        # print(created_user)
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)

        # this is where we will actually use flask-login
        # this "logs in" the user and starts a session
        # https://flask-login.readthedocs.io/en/latest/#login-example
        login_user(created_user)

        # we can't jsonify the password (generate_password_hash gives us
        # something of type "bytes" which is unserializable)
        # plus we shouldn't send the encrypted pw back anyway
        # print(type(created_user_dict['password']))
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201

@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    try:
        user = models.User.get(models.User.email == payload['email'])

        user_dict = model_to_dict(user)
        # check the users pw using bcrypt
        # check_password_hash: 2 args..
          # 1. the encrypted pw you are checking against
          # 2. the pw attempt you are trying to verify
          # https://flask-bcrypt.readthedocs.io/en/latest/
        password_is_good = check_password_hash(user_dict['password'], payload['password'])

        if(password_is_good):
            # LOG THE USER IN!!! using flask-login
            login_user(user) # in express we did this manually by setting stuff in the session
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['email']}",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="Email or password is incorrect", #let's be vague
                status=401
            ), 401


    except models.DoesNotExist:
        return jsonify(
            data={},
            message="Email or password is incorrect", #let's be vague
            status=401
        ), 401

@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message="successful logout",
        status=200
    ), 200
