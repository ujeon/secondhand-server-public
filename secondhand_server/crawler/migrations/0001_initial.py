# Generated by Django 2.2.5 on 2019-09-25 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Average_price',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=60)),
                ('model', models.CharField(max_length=60)),
                ('date', models.DateField()),
                ('average_price', models.IntegerField()),
                ('lowest_price', models.IntegerField()),
                ('highest_price', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Raw_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('price', models.IntegerField()),
                ('url', models.URLField()),
                ('img_url', models.TextField()),
                ('market', models.CharField(max_length=10)),
                ('posted_at', models.DateField()),
                ('is_sold', models.BooleanField()),
                ('location', models.CharField(max_length=60)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crawler.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Filtered_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=60)),
                ('model', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('url', models.URLField()),
                ('img_url', models.TextField()),
                ('market', models.CharField(max_length=10)),
                ('posted_at', models.DateField()),
                ('is_sold', models.BooleanField()),
                ('location', models.CharField(max_length=60)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crawler.Category')),
            ],
        ),
    ]
