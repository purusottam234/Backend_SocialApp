# Generated by Django 4.2.1 on 2023-07-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0003_alter_user_created_alter_user_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
