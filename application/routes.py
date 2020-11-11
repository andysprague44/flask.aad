import flask
from flask import send_file, render_template, session
import os
import time
import traceback
import msal
from blueprints.auth.decorators import login_required
from . import appsettings as config
from flask import current_app as app


@app.route("/")
@login_required
def index():
    # Probably don't need this additional check, but just in case!
    try:
        app.logger.info(f"{flask.session['user']['name']} logged in successfully")
    except Exception as ex:
        app.logger.error('No user found in the flask session. Did authentication fail? {ex}')
        raise

    # Load (dash) app
    #return render_template('index.html', user=session["user"], version=msal.__version__)
    return flask.redirect('/dash')


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
