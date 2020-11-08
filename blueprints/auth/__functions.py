import adal
import uuid
import requests
import flask
from application import appsettings as config


def get_authentication_url(tenant: str,
                           client_id: str,
                           resource: str,
                           redirect_uri: str,
                           auth_state: str,
                           authority_host_uri: str = 'https://login.microsoftonline.com'):
    """Get a url that flask can use as the 'location' response header, to redirect the user to AAD login screen

    Args:
        tenant (str): GUID representing the Azure domain
        client_id (str): GUID representing the connecting application
        resource (str): URI representing the target application
        redirect_uri (str): redirect_uri to send user to after authentication, expect similar to 'https://<my app uri>/auth/signin-oidc'
        authority_host_uri (str): token provider url, 'https://login.microsoftonline.com' by default

    Returns:
        authorization_url (str): A url to AAD login page.
    """
    TEMPLATE_AUTHZ_URL = '{authority_host_uri}/{tenant}/oauth2/authorize?response_type=code&client_id={client_id}&resource={resource}&redirect_uri={redirect_uri}&state={auth_state}'
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        authority_host_uri=authority_host_uri,
        tenant=tenant,
        client_id=client_id,
        redirect_uri=redirect_uri,
        auth_state=auth_state,
        resource=resource)
    return authorization_url


def get_logout_url(tenant: str,
                   logout_redirect_uri: str,
                   authority_host_uri: str = 'https://login.microsoftonline.com'):
    """Get a url that flask can use as the 'location' response header, to redirect the user to AAD logout screen

    Args:
        tenant (str): GUID representing the Azure domain
        logout_redirect_uri (str): redirect_uri to send user to after logout, expect similar to 'https://<my app uri>/auth/logout-complete'
        authority_host_uri (str): token provider url, 'https://login.microsoftonline.com' by default

    Returns:
        authorization_url (str): A url to AAD logout page.
    """
    TEMPLATE_LOGOUT_URL = '{authority_host_uri}/{tenant}/oauth2/logout?post_logout_redirect_uri={logout_redirect_uri}'
    logout_url = TEMPLATE_LOGOUT_URL.format(
        authority_host_uri=authority_host_uri,
        tenant=tenant,
        logout_redirect_uri=logout_redirect_uri)
    return logout_url

def get_json(url: str, auth_token: dict, timeout: int = 180) -> requests.Response:
        """Performs a GET on the provided url and returns the result as json

        Args:
            url (str): url to GET
            auth_token (dict): token returned from interactive log-on, must contain 'accessToken' entry
            timeout (int): number of seconds to wait for connect and read timeout

        Returns:
            response (requests.Response): response

        """
        headers = {'Authorization': f'Bearer {auth_token["accessToken"]}', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
