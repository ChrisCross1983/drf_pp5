# Generated by Django 5.1.5 on 2025-04-07 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_comment_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
