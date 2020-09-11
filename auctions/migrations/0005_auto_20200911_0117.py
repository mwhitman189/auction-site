# Generated by Django 3.1.1 on 2020-09-11 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='seller_id',
            new_name='seller',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='bidder_id',
            new_name='bidder',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commentor_id',
            new_name='commentor',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='seller_id',
            new_name='seller',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('', '--Category--'), ('BKS', 'Books'), ('BNI', 'Business & Industrial'), ('CSE', 'Clothing, Shoes & Accessories'), ('COL', 'Collectibles'), ('CEL', 'Consumer Electronics'), ('CFT', 'Crafts'), ('HNG', 'Home & Garden'), ('MTR', 'Motors'), ('PTS', 'Pet Supplies'), ('SPT', 'Sporting Goods'), ('SPM', 'Sports Mem, Cards & Fan Shop'), ('TNH', 'Toys & Hobbies'), ('ATQ', 'Antiques'), ('CNN', 'Computers/Tablets & Networking')], max_length=3),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='img',
            field=models.URLField(blank=True),
        ),
    ]
