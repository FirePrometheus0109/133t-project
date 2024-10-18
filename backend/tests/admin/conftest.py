import pytest

from tests import factories


@pytest.fixture
def admin_user(db):
    return factories.create_base_user(is_staff=True, is_superuser=True)
