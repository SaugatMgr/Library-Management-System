# Generated by Django 5.0.8 on 2025-01-23 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_borrow_overdue_finepayment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrow',
            options={'ordering': ['-borrowed_date']},
        ),
    ]
