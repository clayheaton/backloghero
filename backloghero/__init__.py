"""
Initialize the app in this file.
"""
import datetime
from settings import CONFIG_VARS
from flask import Flask, render_template
from flask_security import Security, login_required, user_registered, roles_required, \
     SQLAlchemySessionUserDatastore, current_user, RoleMixin, UserMixin, utils
from flask_security.forms import RegisterForm, ConfirmRegisterForm, StringField, Required
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib import sqla

from flask_wtf import Form
from wtforms.fields import PasswordField
from backloghero.database import db_session, init_db
from backloghero.models import User, Role

# Create app
app = Flask(__name__)

# Apply app settings
for key in CONFIG_VARS.keys():
    app.config[key] = CONFIG_VARS[key]

mail = Mail(app)

# Additional Registration Forms/Fields
# We added some fields, so we need to customize the form for registration.
# https://pythonhosted.org/Flask-Security/customizing.html#forms
class ExtendedRegisterForm(RegisterForm):
    qt3_name = StringField('Qt3 Name', [Required()])
    steam_url = StringField('Steam Profile URL', [Required()])

class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    qt3_name = StringField('Qt3 Name', [Required()])
    steam_url = StringField('Steam Profile URL', [Required()])

# For for updating Steam name
class SteamUpdateNameForm(Form):
    steamname = StringField('Steam Name', [Required()])

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore,
                    register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedConfirmRegisterForm)



# Create a user to test with
@app.before_first_request
def create_user():
    init_db()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='trusted-user', description='Trusted user')

    encrypted_password = utils.encrypt_password('password')

    if not user_datastore.get_user('enduser@example.com'):
        user_datastore.create_user(email='enduser@example.com',
                                   password=encrypted_password,
                                   confirmed_at=datetime.datetime.now())

    if not user_datastore.get_user('participant@example.com'):
        user_datastore.create_user(email='participant@example.com',
                                   password=encrypted_password,
                                   confirmed_at=datetime.datetime.now())

    # Default admin user
    if not user_datastore.get_user(app.config["INITIAL_ADMIN_EMAIL"]):
        user_datastore.create_user(email=app.config["INITIAL_ADMIN_EMAIL"],
                                   password=app.config["INITIAL_ADMIN_PASSWORD"],
                                   confirmed_at=datetime.datetime.now(),
                                   qt3_name=app.config["INITIAL_ADMIN_QT3_NAME"],
                                   steam_name="ccheaton",
                                   steam_id=12345)
    db_session.commit()

    user_datastore.add_role_to_user('enduser@example.com', 'trusted-user')
    user_datastore.add_role_to_user(app.config["INITIAL_ADMIN_EMAIL"], 'admin')
    user_datastore.add_role_to_user(app.config["INITIAL_ADMIN_EMAIL"], 'trusted-user')

    db_session.commit()

# Views
@app.route('/')

def home():
    return render_template('index.html')


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
