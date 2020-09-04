# Generated by Django 3.0.8 on 2020-08-08 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FAS', 'Fashion'), ('TOY', 'Toys'), ('ELE', 'Electronics'), ('HOM', 'Home'), ('OTH', 'Others')], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
