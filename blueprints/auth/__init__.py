
import adal
import uuid
import requests
import flask
from flask import Blueprint, render_template
from flask import current_app
from .user import GraphUser as User
from .__functions import get_authentication_url, get_logout_url


def construct_blueprint(auth_config: dict):
    """Get a blueprint for authentication, with routes at /auth/login and /auth/logout.
    
    Args:
        auth_config: dict containing auth config. Must contain keys:
            TENANT: AAD tenant aka directory, can be gui or name
            CLIENT_ID: Your application's client id aka "applicationID"
            CLIENT_SECRET: Your application's client secret aka "applicationKey"
            HTTPS_SCHEME: either 'https' or 'http', should always be 'https' in production
            AUTH_RESOURCE: the resource of the application that contains user roles
            AUTH_USER_INFO_ENDPOINT: the endpoint that returns the user's roles, on the application that contains user roles
            AUTH_APP_REG_DISPLAY_NAME: the display nanme of the app reg, for the application that contains user roles

    NOTE 'the application that contains user roles' is normally a seperate back-end service API for your application. For a stand alone web app, can use the MS Graph API.

    Returns:
        flask.Blueprint called 'auth'
    """
    required_keys = {
        'TENANT', 
        'CLIENT_ID',
        'CLIENT_SECRET',
        'HTTPS_SCHEME',
        'AUTH_RESOURCE',
        'AUTH_USER_INFO_ENDPOINT',
        'AUTH_APP_REG_DISPLAY_NAME'
    }
    intersection = required_keys & auth_config.keys()
    if len(intersection) != len(required_keys):
        missing_keys = required_keys - intersection
        raise ValueError('auth_config dict missing required keys: ' + ','.join(missing_keys))        

    bp = Blueprint('auth', __name__, template_folder='templates')

    # Register blueprint routes
    @bp.route('/hello')
    def hello():
        return '<h1>Hello auth blueprint</h1>'

    @bp.route("/login")
    def login():
        auth_state = str(uuid.uuid4())
        flask.session['state'] = auth_state
        redirect_uri = flask.url_for('.signin_oidc', _external=True, _scheme=auth_config['HTTPS_SCHEME'])
        authorization_url = get_authentication_url(
            auth_config['TENANT'],
            auth_config['CLIENT_ID'],
            auth_config['AUTH_RESOURCE'],
            redirect_uri,
            auth_state)
        resp = flask.Response(status=307)
        resp.headers['location'] = authorization_url
        return resp

    @bp.route("/signin-oidc")
    def signin_oidc():
        """
        This is the re-direct from the MS Auth template
        Here, we try and get an authentication token for calls to the API from the app.
        We then use the token to check the user has at least Read access
            - If we can, we save to the flask session for future use.
            - If we can't, we fail authentication

        Once complete, redirect to the home page
        """
        state = flask.request.args['state']
        if state != flask.session['state']:
            raise ValueError("State does not match")

        redirect_uri = flask.url_for('.signin_oidc', _external=True, _scheme=auth_config['HTTPS_SCHEME'])
        code = flask.request.args['code']

        context = adal.AuthenticationContext('https://login.microsoftonline.com/' + auth_config['TENANT'])
        token_response = context.acquire_token_with_authorization_code(
            code, 
            redirect_uri, 
            auth_config['AUTH_RESOURCE'], 
            auth_config['CLIENT_ID'], 
            auth_config['CLIENT_SECRET'])

        if not 'accessToken' in token_response:
            raise adal.AdalError("Authentication Failed - no 'accessToken' found in token_response = " + token_response)
        
        # Get and check user has at least read access to the app
        user = User(token_response, auth_config)
        
        if not user.has_read_access():
            raise adal.AdalError('Authentication Failed - You do not have at least read access to this application. Please ask support to grant it.')
        flask.session['user.displayName'] = user.display_name
        flask.session['user.email'] = user.email

        # Save the access token to the flask session for use by the app later
        flask.session['authToken.accessToken'] = token_response['accessToken']
        flask.session['authToken.refreshToken'] = token_response['refreshToken']
        flask.session['authToken.expiresOn'] = token_response['expiresOn']

        # Redirect to home page, authentication was successful
        current_app.logger.info(f'User authentication successful for {user.display_name}')
        return flask.redirect(flask.url_for('index'))

    # somewhere to logout
    @bp.route("/logout")
    def logout():
        current_app.logger.info(f'Logout requested')
        flask.session.clear()
        logout_redirect_uri = flask.url_for('.logout_complete', _external=True)
        logout_url = get_logout_url(auth_config['TENANT'], logout_redirect_uri)
        resp = flask.Response(status=307)
        resp.headers['location'] = logout_url
        return resp

    @bp.route("/logout-complete")
    def logout_complete():
        current_app.logger.info(f'Logout complete')
        return render_template("logout.html")
        #TODO drop simple response if template works
        #index = flask.url_for('index')
        #return flask.Response("<h1>Logout Complete</h1><br/><p><a href=\"{0}\">Click Here</a> to go to the Home Page</p>".format(index))
    
    return bp
