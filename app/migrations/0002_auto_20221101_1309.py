# Generated by Django 3.2.16 on 2022-11-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="order",
            name="order_state_valid",
        ),
        migrations.AlterField(
            model_name="order",
            name="state",
            field=models.CharField(max_length=30),
        ),
    ]
