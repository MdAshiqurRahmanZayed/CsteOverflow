# Generated by Django 4.1 on 2022-08-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("csteusers", "0003_remove_profile_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phone",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]