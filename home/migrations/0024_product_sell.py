# Generated by Django 5.0.1 on 2024-03-30 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_brand_alter_category_options_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell',
            field=models.IntegerField(default=0),
        ),
    ]
