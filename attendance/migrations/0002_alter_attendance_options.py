# Generated by Django 3.2.5 on 2021-07-28 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="attendance",
            options={
                "ordering": ["attendance_block__semester__student", "-date"],
                "verbose_name_plural": "Attendance",
            },
        ),
    ]
