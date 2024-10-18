from tests import utils

EXPECTED_AUTOAPPLIES_STATS = [
    {
      'id': utils.Any(int),
      'title': '30My autoapply',
      'applied_jobs_cnt': 1,
      'progress_percents': 3
    },
    {
      'id': utils.Any(int),
      'title': '25My autoapply',
      'applied_jobs_cnt': 1,
      'progress_percents': 4
    },
    {
      'id': utils.Any(int),
      'title': '4My autoapply',
      'applied_jobs_cnt': 1,
      'progress_percents': 25
    }
]
