# Generated by Django 5.0.2 on 2024-03-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                max_length=1,
                verbose_name="Gender",
            ),
        ),
    ]
