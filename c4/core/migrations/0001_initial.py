# Generated by Django 5.0 on 2023-12-24 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('Registeration', 'Registeration'), ('Fundraising', 'Fundraising'), ('Construction', 'Construction'), ('End', 'End')], default='Registeration', max_length=20)),
                ('units_number', models.PositiveIntegerField()),
                ('project_area', models.PositiveIntegerField()),
                ('completed_units_number', models.PositiveIntegerField()),
                ('sold_units_number', models.PositiveIntegerField(default=0)),
                ('applied_people_number', models.PositiveIntegerField(default=0)),
                ('contractor_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_photo', models.ImageField(blank=True, null=True, upload_to='uploads/receipt_photos/')),
                ('payment_valid', models.BooleanField(default=False)),
                ('payment_accepted', models.BooleanField(default=False)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myauth.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='C4Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Inprogress', 'Inprogress'), ('Done', 'Done')], default='Inprogress', max_length=20)),
                ('core1', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_one', to='myauth.profile')),
                ('core2', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_two', to='myauth.profile')),
                ('core3', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_three', to='myauth.profile')),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myauth.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
    ]
