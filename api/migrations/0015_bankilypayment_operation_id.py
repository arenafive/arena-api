# Generated by Django 3.2.12 on 2022-10-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_auto_20220908_2004"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankilypayment",
            name="operation_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
