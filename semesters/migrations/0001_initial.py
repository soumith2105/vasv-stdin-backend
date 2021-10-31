# Generated by Django 3.2.2 on 2021-05-11 22:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Semester",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("semester", models.IntegerField()),
                ("year", models.CharField(default="NA", max_length=15)),
                ("result_link", models.URLField(default="http://vce.ac.in/", max_length=300)),
                ("attendance_link", models.URLField(default="http://vce.ac.in/", max_length=300)),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField(auto_now_add=True)),
                ("int1_max", models.FloatField(default=0)),
                ("int1", models.FloatField(default=0)),
                ("int1_per", models.FloatField(default=0)),
                ("int2_max", models.FloatField(default=0)),
                ("int2", models.FloatField(default=0)),
                ("int2_per", models.FloatField(default=0)),
                ("assn1_max", models.FloatField(default=0)),
                ("assn1", models.FloatField(default=0)),
                ("assn1_per", models.FloatField(default=0)),
                ("assn2_max", models.FloatField(default=0)),
                ("assn2", models.FloatField(default=0)),
                ("assn2_per", models.FloatField(default=0)),
                ("assn3_max", models.FloatField(default=0)),
                ("assn3", models.FloatField(default=0)),
                ("assn3_per", models.FloatField(default=0)),
                ("quiz1_max", models.FloatField(default=0)),
                ("quiz1", models.FloatField(default=0)),
                ("quiz1_per", models.FloatField(default=0)),
                ("quiz2_max", models.FloatField(default=0)),
                ("quiz2", models.FloatField(default=0)),
                ("quiz2_per", models.FloatField(default=0)),
                ("quiz3_max", models.FloatField(default=0)),
                ("quiz3", models.FloatField(default=0)),
                ("quiz3_per", models.FloatField(default=0)),
                ("sess_max", models.FloatField(default=0)),
                ("sess", models.FloatField(default=0)),
                ("sess_per", models.FloatField(default=0)),
                ("ext_sub_credits", models.IntegerField(default=0)),
                ("ext_grade_pts", models.IntegerField(default=0)),
                ("sgpa", models.FloatField(blank=True, null=True)),
                (
                    "student",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["student__roll_number", "-semester"],
            },
        ),
    ]