# pylint: disable=no-member
from django.db import models as orm
from django.core.validators import MaxValueValidator, MinValueValidator

from leet import enums
from leet import models


class StripeBaseModel(models.BaseModel):
    stripe_id = orm.CharField('stripe_id', unique=True, max_length=255)

    class Meta:
        abstract = True


class Customer(StripeBaseModel):
    company = orm.OneToOneField(
        'company.Company',
        on_delete=orm.CASCADE,
        related_name='customer'
    )
    balance = orm.OneToOneField(
        'subscription.Balance',
        on_delete=orm.CASCADE
    )
    is_billing_info_provided = orm.BooleanField(
        'is_billing_info_provided',
        default=False
    )
    auto_renew_subscription = orm.BooleanField(
        'auto_renew_subscription',
        default=False
    )


class Plan(StripeBaseModel):
    name = orm.CharField('name', max_length=255)
    job_seekers_count = orm.PositiveIntegerField()
    jobs_count = orm.PositiveIntegerField()
    is_custom = orm.BooleanField(default=False)
    company = orm.ForeignKey(
        'company.Company',
        on_delete=orm.CASCADE,
        null=True,
        blank=True
    )
    price = orm.DecimalField(max_digits=12, decimal_places=2)
    # Use additional fields to keep price changes because
    # of users notifications 3 months before and "scheduling"
    # of price changes. Admin can update only price field.
    # The same for deletion information.
    new_price = orm.DecimalField(max_digits=12, decimal_places=2,
                                 null=True, blank=True)
    price_apply_date = orm.DateTimeField(null=True, blank=True)
    is_deleted = orm.BooleanField(default=False)
    deletion_date = orm.DateTimeField(null=True, blank=True)
    is_reporting_enabled = orm.BooleanField(default=False)
    users_number = orm.SmallIntegerField(default=1,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
    )

    admin_objects = orm.Manager()

    def __str__(self):
        return self.name


class Subscription(StripeBaseModel):
    stripe_id = orm.CharField(
        'stripe_id',
        blank=True,
        null=True,
        max_length=255
    )
    plan = orm.ForeignKey(
        'subscription.Plan',
        on_delete=orm.PROTECT,
        related_name='subscriptions',
        null=True,
        blank=True
    )
    next_subscription = orm.ForeignKey(
        'subscription.Subscription',
        null=True,
        blank=True,
        on_delete=orm.SET_NULL
    )
    customer = orm.ForeignKey(
        'subscription.Customer',
        on_delete=orm.CASCADE,
        related_name='subscriptions'
    )
    is_trial = orm.BooleanField(default=False)
    date_start = orm.DateTimeField(blank=True, null=True)
    date_end = orm.DateTimeField(blank=True, null=True)
    is_auto_renew = orm.BooleanField(default=False)
    owner = orm.ForeignKey(
        'company.CompanyUser',
        on_delete=orm.CASCADE
    )
    status = orm.CharField(
        max_length=40,
        choices=enums.SubscriptionStatusEnum.choices,
        default=enums.SubscriptionStatusEnum.DRAFT.name
    )

    class Meta:
        unique_together = ('customer', 'status',)


class Balance(models.BaseModel):
    job_seekers_remain = orm.PositiveIntegerField(default=0)
    job_seekers_total = orm.PositiveIntegerField(default=0)
    jobs_remain = orm.PositiveIntegerField(default=0)
    jobs_total = orm.PositiveIntegerField(default=0)


class Invoice(StripeBaseModel):
    """Model that used for customers transactions reports"""
    customer = orm.ForeignKey('subscription.Customer', on_delete=orm.CASCADE,
                              related_name='invoices')
    amount = orm.DecimalField(max_digits=12, decimal_places=2)
    datetime_of_payment = orm.DateTimeField()
    description = orm.CharField(max_length=255, null=True, blank=True)
