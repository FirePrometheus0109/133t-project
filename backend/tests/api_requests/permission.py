from django import urls


def get_permissions_groups(client):
    return client.get(urls.reverse('permission:api_v1:permission-groups-list'))


def get_initial_permissions_groups(client):
    return client.get(
        urls.reverse(
            'permission:api_v1:initial-permission-groups-list'))
