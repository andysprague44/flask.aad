import os
from jsoncomment import JsonComment
from datetime import datetime

FILE_PATH_ROOT = os.path.dirname(os.path.realpath(__file__))

# Load config
config = {}
json = JsonComment()
with open(os.path.join(FILE_PATH_ROOT, 'appsettings.Development.json')) as config_file:
    config = json.load(config_file)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


# App Settings
APP_VERSION = os.environ.get('APP_VERSION', config["app_version"])
PORT = os.environ.get('PORT', config["port"])
APPLICATION_ROOT_URI = os.environ.get('APPLICATION_ROOT_URI', config['application_root_uri'])
APPLICATION_HOME = os.environ.get('APPLICATION_HOME', config['application_home'])
REQUIRE_AUTHENTICATION = str2bool(os.environ.get('REQUIRE_AUTHENTICATION', config['require_authentication'])) #Obviously, should be true in prod

# AzureAD
TENANT = os.environ.get('TENANT', config["AzureAd"]["tenant"])
RESOURCE = os.environ.get('RESOURCE', config["AzureAd"]["resource"])
CLIENT_ID = os.environ.get('CLIENT_ID', config["AzureAd"]["client_id"])
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', config["AzureAd"]["client_secret"])
CALLBACK_PATH = '/auth/signin-oidc'
HTTPS_SCHEME = 'https' if APPLICATION_HOME.startswith('https') else 'http'
APPLICATION_REGISTRATION_DISPLAY_NAME = os.environ.get('APPLICATION_REGISTRATION_DISPLAY_NAME', config["AzureAd"]["application_registration_display_name"])

# Graph Api
GRAPH_RESOURCE = os.environ.get('GRAPH_RESOURCE', config["Graph"]["resource"])
GRAPH_BASE_URI = os.environ.get('GRAPH_BASE_URI', config["Graph"]["base_uri"])

# RapidAPI Rugby API
RAPIDAPI_KEY = config["RapidApiRugby"]["rapidapi-key"]
RAPIDAPI_HOST = config["RapidApiRugby"]["rapidapi-host"]

# Init config required by the authentication flask blueprint
AuthenticationConfig = {
    "TENANT": TENANT,
    "CLIENT_ID": CLIENT_ID,
    "CLIENT_SECRET": CLIENT_SECRET,
    "HTTPS_SCHEME": HTTPS_SCHEME,
    "AUTHORITY": f'https://login.microsoftonline.com/{TENANT}'
}

# Flask App Config
class FlaskConfig:
    """Set Flask config variables."""
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG=True,
    SECRET_KEY= os.environ.get('SECRET_KEY', config['flask_secret_key'])
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SESSION_TYPE = 'filesystem'  # Specifies the token cache should be stored in server-side session
