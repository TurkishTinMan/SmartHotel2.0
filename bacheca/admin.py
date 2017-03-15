from django.contrib import admin
from .models import Utente,Camera,Periodo,TipoCamera,Tariffa,Client,Prenotazione

admin.site.register(Utente)
admin.site.register(Camera)
admin.site.register(Periodo)
admin.site.register(TipoCamera)
admin.site.register(Tariffa)
admin.site.register(Client)
admin.site.register(Prenotazione)


