# Generated by Django 5.0.2 on 2024-02-10 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VolunteerUser',
        ),
    ]
