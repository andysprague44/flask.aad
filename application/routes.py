import flask
from flask import send_file, render_template, session
import os
import time
import traceback
import msal
from blueprints.auth.decorators import login_required
from .dashapp import get_layout
from . import appsettings as config
from .dashapp import get_layout
from flask import current_app as app


@app.route("/")
@login_required
def index():
    if config.REQUIRE_AUTHENTICATION:
        # Check user is authenticated
        try:
            user = flask.session['user']
            displayName = user.get('name', 'Unknown')
            app.logger.info(f'{displayName} logged in successfully')
        except Exception as ex:
            app.logger.error('Authentication failed: {ex}')
            raise Exception('Authentication failed. Please try again. ' + str(ex))
    
    # Load (dash) app
    #return render_template('index.html', user=session["user"], version=msal.__version__)
    return flask.redirect('dash/')


@app.errorhandler(404)
def not_found(e):
    app.logger.info('Page not found: ' + str(e))
    return render_template("404.html")


@app.errorhandler(Exception)
def internal_error(error):
    msg = f'Internal Server Error: {str(error)}'
    app.logger.error(msg)
    flask.flash(str(msg), "Error")

    if app.debug:
        trace = traceback.format_exc()
        app.logger.error(trace)
        msg = msg + '\n\n' + trace

    return render_template("500.html", error=error)


# @app.route('/favicon.ico')
# def favicon():
#     """
#     favicon.ico must be in the dash app assets folder to display when in dash
#     This route works for the flask only endpoints
#     """
#     return app.send_static_file('favicon.ico')
