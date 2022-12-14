# Generated by Django 4.1 on 2022-08-19 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("csteusers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="birthday",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="username",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
