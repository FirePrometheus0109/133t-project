import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('job_seeker', '0028_auto_20190218_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4,
                                   editable=False,
                                   unique=True),
        ),
    ]
