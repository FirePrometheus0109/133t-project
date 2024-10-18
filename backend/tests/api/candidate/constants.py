import datetime

from tests import utils


FROM_DATE = utils.date(2019, 1, 20)
TO_DATE = FROM_DATE + datetime.timedelta(days=5)
