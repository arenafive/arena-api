# Generated by Django 3.2.12 on 2022-05-30 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_media"),
    ]

    operations = [
        migrations.AddField(
            model_name="arena",
            name="larg",
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name="arena",
            name="long",
            field=models.IntegerField(default=18),
        ),
    ]
