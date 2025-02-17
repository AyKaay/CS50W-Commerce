# Generated by Django 5.0.6 on 2024-07-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_auctionlistings_bid_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlistings',
            name='seller_information',
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='bid_amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='buy_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='category',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='starting_bid',
            field=models.FloatField(),
        ),
    ]
