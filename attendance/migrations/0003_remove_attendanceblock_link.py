# Generated by Django 3.2.6 on 2021-08-16 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0002_alter_attendance_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendanceblock",
            name="link",
        ),
    ]
