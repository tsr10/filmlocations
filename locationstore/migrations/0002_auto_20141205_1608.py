# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locationstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTruck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locationid', models.CharField(default=b'', max_length=200)),
                ('applicant', models.CharField(default=b'', max_length=200)),
                ('facility_type', models.CharField(default=b'', max_length=100)),
                ('location_description', models.CharField(default=b'', max_length=500)),
                ('address', models.CharField(default=b'', max_length=200)),
                ('status', models.CharField(default=b'', max_length=200)),
                ('food_items', models.CharField(default=b'', max_length=400)),
                ('latitude', models.DecimalField(null=True, max_digits=20, decimal_places=15)),
                ('longitude', models.DecimalField(null=True, max_digits=20, decimal_places=15)),
                ('schedule', models.CharField(default=b'', max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Shoot',
        ),
    ]
