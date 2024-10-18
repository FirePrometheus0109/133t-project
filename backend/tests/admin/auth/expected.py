BASE_USER_CREATION_FORM = [
    'username',
    'password1',
    'password2',
    'date_joined',
    'last_login',
]

JOB_SEEKER_CREATION_FORM = BASE_USER_CREATION_FORM

COMPANY_USER_CREATION_FORM = [
    'username',
    'password1',
    'password2',
    'company',
    'is_owner',
    'date_joined',
    'last_login',
]

BASE_USER_SORTABLE_FIELDS = (
    'username',
    'date_joined',
    'user_status'
)

BASE_USER_SEARCH_FIELDS = (
    'username',
    'date_joined',
    'first_name',
    'last_name',
    'email',
)

BASE_USER_FORM_FIELDS = [
    'password',
    'is_superuser',
    'groups',
    'user_permissions',
    'username',
    'first_name',
    'last_name',
    'email',
    'is_staff',
    'is_active',
    'date_joined',
    'last_login',
]

BASE_USER_FIELDSETS = (
    (None, {
        'fields': (
            'username',
            'password'
        )
    }),
    ('Personal info',
     {
         'fields': (
             'first_name',
             'last_name',
             'email')
     }),
    ('Permissions', {
        'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )
    }),
    ('Important dates',
     {
         'fields': (
             'last_login',
             'date_joined'
         )
     }
     ))

COMPANY_USER_INLINE_FIELDS = [
    'is_active',
    'ban_status',
    'user',
    'company',
    'status',
    'is_disabled_by_subscription',
    'candidate_statuses'
]

JOB_SEEKER_INLINE_FIELDS = [
    'is_active',
    'ban_status',
    'user',
    'about',
    'address',
    'phone',
    'photo',
    'position_type',
    'education',
    'clearance',
    'experience',
    'salary_min',
    'salary_max',
    'salary_public',
    'benefits',
    'travel',
    'skills',
    'is_public',
    'is_deleted',
    'industries',
    'is_shared'
]
