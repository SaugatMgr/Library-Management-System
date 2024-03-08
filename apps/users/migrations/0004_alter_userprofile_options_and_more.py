# Generated by Django 5.0.2 on 2024-03-08 14:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_userprofile_gender"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userprofile",
            options={
                "verbose_name": "User Profile",
                "verbose_name_plural": "User Profile",
            },
        ),
        migrations.RenameField(
            model_name="userprofile",
            old_name="profile_pictue",
            new_name="profile_picture",
        ),
    ]
