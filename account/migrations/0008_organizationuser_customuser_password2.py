# Generated by Django 5.0.1 on 2024-02-05 21:18

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_customuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('account.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='password2',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
