# Generated by Django 4.1 on 2022-08-24 14:09

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cstebase", "0005_alter_question_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
