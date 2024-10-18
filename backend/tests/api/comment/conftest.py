import pytest
from faker import Faker


fake = Faker()


@pytest.fixture
def comment_base_data(job_seeker):
    return {
        'title': fake.word(),
        'comment': fake.sentence()
    }
