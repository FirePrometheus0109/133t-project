from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_candidate_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='previous_status',
            field=models.CharField(blank=True, max_length=16, verbose_name='previous status'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('APPLIED', 'Applied'), ('SCREENED', 'Screened'), ('INTERVIEWED', 'Interviewed'), ('OFFERED', 'Offered'), ('HIRED', 'Hired'), ('REJECTED', 'Rejected')], default='APPLIED', max_length=16, verbose_name='status'),
        ),
    ]
