# Generated by Django 2.2 on 2019-04-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20190415_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='count_words',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='read_time',
            field=models.CharField(default=0, max_length=50),
        ),
    ]