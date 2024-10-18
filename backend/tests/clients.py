import http

from django import urls
from rest_framework import test


class JWTClient(test.APIClient):

    login_url = urls.reverse('auth:api_v1:login')

    def login(self, **credentials):
        response = self.post(self.login_url, credentials, format='json')
        if response.status_code == http.HTTPStatus.OK:
            self.credentials(
                HTTP_AUTHORIZATION="JWT {}".format(response.data['token']))
            return True
        else:
            return False


class GoogleLoginClient(JWTClient):
    login_url = urls.reverse('auth:api_v1:google-login')


class FacebookLoginClient(JWTClient):
    login_url = urls.reverse('auth:api_v1:fb-login')
