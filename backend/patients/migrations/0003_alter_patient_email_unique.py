from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_alter_patient_email_alter_patient_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
