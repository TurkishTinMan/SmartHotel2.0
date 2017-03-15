# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('numero_posti', models.IntegerField()),
                ('numero_posti_extra', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
                ('cognome', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=10)),
                ('mail', models.CharField(max_length=45)),
                ('pericolo', models.CharField(max_length=1, choices=[(b'E', b'Esigente'), (b'M', b'Medio'), (b'T', b'Tranquillo')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Extra', max_length=30)),
                ('costo', models.DecimalField(max_digits=8, decimal_places=2)),
                ('tipo', models.CharField(max_length=1, choices=[(b'B', b'Bar'), (b'S', b'Servizi'), (b'R', b'Ristorante')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note_Camera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('causale', models.CharField(max_length=140)),
                ('data', models.DateField()),
                ('camera', models.ForeignKey(to='bacheca.Camera')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note_Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('causale', models.CharField(max_length=140)),
                ('data', models.DateField()),
                ('cliente', models.ForeignKey(to='bacheca.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note_Prenotazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('causale', models.CharField(max_length=140)),
                ('data', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('start_data', models.DateField()),
                ('end_data', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prenotazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
                ('adulti', models.IntegerField()),
                ('conto_base', models.DecimalField(max_digits=8, decimal_places=2)),
                ('acconto_fatto', models.DecimalField(max_digits=8, decimal_places=2)),
                ('acconto_versato', models.BooleanField(default=False)),
                ('sconto', models.DecimalField(max_digits=8, decimal_places=2)),
                ('notti', models.IntegerField()),
                ('camera', models.ForeignKey(to='bacheca.Camera')),
                ('cliente', models.ForeignKey(to='bacheca.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrenotazioneHasExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantita', models.IntegerField()),
                ('extra', models.ForeignKey(to='bacheca.Extra')),
                ('prenotazione', models.ForeignKey(to='bacheca.Prenotazione')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrenotazioneHasSconto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantita', models.IntegerField()),
                ('prenotazione', models.ForeignKey(to='bacheca.Prenotazione')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sconto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Sconto', max_length=30)),
                ('percentage', models.IntegerField()),
                ('tipo', models.CharField(max_length=1, choices=[(b'N', b'Notte'), (b'T', b'Totale')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tariffa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2)),
                ('periodo', models.ForeignKey(to='bacheca.Periodo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoCamera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('user', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, unique=True)),
                ('name_structure', models.CharField(max_length=30)),
                ('num_camere', models.IntegerField()),
                ('start_data', models.DateField()),
                ('end_data', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tipocamera',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tariffa',
            name='tipo',
            field=models.ForeignKey(to='bacheca.TipoCamera'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tariffa',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sconto',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prenotazionehassconto',
            name='sconto',
            field=models.ForeignKey(to='bacheca.Sconto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prenotazione',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='periodo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note_prenotazione',
            name='prenotazione',
            field=models.ForeignKey(to='bacheca.Prenotazione'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note_prenotazione',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note_cliente',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note_camera',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extra',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camera',
            name='tipo',
            field=models.ForeignKey(to='bacheca.TipoCamera'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camera',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
