# Generated by Django 4.1.3 on 2023-04-24 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("csteusers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="linkedIn",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
