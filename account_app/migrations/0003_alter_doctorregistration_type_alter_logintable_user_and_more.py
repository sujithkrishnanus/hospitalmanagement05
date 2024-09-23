# Generated by Django 4.2.16 on 2024-09-12 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_alter_logintable_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='type',
            field=models.OneToOneField(limit_choices_to={'user': 'doctor'}, on_delete=django.db.models.deletion.CASCADE, to='account_app.logintable'),
        ),
        migrations.AlterField(
            model_name='logintable',
            name='user',
            field=models.CharField(choices=[('staff', 'staff'), ('doctor', 'doctor'), ('patient', 'patient')], default='patient', max_length=200),
        ),
        migrations.AlterField(
            model_name='patientregistration',
            name='type',
            field=models.OneToOneField(limit_choices_to={'user': 'patient'}, on_delete=django.db.models.deletion.CASCADE, to='account_app.logintable'),
        ),
        migrations.AlterField(
            model_name='staffregistration',
            name='type',
            field=models.OneToOneField(limit_choices_to={'user': 'staff'}, on_delete=django.db.models.deletion.CASCADE, to='account_app.logintable'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_appointment', models.CharField(max_length=250)),
                ('time_of_appointment', models.CharField(max_length=250)),
                ('additional_msg', models.TextField(blank=True)),
                ('remark', models.CharField(default=0, max_length=250)),
                ('status', models.CharField(default=0, max_length=200)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.doctorregistration')),
                ('pat_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='account_app.patientregistration')),
                ('spec_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='account_app.specialization')),
            ],
        ),
    ]
