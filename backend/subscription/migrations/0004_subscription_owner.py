# Generated by Django 2.1 on 2018-12-13 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_is_trial_available'),
        ('subscription', '0003_customer_add_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='company.CompanyUser'),
        ),
    ]
