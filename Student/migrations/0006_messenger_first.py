# Generated by Django 3.0.3 on 2020-06-23 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0005_messenger_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='messenger',
            name='first',
            field=models.BooleanField(default=False),
        ),
    ]