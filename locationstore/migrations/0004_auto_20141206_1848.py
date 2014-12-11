# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locationstore', '0003_auto_20141205_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoot',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=16, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shoot',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=16, blank=True),
            preserve_default=True,
        ),
    ]
