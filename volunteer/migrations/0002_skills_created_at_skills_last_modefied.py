# Generated by Django 5.0.2 on 2024-02-11 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2022-02-02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skills',
            name='last_modefied',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
