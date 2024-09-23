# Generated by Django 4.2.16 on 2024-09-12 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0003_alter_doctorregistration_type_alter_logintable_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logintable',
            name='user',
            field=models.CharField(choices=[('doctor', 'doctor'), ('staff', 'staff'), ('patient', 'patient')], default='patient', max_length=200),
        ),
    ]