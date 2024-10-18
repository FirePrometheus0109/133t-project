from company import validators as company_validators
from job import services as job_services
from leet import services as base_services
from subscription import models
from log import constants as log_constants
from log import utils as log_utils


class CompanyService:

    def __init__(self, company):
        self.company = company

    def purchase_job_seeker(self, company_user, job_seeker):
        company_balance = (models.Balance.objects
                           .select_for_update()
                           .get(customer=self.company.customer))

        company_validators.validate_job_seeker_is_not_purchased_or_applied(
            self.company, job_seeker)
        company_validators.validate_job_seeker_profile_is_public(job_seeker)
        company_validators.validate_company_job_seeker_balance(self.company)
        company_balance.job_seekers_remain -= 1
        company_balance.save()
        self.company.purchased_job_seekers.add(job_seeker)
        # delete profile from saved for all company users
        (job_seeker.savedjobseeker_set
                   .filter(company_user__company=self.company)
                   .delete())
        log_utils.create_log(
            company_user.user,
            log_constants.LogEnum.profile_purchase.name,
            log_constants.LogEnum.profile_purchase.value,
            job_seeker
        )

    def ban_company_entities(self):
        """Ban all related to company entities"""
        base_services.ban_entities(self.get_company_users())
        job_services.ban_company_jobs(self.company)

    def unban_company_entities(self):
        """Unban all related to company entities"""
        base_services.unban_entities(self.get_company_users())
        job_services.unban_company_jobs(self.company)

    def get_company_users(self):
        return self.company.company_users.all()
