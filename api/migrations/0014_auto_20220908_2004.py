# Generated by Django 3.2.12 on 2022-09-08 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_arenafivesettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankilypayment",
            name="transaction_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="paymentgame",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to="api.payment",
            ),
        ),
    ]
