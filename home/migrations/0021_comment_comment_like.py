# Generated by Django 5.0.1 on 2024-02-27 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_comment_reply'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_like',
            field=models.ManyToManyField(blank=True, related_name='com_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
