# Generated by Django 3.0.3 on 2020-05-26 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_auto_20200522_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='gadget',
            name='taken',
            field=models.BooleanField(default=False),
        ),
    ]
