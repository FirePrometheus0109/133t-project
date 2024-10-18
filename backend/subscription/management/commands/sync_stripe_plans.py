import stripe
from django.core.management import base

from subscription import constants, models as s_models

FALSE_TEXT = "False"


class Command(base.BaseCommand):
    """
    Obtain plans from via Stripe API and create in db if they doesn't exist
    """

    help = ("Obtain plans from via Stripe API and create in db "
            "if they doesn't exist")

    def handle(self, *args, **options):
        if not s_models.Plan.objects.all().exists():
            stripe_plans = stripe.Plan.list(active=True)
            for stripe_plan in stripe_plans['data']:
                # Don't sync custom plans. If there are no plans in db
                # it means something went wrong and possibly
                # there are no customer that this plan belong to.
                if stripe_plan['metadata']['is_custom'] == FALSE_TEXT:
                    s_models.Plan.objects.create(
                        stripe_id=stripe_plan['id'],
                        name=stripe_plan['nickname'],
                        job_seekers_count=stripe_plan['metadata']['profile_views_number'],  # noqa
                        jobs_count=stripe_plan['metadata']['job_postings_number'],  # noqa
                        price=int(stripe_plan['amount']) / constants.CENTS_IN_DOLLAR  # noqa
                    )
