"""
Variables used in initializing the app
"""
CONFIG_VARS = {
    "DEBUG"                          : True,
    "SECRET_KEY"                     : 'super-secret',
    "SERVER_NAME"                    : 'localhost:8080',
    "SQLALCHEMY_DATABASE_URI"        : 'sqlite:///db.sqlite',
    "SQLALCHEMY_TRACK_MODIFICATIONS" : False,
    "SQLALCHEMY_ECHO"                : False,
    "SECURITY_PASSWORD_HASH"         : 'pbkdf2_sha512',
    "SECURITY_PASSWORD_SALT"         : 'saltsecret',
    "SECURITY_REGISTERABLE"          : True,
    "SECURITY_CONFIRMABLE"           : True,
    "SECURITY_DEFAULT_REMEMBER_ME"   : True,
    "SECURITY_CHANGEABLE"            : True,
    "SECURITY_RECOVERABLE"           : True,
    "SECURITY_POST_CHANGE_VIEW"      : '/changed',
    "SECURITY_POST_RESET_VIEW"       : '/reset_complete',
    "MAIL_SERVER"                    : 'smtp.gmail.com',
    "MAIL_PORT"                      : 465,
    "MAIL_USE_SSL"                   : True,
    "MAIL_USERNAME"                  : 'email@email.com',
    "MAIL_PASSWORD"                  : 'pw',
    "INITIAL_USER_EMAIL"             : 'test@test.com',
    "INITIAL_USER_PASSWORD"          : 'password',
    "STEAM_MASTER_KEY"               : 'steam_key',
    "CELERY_BACKEND"                 : 'sqla+sqlite:///celerydb.sqlite',
    "CELERY_BROKER_URL"              : 'sqla+sqlite:///celerydb.sqlite',
    "CELERY_RESULT_BACKEND"          : 'db+sqlite:///celery_results.sqlite',
    "CELERY_RESULT_PERSISTENT"       : True
}
