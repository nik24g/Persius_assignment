# Generated by Django 4.0 on 2021-12-31 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_comment_delete_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='winner',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]