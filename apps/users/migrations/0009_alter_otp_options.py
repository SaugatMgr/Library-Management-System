# Generated by Django 5.0.8 on 2024-09-09 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otp',
            options={'verbose_name': 'OTP', 'verbose_name_plural': 'OTPs'},
        ),
    ]
