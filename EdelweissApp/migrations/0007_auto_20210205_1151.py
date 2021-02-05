# Generated by Django 3.1.5 on 2021-02-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EdelweissApp', '0006_auto_20210108_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hike',
            name='cumulativeElevation',
        ),
        migrations.AlterField(
            model_name='hike',
            name='thumbnail',
            field=models.ImageField(blank=True, default='', upload_to='img\\hikes\\'),
        ),
        migrations.AlterField(
            model_name='pointsofinterest',
            name='thumbnail',
            field=models.ImageField(blank=True, default='', upload_to='img\\poi\\'),
        ),
    ]
