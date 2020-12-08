from flask import Flask, g
from flask_cors import CORS
from resources.walks import walk
from flask_login import LoginManager
import os
from resources.users import user
import models

DEBUG = True
PORT = 8000


# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)
login_manager = LoginManager()
# sets up the ability to set up the session
app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" # Need this to encode the session

login_manager.init_app(app) # set up the sessions on the app

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_user(userid):
    try:
        # print('loading the following user')
        # user = models.User.get_by_id(user_id) # Important Change
        return models.User.get(models.User.id == userid)
        return user
    except models.DoesNotExist:
        return None

CORS(walk, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(user, url_prefix='/api/v1/users')

app.register_blueprint(walk, url_prefix='/api/v1/walks')

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(walk, origins=['http://localhost:3000'], supports_credentials=True)



# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)