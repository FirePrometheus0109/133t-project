import enum


class LogEnum(enum.Enum):

    profile_purchase = 'purchased Candidate\'s profile.'
    candidate_assign = 'assigned Candidate to {}.'
    candidate_apply = 'Candidate applied for {}.'
    workflow_change = 'changed Candidate\'s status from {} to {} in {}'
    rate_change = 'changed Candidate\'s rate to {} in {}.'
    rate_remove = 'removed Candidate\'s rate in {}.'
    # NOTE profile save and schedule are not implemented
    profile_save = 'added profile to Saved.'
    schedule_screening = 'scheduled Screening with Candidate for {} in {}.'
    schedule_interview = 'scheduled Interview with Candidate for {} in {}.'
    comment_left = 'left a comment.'
    comment_edit = 'edited a comment.'
    comment_delete = 'deleted a comment.'
    job_create = 'created the job posting.'
    job_edit = 'edited the job posting.'
    job_delete = 'deleted the job posting.'
    job_status_change = 'changed status to {}.'
