# Generated by Django 5.2.1 on 2025-05-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'ops_user'), (2, 'client')], default=2),
        ),
    ]
