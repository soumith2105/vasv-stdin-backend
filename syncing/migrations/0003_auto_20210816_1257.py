# Generated by Django 3.2.6 on 2021-08-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("syncing", "0002_auto_20210816_1206"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signup",
            name="attendance_pending",
            field=models.CharField(blank=True, default="", max_length=15),
        ),
        migrations.AlterField(
            model_name="signup",
            name="result_pending",
            field=models.CharField(blank=True, default="", max_length=15),
        ),
    ]
