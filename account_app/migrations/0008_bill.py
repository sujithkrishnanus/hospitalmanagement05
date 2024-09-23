# Generated by Django 4.2.16 on 2024-09-21 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0007_alter_appointment_status_alter_logintable_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=200)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.appointment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.doctorregistration')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.patientregistration')),
            ],
        ),
    ]
