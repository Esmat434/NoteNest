# Generated by Django 4.2.19 on 2025-02-18 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auth_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auth_token',
            options={'verbose_name': 'Token', 'verbose_name_plural': 'Token'},
        ),
    ]
