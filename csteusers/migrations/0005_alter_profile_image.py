# Generated by Django 4.1 on 2022-08-26 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("csteusers", "0004_alter_profile_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="images/profile"),
        ),
    ]