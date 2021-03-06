# Generated by Django 4.0.4 on 2022-06-02 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('derparture', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('schedule', models.CharField(max_length=100)),
                ('seats', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('passengers', models.ManyToManyField(related_name='passengers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
