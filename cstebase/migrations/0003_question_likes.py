# Generated by Django 4.1 on 2022-08-24 04:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cstebase", "0002_alter_question_anonymous_alter_question_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="likes",
            field=models.ManyToManyField(
                related_name="question_post", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
