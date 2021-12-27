# Generated by Django 3.2.8 on 2021-12-27 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='Message',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='feed',
            name='Photo',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='Title',
            field=models.CharField(max_length=255),
        ),
    ]
