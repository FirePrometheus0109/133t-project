from django.core.management import base
import stripe

from subscription import models


class Command(base.BaseCommand):
    """
    Clear Stripe Plans, Products, Events, Subscriptions, Customers.
    Should be used only for testing purposes!
    """

    help = 'Clear Stripe Plans, Products, Events, Subscriptions, Customers'

    def handle(self, *args, **options):

        plans = stripe.Plan.list(limit=100)
        for plan in plans:
            plan.delete()
        products = stripe.Product.list(limit=100)
        for product in products:
            product.delete()
        subscriptions = stripe.Subscription.list(limit=100)
        for subscription in subscriptions:
            subscription.delete()
        customers = stripe.Customer.list(limit=100)
        for customer in customers:
            customer.delete()
        models.Subscription.objects.all().delete()
        models.Plan.admin_objects.all().delete()
        models.Customer.objects.all().delete()
        models.Balance.objects.all().delete()
