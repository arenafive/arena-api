# Generated by Django 3.2.12 on 2022-10-11 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_auto_20221010_2322"),
    ]

    operations = [
        migrations.AddField(
            model_name="arenafivesettings",
            name="bankily_merchant_id",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
