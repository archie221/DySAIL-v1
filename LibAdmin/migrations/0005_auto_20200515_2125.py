# Generated by Django 3.0.3 on 2020-05-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibAdmin', '0004_auto_20200515_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticate',
            name='login',
            field=models.BooleanField(default=True),
        ),
    ]
