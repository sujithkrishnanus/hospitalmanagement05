# Generated by Django 4.2.16 on 2024-09-18 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0005_alter_logintable_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logintable',
            name='user',
            field=models.CharField(choices=[('patient', 'patient'), ('staff', 'staff'), ('doctor', 'doctor')], default='patient', max_length=200),
        ),
    ]
