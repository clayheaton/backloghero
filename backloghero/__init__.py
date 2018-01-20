"""
Initialize the app in this file.
"""

from flask import Flask
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, current_user
from backloghero.database import db_session, init_db
from backloghero.models import User, Role

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'asecretagain'

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db_session.commit()

# Views
@app.route('/')
@login_required
def home():
    return 'Here you go!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out'


############################################
# Import additional module files
import backloghero.database
import backloghero.models

def list_routes():
    """
    Function that prints to console all routes in the Flask app.
    Uncomment the line below to display them when the app starts.
    """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)
