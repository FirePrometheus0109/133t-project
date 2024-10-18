import enum


MANAGE_COMPANY_USERS_GROUP = 'Manage company users'
MANAGE_JOB_POSTINGS_GROUP = 'Manage job postings'
MANAGE_REPORTS_GROUP = 'Working with reports'
# TODO (i.bogretsov) delete unused groups
EDIT_CALENDAR_GROUP = 'Edit other user\'s calendar'
EDIT_COMPANY_CALENDAR_GROUP = 'Edit company calendar'
EDIT_COMPANY_PROFILE_GROUP = 'Edit company profile'
MANAGE_SUBSCRIPTION_PLAN_GROUP = 'Manage Subscription plan'
MANAGE_LETTER_TEMPLATE_GROUP = 'Manage letter templates'
MANAGE_CANDIDATE_COMMENTS_GROUP = 'Manage comments in the candidates profile'
VIEW_CREATE_CANDIDATE_COMMENTS_GROUP = 'View and add comments in the profiles'
MANAGE_JOB_COMMENTS_GROUP = 'Manage comments in the job posting'
VIEW_CREATE_JOB_COMMENTS_GROUP = 'View and add comments in the job postings'
DELETE_LOG_GROUP = 'Delete log entry'
PURCHASE_JSPROFILE_GROUP = 'Purchase Job seeker\'s profile'
CREATE_CALENDAR_EVENT_GROUP = 'Create Calendar Event'
MANAGE_CALENDAR_EVENT_GROUP = 'Manage Calendar Event'

CAN_NOT_DISABLE_IF_ONLY_ONE_USER_IN_GROUP = [
    MANAGE_COMPANY_USERS_GROUP,
    MANAGE_SUBSCRIPTION_PLAN_GROUP
]

INITIAL_INVITED_COMPANY_USERS_PERMISSIONS_GROUPS = [
    MANAGE_JOB_POSTINGS_GROUP,
    MANAGE_LETTER_TEMPLATE_GROUP,
    VIEW_CREATE_CANDIDATE_COMMENTS_GROUP,
    VIEW_CREATE_JOB_COMMENTS_GROUP,
    PURCHASE_JSPROFILE_GROUP
]

PERMISSION_GROUPS = [
    {
        'title': 'User',
        'name': MANAGE_COMPANY_USERS_GROUP,
        'description': 'View users list, invite new users, '
                       'edit user\'s account, enable/disable account,'
                       ' change permissions, delete account.'
    },
    {
        'title': 'Job',
        'name': MANAGE_JOB_POSTINGS_GROUP,
        'description': 'Create, edit, delete job postings of your Company '
                       '(created by anyone). '
                       '*User always has a possibility to '
                       'edit and delete his own job postings.'
    },
    {
        'title': 'Report',
        'name': MANAGE_REPORTS_GROUP,
        'description': 'Access to Reports sections.'
    },
    {
        'title': 'Other user\'s calendar',
        'name': EDIT_CALENDAR_GROUP,
        'description': 'TBD: Edit interviews, screening, availability in '
                       'the calendar of other user.'
    },
    {
        'title': 'Company calendar',
        'name': EDIT_COMPANY_CALENDAR_GROUP,
        'description': 'TBD: Edit interviews, screening, '
                       'availability in the company calendar.'
    },
    {
        'title': 'Company profile',
        'name': EDIT_COMPANY_PROFILE_GROUP,
        'description': 'Edit information in Company profile.'
    },
    {
        'title': 'Subscription plan and Payment',
        'name': MANAGE_SUBSCRIPTION_PLAN_GROUP,
        'description': 'Select subscription plan, '
                       'renew subscription plan, make payments.'
    },
    {
        'title': 'Letters templates',
        'name': MANAGE_LETTER_TEMPLATE_GROUP,
        'description': 'Create, edit and delete letters templates.'
    },
    {
        'title': 'Comment in the candidates profile',
        'name': MANAGE_CANDIDATE_COMMENTS_GROUP,
        'description': 'Full access to working with comments: view comments, '
                       'add new comments, edit and delete comments '
                       'under candidate\'s profile.'
    },
    {
        'title': 'Comment in the candidates profile',
        'name': VIEW_CREATE_CANDIDATE_COMMENTS_GROUP,
        'description': 'View comments, add new comments under candidate\'s '
                       'profile.'
    },
    {
        'title': 'Comment in the job post',
        'name': MANAGE_JOB_COMMENTS_GROUP,
        'description': 'Full access to working with comments: view comments, '
                       'add new comments, edit and delete '
                       'comments under job posting.'
    },
    {
        'title': 'Comment in the job post',
        'name': VIEW_CREATE_JOB_COMMENTS_GROUP,
        'description': 'View comments, add new comments under job posting.'
    },
    {
        'title': 'Logs',
        'name': DELETE_LOG_GROUP,
        'description': 'Delete separate log '
                       'entries in job postings and candidates profiles.'
    },
    {
        'title': 'Purchase Job seeker\'s profile',
        'name': PURCHASE_JSPROFILE_GROUP,
        'description': 'Select to purchase '
                       'candidate\'s profile (contact info).'
    },
    {
        'title': 'Create events.',
        'name': CREATE_CALENDAR_EVENT_GROUP,
        'description': 'Create new events in company calendar. '
                       'User can edit and delete his events in calendar.'
    },
    {
        'title': 'Manage calendar events.',
        'name': MANAGE_CALENDAR_EVENT_GROUP,
        'description': 'Manage events in company calendar. '
                       'User can edit and delete all events in calendar.'
    }
]


class Permissions(enum.Enum):
    add_job = ('add_job', 'Can add job')
    view_job = ('view_job', 'Can view job')
    change_job = ('change_job', 'Can change job')
    delete_job = ('delete_job', 'Can delete job')
    view_viewjob = ('view_viewjob', 'Can view view job')
    restore_job = ('restore_job', 'Can restore job')
    export_job_csv = ('export_job_csv', 'Can export jobs as csv')
    create_delayed_job = ('create_delayed_job', 'Create delayed jobs')
    set_job_is_cover_letter_required = ('set_job_is_cover_letter_required',
                                        'Can set `is cover_letter required`')
    set_job_closing_date = ('set_job_closing_date', 'Can set closing date')

    add_companyuser = ('add_companyuser', 'Can add company user')
    change_companyuser = ('change_companyuser', 'Can change company user')
    view_companyuser = ('view_companyuser', 'Can view company user')
    delete_companyuser = ('delete_companyuser', 'Can delete company user')

    change_company = ('change_company', 'Can change company')
    view_company = ('view_company', 'Can view company')
    change_company_logo = ('change_company_logo', 'Can change company logo')

    add_report = ('add_report', 'Can add report')
    change_report = ('change_report', 'Can change report')
    delete_report = ('delete_report', 'Can delete report')
    view_report = ('view_report', 'Can view report')

    add_event = ('add_event', 'Can add event')
    view_event = ('view_event', 'Can view event')
    change_event = ('change_event', 'Can change event')
    delete_event = ('delete_event', 'Can delete event')
    view_eventtype = ('view_eventtype', 'Can view event type')
    check_another_event = ('check_another_event', 'Can check another event')

    delete_log = ('delete_log', 'Can delete log')
    view_log = ('view_log', 'Can view log')

    add_lettertemplate = ('add_lettertemplate', 'Can add letter template')
    view_lettertemplate = ('view_lettertemplate', 'Can view letter template')
    change_lettertemplate = (
        'change_lettertemplate', 'Can change letter template')
    delete_lettertemplate = (
        'delete_lettertemplate', 'Can delete letter template')

    add_jobseekercomment = (
        'add_jobseekercomment', 'Can add comment')
    view_jobseekercomment = (
        'view_jobseekercomment', 'Can view comment')
    change_jobseekercomment = (
        'change_jobseekercomment', 'Can change comment')
    delete_jobseekercomment = (
        'delete_jobseekercomment', 'Can delete comment')

    add_jobcomment = ('add_jobcomment', 'Can add comment')
    view_jobcomment = ('view_jobcomment', 'Can view comment')
    change_jobcomment = ('change_jobcomment', 'Can change comment')
    delete_jobcomment = ('delete_jobcomment', 'Can delete comment')

    purchase_subscription = (
        'purchase_subscription_plan', 'Can purchase subscription plan')
    view_active_subscription = (
        'view_active_subscription', 'Can view active subscription')

    purchase_js_profile = ('purchase_js_profile', 'Can purchase js_profile')
    view_purchased_job_seekers = (
        'view_purchased_job_seekers', 'Can view purchased job seekers')

    add_question = ('add_question', 'Can add question')
    view_question = ('view_question', 'Can view question')
    change_question = ('change_question', 'Can change question')
    delete_question = ('delete_question', 'Can delete question')

    add_survey = ('add_survey', 'Can add survey')
    view_survey = ('view_survey', 'Can view survey')
    change_survey = ('change_survey', 'Can change survey')
    delete_survey = ('delete_survey', 'Can delete survey')

    add_answerjobseeker = ('add_answerjobseeker', 'Can add answer job seeker')
    view_answerjobseeker = (
        'view_answerjobseeker', 'Can view answer job seeker')

    view_autoapply_jobs = ('view_autoapply_jobs', 'Can view jobs of autoapply')
    view_autoapply_job_detail = (
        'view_autoapply_job_detail', 'Can view job details of autoapply')
    add_autoapply = ('add_autoapply', 'Can add autoapply')
    view_autoapply = ('view_autoapply', 'Can view autoapply')
    change_autoapply = ('change_autoapply', 'Can change autoapply')
    delete_autoapply = ('delete_autoapply', 'Can delete autoapply')
    start_autoapply = ('start_autoapply', 'Can start autoapply')
    stop_autoapply = ('stop_autoapply', 'Can stop autoapply')
    restart_autoapply = ('restart_autoapply', 'Can restart autoapply')
    autoapply_to_job = ('autoapply_to_job', 'Can autoapply to job')
    share_job = ('share_job', 'Can share job by email')
    view_applied_jobs = ('view_applied_jobs', 'Can view applied jobs')
    add_apply = ('add_apply', 'Can add apply')
    do_reapply = ('do_reapply', 'Can do reapply')
    view_autoapply_stats = ('view_autoapply_stats', 'Can view autoapply stats')
    view_job_candidates = ('view_job_candidates', 'Can view job candidates')

    view_jobseeker = ('view_jobseeker', 'Can view job seeker')
    change_jobseeker = ('change_jobseeker', 'Can change job seeker')
    delete_jobseeker = ('delete_jobseeker', 'Can delete job seeker')
    upload_photo = ('upload_photo', 'Can upload Photo')

    add_jobexperience = ('add_jobexperience', 'Can add job experience')
    view_jobexperience = ('view_jobexperience', 'Can view job experience')
    change_jobexperience = (
        'change_jobexperience', 'Can change job experience')
    delete_jobexperience = (
        'delete_jobexperience', 'Can delete job experience')

    add_education = ('add_education', 'Can add education')
    view_education = ('view_education', 'Can view education')
    change_education = ('change_education', 'Can change education')
    delete_education = ('delete_education', 'Can delete education')

    add_document = ('add_document', 'Can add document')
    view_document = ('view_document', 'Can view document')
    delete_document = ('delete_document', 'Can delete document')

    add_certification = ('add_certification', 'Can add certification')
    view_certification = ('view_certification', 'Can view certification')
    change_certification = ('change_certification', 'Can change certification')
    delete_certification = ('delete_certification', 'Can delete certification')

    add_coverletter = ('add_coverletter', 'Can add cover letter')
    view_coverletter = ('view_coverletter', 'Can view cover letter')
    change_coverletter = (
        'change_coverletter', 'Can change cover letter')
    delete_coverletter = (
        'delete_coverletter', 'Can delete cover letter')

    add_savedjob = ('add_savedjob', 'Can add saved job')
    view_savedjob = ('view_savedjob', 'Can view saved job')
    view_permissiongroup = (
        'view_permissiongroup', 'Can view permission group')

    is_job_seeker = ('is_job_seeker', 'Can be job seeker')
    is_company_user = ('is_company_user', 'Can be company user')

    add_candidate = ('add_candidate', 'Can add candidate')
    view_candidate = ('view_candidate', 'Can view candidate')
    change_candidate = ('change_candidate', 'Can change candidate')
    delete_candidate = ('delete_candidate', 'Can delete candidate')
    can_rate_candidate = ('can_rate_candidate', 'Can rate candidate')
    export_candidate_csv = ('export_candidate_csv',
                            'Can export candidates to csv')
    change_candidatestatus = (
        'change_candidatestatus', 'Can change candidate status')
    restore_candidate = ('restore_candidate', 'Can restore candidate')
    view_workflowstep_stats = (
        'view_workflowstep_stats', 'Can view workflow step stats')

    view_viewjobseeker = (
        'view_viewjobseeker', 'Can view view job seeker')
    change_viewed_candidate_statuses = (
        'change_viewed_candidate_statuses',
        'Can change viewed candidate statuses'
    )
    view_notificationtype = (
        'view_notificationtype', 'Can view notification type'
    )
    manage_notifications = (
        'manage_notifications', 'Can manage notifications'
    )
    view_candidate_activity = (
        'view_candidate_activity', 'Can view candidate activity'
    )
    view_quick_list = ('view_quick_list', 'Can view quick list')
    add_savedjobseeker = (
        'add_savedjobseeker', 'Can add saved job seeker'
    )
    view_company_user_enum = (
        'view_company_user_enum', 'Can view company user enum'
    )
    view_candidate_enum = ('view_candidate_enum', 'Can view candidate enum')
    view_job_enum = ('view_job_enum', 'Can view job enum')


STARTER_SUBSCRIPTION_RESTRICTED_PERMS = (
    'comment.add_jobcomment',
    'comment.change_jobcomment',
    'comment.delete_jobcomment',
    'comment.add_jobseekercomment',
    'comment.change_jobseekercomment',
    'comment.delete_jobseekercomment',
    'candidate.add_candidate',
    'candidate.delete_candidate',
    'job_seeker.purchase_js_profile',
    'company.add_companyuser',
    'company.change_companyuser',
    'company.delete_companyuser',
    'job.create_delayed_job',
    'job.set_job_is_cover_letter_required',
    'job.set_job_closing_date'
)
