# Generated by Django 4.0.4 on 2022-06-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0002_ride'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
