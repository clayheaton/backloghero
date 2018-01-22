"""
Initialize the app in this file.
"""
import datetime
from settings import CONFIG_VARS
from flask import Flask, render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, current_user
from backloghero.database import db_session, init_db
from backloghero.models import User, Role

# Create app
app = Flask(__name__)

# Apply app settings
for key in CONFIG_VARS.keys():
    app.config[key] = CONFIG_VARS[key]

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    if not user_datastore.get_user(app.config["INITIAL_USER_EMAIL"]):
        user_datastore.create_user(email=app.config["INITIAL_USER_EMAIL"],
                                   password=app.config["INITIAL_USER_PASSWORD"],
                                   confirmed_at=datetime.datetime.now())
    db_session.commit()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

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
