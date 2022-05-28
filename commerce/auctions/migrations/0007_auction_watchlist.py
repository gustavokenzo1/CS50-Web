# Generated by Django 4.0.4 on 2022-05-27 18:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_current_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='watchlist',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
