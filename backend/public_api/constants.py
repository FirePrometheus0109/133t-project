# pylint: disable=no-member
from leet import enums


LAST_UPDATE_WITH_DAYS_FRONT = {
    enums.LastUpdatedWithingDays.FIVE_DAYS.value: 'Within 5 days',
    enums.LastUpdatedWithingDays.TEN_DAYS.value: 'Within 10 days',
    enums.LastUpdatedWithingDays.FIFTEEN_DAYS.value: 'Within 15 days',
    enums.LastUpdatedWithingDays.THIRTY_DAYS.value: 'Within 30 days',
    enums.LastUpdatedWithingDays.SIXTY_DAYS.value: 'Within 60 days'
}

POSTED_DATE_WITH_DAYS_FRONT = LAST_UPDATE_WITH_DAYS_FRONT

PROFILE_IS_NOT_AVAILABLE_ERROR = (
    'Profile is not longer available.'
)
