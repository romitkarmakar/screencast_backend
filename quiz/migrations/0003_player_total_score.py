# Generated by Django 2.2.4 on 2019-08-15 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190812_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]