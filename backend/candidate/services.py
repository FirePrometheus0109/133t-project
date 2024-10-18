import itertools

from django.conf import settings
from django.db import models as orm

from job_seeker import models as js_models
from leet import utils as base_utils
from log import constants as log_constants
from log import utils as log_utils


class QuickListService:

    num_days = settings.NUMBER_DAYS_FOR_QUICK_LIST

    def __init__(self, queryset, user):
        self.queryset = queryset
        self.user = user
        self.worked_with_js = {}

    def _get_candidates_from_logs_by_log_type(self, action):
        candidates = log_utils.get_company_logs(
            self.user.company_user.company,
            content_type__model='jobseeker',
            type=action,
            owner=self.user,
            time__date__gte=base_utils.ago(self.num_days))
        return (candidates
                .annotate(
                    job_seeker_id=orm.F('object_id'),
                    worked_date=orm.F('time'))
                .values('job_seeker_id', 'worked_date'))

    def _get_changed_steps_candidates_job_seekers_qs(self):
        return self._get_candidates_from_logs_by_log_type(
            log_constants.LogEnum.workflow_change.name
        )

    def _get_viewed_candidates_job_seekers_qs(self):
        return (js_models.ViewJobSeeker
                         .objects
                         .filter(
                             company_user__user=self.user,
                             created_at__date__gte=base_utils.ago(
                                 self.num_days))
                         .annotate(worked_date=orm.F('created_at'))
                         .values('job_seeker_id', 'worked_date'))

    def _get_commented_candidates_job_seekers_qs(self):
        return self._get_candidates_from_logs_by_log_type(
            log_constants.LogEnum.comment_left.name
        )

    def _get_assigned_candidates_job_seekers_qs(self):
        return self._get_candidates_from_logs_by_log_type(
            log_constants.LogEnum.candidate_assign.name
        )

    def _get_filtered_candidates_queryset_user_worked_with(self):
        changed_steps_qs = self._get_changed_steps_candidates_job_seekers_qs()
        viewed_qs = self._get_viewed_candidates_job_seekers_qs()
        commented_js_qs = self._get_commented_candidates_job_seekers_qs()
        assigned_candidates_qs = self._get_assigned_candidates_job_seekers_qs()
        worked_with_chain = itertools.chain(
            changed_steps_qs,
            viewed_qs,
            commented_js_qs,
            assigned_candidates_qs
        )

        for entry in worked_with_chain:
            js_id = entry['job_seeker_id']
            worked_date = entry['worked_date']
            if (js_id not in self.worked_with_js or
                    worked_date > self.worked_with_js[js_id]['worked_date']):
                self.worked_with_js[js_id] = entry

        return self.queryset.filter(
            job_seeker_id__in=self.worked_with_js.keys())

    def get_data_for_quick_list(self):
        """
        Return data of candidates who company user has worked during 5 days:
            1. Changed candidate's workflow step.
            2. View candidate's profile's details.
            3. Left comments to candidate's profile.
        :param queryset: queryset of candidates.
        :param user: user object.
        :return: list of dicts.
        """
        result = []
        queryset = self._get_filtered_candidates_queryset_user_worked_with()
        for i in queryset:
            worked_date = self.worked_with_js[i.job_seeker.id]['worked_date']
            result.append({
                'status': {
                    'id': i.status.id,
                    'name': i.status.name
                },
                'user': {
                    'id': i.job_seeker.user.id,
                    'first_name': i.job_seeker.user.first_name,
                    'last_name': i.job_seeker.user.last_name
                },
                'job': {
                    'id': i.job.id,
                    'title': i.job.title
                },
                'id': i.id,
                'worked_date': worked_date
            })
        return sorted(result, key=lambda i: i['worked_date'], reverse=True)
