# Generated by Django 5.0.2 on 2024-03-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_userprofile_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=10, unique=True, verbose_name="Phone No."
            ),
        ),
    ]
