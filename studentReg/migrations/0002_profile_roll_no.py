# Generated by Django 3.0.3 on 2020-05-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentReg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Roll_No',
            field=models.CharField(default=18, max_length=9),
            preserve_default=False,
        ),
    ]