# Generated by Django 5.0.1 on 2024-02-19 18:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_product_like_product_unlike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='information',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
