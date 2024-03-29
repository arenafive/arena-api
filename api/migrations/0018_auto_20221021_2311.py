# Generated by Django 3.2.12 on 2022-10-21 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_bankilypayment_operation_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="manager",
            old_name="exponent_push_token",
            new_name="android_exponent_push_token",
        ),
        migrations.RenameField(
            model_name="player",
            old_name="exponent_push_token",
            new_name="android_exponent_push_token",
        ),
        migrations.AddField(
            model_name="manager",
            name="ios_exponent_push_token",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="ios_exponent_push_token",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
