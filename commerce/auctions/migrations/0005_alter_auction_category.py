# Generated by Django 4.0.4 on 2022-05-27 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], max_length=100),
        ),
    ]
