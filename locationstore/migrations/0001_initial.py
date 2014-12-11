# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shoot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=200)),
                ('release_year', models.CharField(default=b'', max_length=4)),
                ('location', models.CharField(default=b'', max_length=300)),
                ('fun_facts', models.CharField(default=b'', max_length=500)),
                ('production_company', models.CharField(default=b'', max_length=200)),
                ('distributor', models.CharField(default=b'', max_length=200)),
                ('director', models.CharField(default=b'', max_length=200)),
                ('writer', models.CharField(default=b'', max_length=200)),
                ('actor_1', models.CharField(default=b'', max_length=200)),
                ('actor_2', models.CharField(default=b'', max_length=200)),
                ('actor_3', models.CharField(default=b'', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
