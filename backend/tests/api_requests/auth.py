import json

from django import urls


def login(client, data):
    return client.post(
        urls.reverse('auth:api_v1:login'),
        data=json.dumps(data),
        content_type='application/json')


def logout(client):
    return client.post(urls.reverse('auth:api_v1:logout'))


def signup(client, data):
    return client.post(
        urls.reverse('auth:api_v1:job_seeker_signup'),
        data=json.dumps(data),
        content_type='application/json')


def get_current_user(client):
    return client.get(
        urls.reverse('auth:api_v1:user'),
        content_type='application/json'
    )


def update_current_user(client, data):
    return client.patch(
        urls.reverse('auth:api_v1:user'),
        data=json.dumps(data),
        content_type='application/json')


def update_user_password(client, data):
    return client.post(
        urls.reverse('auth:api_v1:password-change'),
        data=json.dumps(data),
        content_type='application/json')


def reset_user_password(client, data):
    return client.post(
        urls.reverse('auth:api_v1:password-reset'),
        data=json.dumps(data),
        content_type='application/json'
    )


def set_user_password(client, data):
    return client.post(
        urls.reverse('auth:api_v1:set-password'),
        data=json.dumps(data),
        content_type='application/json'
    )


def reset_user_password_confirm(client, data):
    return client.post(
        urls.reverse('auth:api_v1:password-reset-confirm'),
        data=json.dumps(data),
        content_type='application/json')


def signup_company_user(client, data):
    return client.post(
        urls.reverse('auth:api_v1:company_signup'),
        data=json.dumps(data),
        content_type='application/json')


def delete_account(client, data):
    return client.post(
        urls.reverse('auth:api_v1:delete-account'),
        data=json.dumps(data),
        content_type='application/json'
    )

def resend_restore_account(client, data):
    return client.post(
        urls.reverse('auth:api_v1:resend-restore-account-email'),
        data=json.dumps(data),
        content_type='application/json'
    )

def restore_account(client, data):
    return client.post(
        urls.reverse('auth:api_v1:restore-account'),
        data=json.dumps(data),
        content_type='application/json'
    )


def signup_invited_company_user(client, data):
    return client.post(
        urls.reverse('auth:api_v1:invited-company-user-sign-up'),
        data=json.dumps(data),
        content_type='application/json')


def get_all_permissions(client):
    return client.get(urls.reverse('auth:api_v1:all-permissions'))


def get_all_user_permissions(client):
    return client.get(urls.reverse('auth:api_v1:permissions'))


def sign_up_facebook(client, data):
    return client.post(
        urls.reverse('auth:api_v1:fb-login'),
        data=json.dumps(data),
        content_type='application/json')


def sign_up_google(client, data):
    return client.post(
        urls.reverse('auth:api_v1:google-login'),
        data=json.dumps(data),
        content_type='application/json')
