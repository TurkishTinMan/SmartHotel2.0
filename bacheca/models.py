from django.db import models
from django.contrib.auth.models import User

class Utente(models.Model):
    user                = models.ForeignKey(User, unique=True,primary_key=True)
    name_structure      = models.CharField(max_length=30)
    num_camere          = models.IntegerField()
    start_data          = models.DateField()
    end_data            = models.DateField()
    
class Periodo(models.Model):
    user                = models.ForeignKey(User)
    name                = models.CharField(max_length= 30)
    start_data          = models.DateField()
    end_data            = models.DateField()

class TipoCamera(models.Model):
    user                = models.ForeignKey(User)
    name                = models.CharField(max_length= 30)
    
class Camera(models.Model):
    user                = models.ForeignKey(User)
    numero              = models.IntegerField()
    numero_posti        = models.IntegerField()
    numero_posti_extra  = models.IntegerField()
    tipo                = models.ForeignKey(TipoCamera)
        
class Tariffa(models.Model):
    user = models.ForeignKey(User)
    tipo = models.ForeignKey(TipoCamera)
    periodo = models.ForeignKey(Periodo)
    cost = models.DecimalField(max_digits = 10,decimal_places=2)
    
class Client(models.Model):
    user = models.ForeignKey(User)
    TIPO = (
        ('E', 'Esigente'),
        ('M', 'Medio'),
        ('T', 'Tranquillo'),
    )
    nome                = models.CharField(max_length=30)
    cognome             = models.CharField(max_length=30)
    telefono            = models.CharField(max_length=10)
    mail                = models.CharField(max_length=45)
    pericolo            = models.CharField(max_length=1, choices=TIPO)

class Prenotazione(models.Model):
    user                = models.ForeignKey(User)
    data_inizio         = models.DateField()
    data_fine           = models.DateField()
    cliente             = models.ForeignKey(Client)
    camera              = models.ForeignKey(Camera)
    adulti              = models.IntegerField()
    conto_base          = models.DecimalField(max_digits=8, decimal_places=2)
    acconto_fatto       = models.DecimalField(max_digits=8, decimal_places=2)
    acconto_versato     = models.BooleanField(default=False)
    sconto              = models.DecimalField(max_digits=8, decimal_places=2)
    notti               = models.IntegerField()

class Extra(models.Model):
    user                = models.ForeignKey(User)
    TIPOEXTRA = (
        ('B', 'Bar'),
        ('S', 'Servizi'),
        ('R', 'Ristorante'),
    )
    name                = models.CharField(max_length=30, default="Extra")
    costo               = models.DecimalField(max_digits=8, decimal_places=2)
    tipo                = models.CharField(max_length=1, choices=TIPOEXTRA)

class PrenotazioneHasExtra(models.Model):
    prenotazione        = models.ForeignKey(Prenotazione)
    extra               = models.ForeignKey(Extra)
    quantita            = models.IntegerField()
    
class Sconto(models.Model):
    user                = models.ForeignKey(User)
    TIPOSCONTO = (
        ('N', 'Notte'),
        ('T', 'Totale'),
    )
    name                = models.CharField(max_length=30,default="Sconto")
    percentage          = models.IntegerField()
    tipo                = models.CharField(max_length=1, choices=TIPOSCONTO)

class PrenotazioneHasSconto(models.Model):
    prenotazione        = models.ForeignKey(Prenotazione)
    sconto              = models.ForeignKey(Sconto)
    quantita            = models.IntegerField()

class Note_Cliente(models.Model):
    user                = models.ForeignKey(User)
    causale             = models.CharField(max_length=140)
    cliente             = models.ForeignKey(Client)
    data                = models.DateField()

class Note_Camera(models.Model):
    user                = models.ForeignKey(User)
    causale             = models.CharField(max_length=140)
    camera              = models.ForeignKey(Camera)
    data                = models.DateField()

class Note_Prenotazione(models.Model):
    user                = models.ForeignKey(User)
    causale             = models.CharField(max_length=140)
    prenotazione        = models.ForeignKey(Prenotazione)
    data                = models.DateField()
 
