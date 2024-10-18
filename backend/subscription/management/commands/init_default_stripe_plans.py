import stripe
from django.core.management import base

from subscription import models, constants


class Command(base.BaseCommand):
    """Create default system Stripe plans"""

    help = 'Create default system Stripe plans'

    def handle(self, *args, **options):
        for package in constants.DEFAULT_PLANS:
            stripe_product = stripe.Product.create(
                name=package['name'],
                type='service'
            )
            stripe_plan = stripe.Plan.create(
                nickname=package['name'],
                amount=package['price'] * constants.CENTS_IN_DOLLAR,
                product=stripe_product['id'],
                interval='month',
                currency=constants.USD_CURRENCY_ISO_CODE,
                metadata=package['metadata']
            )
            models.Plan.objects.create(
                stripe_id=stripe_plan['id'],
                name=stripe_plan['nickname'],
                job_seekers_count=package['metadata']['profile_views_number'],
                jobs_count=package['metadata']['job_postings_number'],
                price=package['price']
            )
            self.stdout.write(self.style.SUCCESS(
                'Plan {} was created'.format(package['name'])
            ))
