# Generated by Django 4.1 on 2022-09-17 05:32

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("cstebase", "0011_rename_about_aboutpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="teammember",
            name="about",
            field=models.TextField(),
        ),
    ]