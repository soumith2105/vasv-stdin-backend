# Generated by Django 3.2.6 on 2021-08-15 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0003_remove_student_last_refreshed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="current_status",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
