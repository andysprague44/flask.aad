import flask
from datetime import datetime, timedelta
from functools import wraps
from application import appsettings as config
from flask import current_app

def login_required(f):
    """
    Decorator for flask endpoints, ensuring that the user is authenticated and redirecting to log-in page if not.
    Example:
    ```
        from server import server
        @login_required
        @server.route("/")
        def home():
            return 'protected data'
    ```
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.REQUIRE_AUTHENTICATION:
            # Disable authentication, for dev/test only!
            current_app.logger.error('Authentication is disabled! For dev/test only!')
            flask.session['user'] = {'name': 'AUTHENTICATION DISABLED'}
            return f(*args, **kwargs)

        if not flask.session.get("user"):
            return flask.redirect(flask.url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function
