# Generated by Django 5.0.7 on 2025-02-24 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flashcards", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="phrasepair",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
