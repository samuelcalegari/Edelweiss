# Generated by Django 3.1.5 on 2021-01-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EdelweissApp', '0003_auto_20210108_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hike',
            name='thumbnail',
            field=models.ImageField(default='images/no-img.png', upload_to='static/'),
        ),
    ]