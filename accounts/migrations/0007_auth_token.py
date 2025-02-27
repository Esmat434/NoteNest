# Generated by Django 4.2.19 on 2025-02-18 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0004_alter_tokenproxy_options'),
        ('accounts', '0006_alter_customuser_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth_Token',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authtoken.token')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            bases=('authtoken.token',),
        ),
    ]
