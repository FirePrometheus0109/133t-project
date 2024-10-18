import enum


class ChoicesEnumMeta(enum.EnumMeta):
    @property
    def choices(cls):   # noqa
        return [(name.name, name.value) for name in cls]    # noqa

    def to_dict(cls):   # noqa
        return {name.name: name.value for name in cls}  # noqa


class ChoicesEnum(enum.Enum, metaclass=ChoicesEnumMeta):
    pass


class CustomEnumField:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ApplyStatusEnum(ChoicesEnum):
    APPLIED = 'Applied'
    NEED_REVIEW = 'Need review'
    VIEWED = 'Viewed'
    NEW = 'New'


class JobStatusEnum(ChoicesEnum):
    DRAFT = 'Draft'
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    DELAYED = 'Delayed'


class AutoapplyStatusEnum(ChoicesEnum):
    SAVED = 'Saved'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'
    STOPPED = 'Stopped'


class AuthGroupsEnum(ChoicesEnum):
    COMPANY_USER = 'company_user'
    JOB_SEEKER = 'job_seeker'


class CandidateTypeEnum(ChoicesEnum):
    """
    Currently it's enum for internal usage.
    Used to specify whether candidate was applied or assigned
    """
    ASSIGNED = "Assigned"
    APPLIED = "Applied"


class RatingEnum(ChoicesEnum):
    NO_RATING = 'No Rating'
    POOR = 'Poor'
    GOOD = 'Good'
    VERY_GOOD = 'Very good'
    EXCELLENT = 'Excellent'


class AppliedDateFilterEnum(ChoicesEnum):
    YESTERDAY = 'Yesterday'
    THIS_WEEK = 'This Week'
    LAST_WEEK = 'Last Week'
    THIS_MONTH = 'This Month'
    LAST_MONTH = 'Last Month'
    THIS_YEAR = 'This Year'
    LAST_YEAR = 'Last Year'


class CompanyUserStatusEnum(ChoicesEnum):

    NEW = 'New'
    ACTIVE = 'Active'
    DISABLED = 'Disabled'


class PositionTypesEnum(ChoicesEnum):
    FULL_TIME = "Full Time"
    PART_TIME = "Part Time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERNSHIP = "Internship"
    COMMISSION = "Commission"


class EducationTypesEnum(ChoicesEnum):
    HIGH_SCHOOL = "High School"
    CERTIFICATION = "Certification"
    ASSOCIATES_DEGREE = "Associates Degree"
    BACHELORS_DEGREE = "Bachelor's Degree"
    MASTERS_DEGREE = "Master's Degree"
    PHD = "PHD"
    NO_EDUCATION = 'No Education'


class CustomEnumMeta(type):
    @property
    def choices(cls):   # noqa
        return [(name.name, name.value) for name in cls]    # noqa

    def to_dict(cls):   # noqa
        return {name.name: name.value for name in cls}  # noqa

    def __iter__(cls):
        """Iterate over all upper case attributes."""
        # ToDo: Replace with a smarter solution
        return (getattr(cls, x) for x in cls.__dict__.keys() if x.isupper())    # noqa


class ClearanceTypesEnum(metaclass=CustomEnumMeta):
    NO_CLEARANCE = CustomEnumField(name=0, value="No Clearance")
    UNCLASSIFIED = CustomEnumField(name=1, value="Unclassified")
    CONFIDENTIAL = CustomEnumField(name=2, value="Confidential")
    MBI = CustomEnumField(name=3, value="MBI")
    PUBLIC_TRUST = CustomEnumField(name=4, value="Public Trust")
    SECRET = CustomEnumField(name=5, value="Secret")   # noqa
    TOP_SECRET = CustomEnumField(name=6, value="Top Secret")   # noqa
    TOP_SECRET_SCI = CustomEnumField(name=7, value="Top Secret/SCI")   # noqa


class ExperienceEnum(ChoicesEnum):
    NO_EXPERIENCE = "No experience"
    LESS_THAN_1 = "Less than 1 year"
    FROM_1_TO_2 = "1 to 2 years"
    FROM_3_TO_5 = "3 to 5 years"
    FROM_5_TO_10 = "5 to 10 years"
    MORE_THAN_10 = "10+ years"


class BenefitsEnum(ChoicesEnum):
    FULL_BENEFITS = "Full Benefits"
    PARTIAL_BENEFITS = "Partial Benefits"
    HEALTH = "Health"
    VISION = "Vision"
    HEALTH_AND_VISION = "Health & Vision"
    FOUR_OH_ONE_KEY = "401K"
    NO_BENEFITS = "No Benefits"


class TravelOpportunitiesEnum(ChoicesEnum):
    NO_TRAVEL = "No Travel"
    MINIMAL = "Minimal"
    TWENTY_FIVE_OR_LESS = "25% or Less"
    FIFTY_OR_LESS = "50% or Less"
    FIFTY_OR_MORE = "50% or More"


class JSTravelOpportunitiesEnum(ChoicesEnum):
    NO_TRAVEL = "No Travel"
    WILLING_TO_TRAVEL = "Willing To Travel"


class EmploymentEnum(ChoicesEnum):
    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'


class ActionEnum(ChoicesEnum):

    ADD = 'add'
    DELETE = 'delete'


class AnswerTypeEnum(ChoicesEnum):
    """
    Now is emplemented only YES_NO and PLAIN_TEXT types.
    On UI is used only Yes/No questions.
    """

    YES_NO = 'Yes/No'
    PLAIN_TEXT = 'Plain Text'
    SIMPLE_CHOICE = 'Simple Choice'
    MULTIPLE_CHOICE = 'Multiple Choice'


class YesNoAnswerEnum(ChoicesEnum):

    YES = 'Yes'
    NO = 'No'


class LastUpdatedWithingDays(ChoicesEnum):
    FIVE_DAYS = 5
    TEN_DAYS = 10
    FIFTEEN_DAYS = 15
    THIRTY_DAYS = 30
    SIXTY_DAYS = 60


class BanStatusEnum(ChoicesEnum):
    ACTIVE = 'Active'
    BANNED = 'Banned'


class UserTypeEnum(ChoicesEnum):
    ADMIN = '133T'
    COMPANY_USER = 'Company user'
    JOB_SEEKER = 'Job seeker'


class SubscriptionStatusEnum(ChoicesEnum):
    ACTIVE = 'Active'
    DRAFT = 'Draft'
    SCHEDULED = 'Scheduled'


class CustomPermissionReasonEnum(ChoicesEnum):
    SUBSCRIPTION_LIMIT = 'Subscription limit'


class WorkflowStepsCompanyStatFilters(ChoicesEnum):
    TWO_WEEKS = '2 weeks'
    THIRTY_DAYS = '30 days'
    SIXTY_DAYS = '60 days'


class EventAttendeeStatusEnum(ChoicesEnum):
    INVITED = 'Invited'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
