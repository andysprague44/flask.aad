import flask
import adal
import requests
import uuid
from typing import List
from application import appsettings as config
from .__functions import get_json

class User:
    """
    User class for an app with a custom API, where the app roles can be retrieved from an end point on the back-end API e.g. /aad/user-info.
    
    Your back-end API must have an endpoint e.g. '../aad/user-info' that returns something like:
        {
            "lastName": "Sprague",
            "firstName": "Andrew",
            "email": "joebloggs@gmail.com",
            "userRoles": ["App.Read","App.Write","App.Admin"]
        }

    The auth_token in this case is a token for the back-end API.
    """
    def __init__(self, auth_token: dict, auth_config: dict = None):
        """Contruct user class to hold authentication info for the currently logged in user.
        
        Note this blueprint is used by client applications that do not have info on the user! 
        The authentication is 'pass-through' to a corresponding API that can return user info.
        
        Args:
            auth_token: token returned from interactive log-on, must contain 'accessToken' entry
            user_info_uri: Full uri to an API endpoint that can return user info, e.g. https://my-pai.azurewebsites.net/aad/user-info
        """
        user_info = self._get_user_info(auth_token, auth_config)

        if 'userRoles' in user_info:
            self._user_roles = user_info['userRoles']
        else:
            self._user_roles = []      
        
        if 'displayName' in user_info:
            self._display_name = user_info['displayName']
        elif 'firstName' in user_info and 'lastName' in user_info:
            self._display_name = f"{user_info['firstName']} {user_info['lastName']}"
        else:
            self._display_name = 'Unknown'
        
        if 'mail' in user_info:
            self._email = user_info['mail']
        elif 'email' in user_info:
            self._email = user_info['email']
        else:
            self._email = 'unknown@gmail.com'
    
    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_roles(self) -> List[str]:
        return self._user_roles

    def has_read_access(self) -> bool:
        return self.has_admin_access() or self.has_write_access() or any("READ" in role.upper() for role in self._user_roles)

    def has_write_access(self) -> bool:
        return self.has_admin_access() or any("WRITE" in role.upper() for role in self._user_roles)

    def has_admin_access(self) -> bool:
        return any("ADMIN" in role.upper() for role in self._user_roles)

    def _get_user_info(self, auth_token, auth_config):
        user_info_uri = auth_config['AUTH_USER_INFO_ENDPOINT']
        user_info = get_json(user_info_uri, auth_token)
        return user_info
    
    @staticmethod
    def from_flask_session(user_info_uri: str = None):
        auth_token = {
            'accessToken': flask.session['authToken.accessToken'],
            'refreshToken': flask.session['authToken.refreshToken'],
            'expiresOn': flask.session['authToken.expiresOn']
        }
        return User(auth_token, user_info_uri)


class GraphUser(User):
    """
    User class for a stand-alone app, where the app roles can be retrieved from MS Graph API.
    """
    def _get_user_info(self, auth_token, auth_config: dict):
        resourceDisplayName = auth_config['AUTH_APP_REG_DISPLAY_NAME']
        user_graph_app_role_data = get_json('https://graph.microsoft.com/v1.0/me/appRoleAssignments', auth_token)
        
        app_roles = [x['principalDisplayName'] for x in user_graph_app_role_data['value'] if x['resourceDisplayName'] == resourceDisplayName]

        user_graph_data = get_json('https://graph.microsoft.com/v1.0/me', auth_token)
        user_graph_data['userRoles'] = app_roles

        return user_graph_data

    def has_read_access(self) -> bool:
        return len(self._user_roles) > 0

    def has_write_access(self) -> bool:
        return False
    
    def has_admin_access(self) -> bool:
        return False
