# Generated by Django 3.2.6 on 2021-08-15 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0002_alter_student_branch"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="last_refreshed",
        ),
    ]