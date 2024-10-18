import pytest

from leet import admin as base_admin


class MockRequest:
    GET = {}

    def update_request_type(self, value):
        self.GET['type'] = value


class MockSuperUser:

    def has_perm(self, perm):
        return True


@pytest.fixture
def admin_request():
    request = MockRequest()
    request.user = MockSuperUser()
    return request


@pytest.fixture
def admin_site():
    return base_admin.base_admin_site
