# Generated by Django 3.2.12 on 2022-06-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_auto_20220530_0016"),
    ]

    operations = [
        migrations.AddField(
            model_name="arena",
            name="price",
            field=models.IntegerField(default=5000),
        ),
    ]
