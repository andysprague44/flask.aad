
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from . import appsettings as config

def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    app.config.from_object('application.appsettings.FlaskConfig')

    with app.app_context():
        # Flask routes
        from . import routes

        # Register blueprint for auth
        from blueprints import auth
        app.register_blueprint(
            auth.construct_blueprint(config.AuthenticationConfig),
            url_prefix='/auth')

        # Init the embedded dash app
        from .dashapp import create_dashapp
        app = create_dashapp(app)

        # Fix "flask.url_for" when deployed to an azure container web app
        # Browser --HTTPS--> Reverse proxy --HTTP--> Flask, so flask is not able to detect it is actually serving https traffic.
        # See https://github.com/Azure-Samples/ms-identity-python-webapp/issues/18#issuecomment-604744997
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    return app
