# Generated by Django 2.1 on 2018-12-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0009_customer_auto_renew_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='is_payment_source_provided',
        ),
        migrations.AddField(
            model_name='customer',
            name='is_billing_info_provided',
            field=models.BooleanField(default=False, verbose_name='is_billing_info_provided'),
        ),
    ]
