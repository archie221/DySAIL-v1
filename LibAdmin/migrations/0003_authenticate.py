# Generated by Django 3.0.3 on 2020-05-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('LibAdmin', '0002_delete_passkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='authenticate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.BooleanField(default=False)),
            ],
        ),
    ]
