# Generated by Django 5.0.2 on 2024-04-02 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0008_reservequeue"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservequeue",
            options={
                "verbose_name": "Reserve Queue",
                "verbose_name_plural": "Reserve Queue",
            },
        ),
        migrations.AlterField(
            model_name="reservequeue",
            name="book",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reserve_queue",
                to="books.book",
            ),
        ),
    ]