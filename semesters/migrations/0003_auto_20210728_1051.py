# Generated by Django 3.2.5 on 2021-07-28 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("semesters", "0002_auto_20210724_1721"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="semester",
            name="assn1",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="assn1_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="assn2",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="assn2_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="assn3",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="assn3_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="ext_grade_pts",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="ext_sub_credits",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="int1",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="int1_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="int2",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="int2_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz1",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz1_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz2",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz2_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz3",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="quiz3_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="sess",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="sess_max",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="sess_per",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="sgpa",
        ),
        migrations.CreateModel(
            name="SemesterBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("int1_max", models.FloatField(default=0)),
                ("int1", models.FloatField(default=0)),
                ("int2_max", models.FloatField(default=0)),
                ("int2", models.FloatField(default=0)),
                ("assn1_max", models.FloatField(default=0)),
                ("assn1", models.FloatField(default=0)),
                ("assn2_max", models.FloatField(default=0)),
                ("assn2", models.FloatField(default=0)),
                ("assn3_max", models.FloatField(default=0)),
                ("assn3", models.FloatField(default=0)),
                ("quiz1_max", models.FloatField(default=0)),
                ("quiz1", models.FloatField(default=0)),
                ("quiz2_max", models.FloatField(default=0)),
                ("quiz2", models.FloatField(default=0)),
                ("quiz3_max", models.FloatField(default=0)),
                ("quiz3", models.FloatField(default=0)),
                ("sess_max", models.FloatField(default=0)),
                ("sess", models.FloatField(default=0)),
                ("sess_per", models.FloatField(default=0)),
                ("ext_sub_credits", models.IntegerField(default=0)),
                ("ext_grade_pts", models.IntegerField(default=0)),
                ("sgpa", models.FloatField(blank=True, null=True)),
                (
                    "semester",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="semesters.semester"),
                ),
            ],
            options={
                "ordering": ["semester__student__roll_number", "-semester__semester"],
            },
        ),
    ]