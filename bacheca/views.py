from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from models import Utente,Camera,Periodo,TipoCamera,Tariffa,Prenotazione,Client,Extra,Note_Cliente,Note_Camera,Note_Prenotazione,Sconto,PrenotazioneHasSconto,PrenotazioneHasExtra
from datetime import date,datetime,timedelta,time

def context(user,request):
    periodi = Periodo.objects.filter(user = request.user).count()
    mioperiodo = None
    if periodi > 0:
        today=date.today()
        today= datetime(2017,today.month,today.day)
        mioperiodo = get_object_or_404(Periodo, user = request.user,start_data__lte=today,end_data__gte=today)
    tocomplete = user.num_camere - Camera.objects.filter(user = request.user).count()
    tariffe = Tariffa.objects.filter(user = request.user).count()
    tipi = TipoCamera.objects.filter(user = request.user).count()
    
    return {'user':user,
            'todocamere':periodi != 0 and tipi!=0 and tocomplete > 0,
            'numbertodocamere':tocomplete,
            'todoperiodo':periodi == 0,
            'mioperiodo':mioperiodo,
            'todotipo':tipi == 0,
            'todotariffe':periodi != 0 and tipi!=0 and tariffe == 0,
           }

@login_required(login_url='/login')
def impostazioni(request):
    user = get_object_or_404(Utente, pk=request.user)
    periodi = Periodo.objects.filter(user = request.user)
    tariffe = Tariffa.objects.filter(user = request.user)
    tipi = TipoCamera.objects.filter(user = request.user)
    return render(request,'impostazioni.html',dict(context(user,request).items() +{'periodi':periodi,'tariffe':tariffe,'tipi':tipi}.items()))



@login_required(login_url='/login')
def index(request):
    user = get_object_or_404(Utente, pk=request.user)
    '''dati per la dashboard'''
    today = date.today()
    arrivi = Prenotazione.objects.filter(user = request.user).filter(data_inizio = today)
    arrivicount = 0
    partenzecount = 0
    for arrivo in arrivi:
        arrivo.note_prenotazione = Note_Prenotazione.objects.filter(user = request.user, prenotazione = arrivo)
        arrivo.note_cliente = Note_Cliente.objects.filter(user = request.user, cliente = arrivo.cliente)
        arrivicount = arrivicount + arrivo.adulti
    partenze = Prenotazione.objects.filter(user = request.user).filter(data_fine = today)
    for partenza in partenze:
        partenzecount = partenzecount + partenza.adulti
    note_camera = Note_Camera.objects.filter(user = request.user)
    presenze = 0
    prenotazionipresenze = Prenotazione.objects.filter(user = request.user).filter(data_fine__gt = today, data_inizio__lte = today)
    for prenotazionepresenze in prenotazionipresenze:
        presenze = prenotazionepresenze.adulti + presenze
    return render(request,'index.html',dict(context(user,request).items() +{'arrivi':arrivi,'partenze':partenze,'partenzecount':partenzecount,'arrivicount':arrivicount,'note_camera':note_camera,'presenze':presenze}.items()))

@login_required(login_url='/')
def info_room(request, room_id):
    user = get_object_or_404(Utente, pk=request.user)
    room = get_object_or_404(Camera, pk=room_id,user = request.user)
    if request.POST:
        new_note = Note_Camera()
        new_note.user = request.user
        new_note.causale = request.POST.get('nota')
        new_note.camera = room
        new_note.data = date.today()
        new_note.save()
    note_camera = Note_Camera.objects.filter(user = request.user).filter(camera = room)
    tipi_camera = TipoCamera.objects.filter(user = request.user)
    return render(request,'room.html',dict(context(user,request).items()+{'room':room,'note':note_camera,'tipi':tipi_camera}.items()))

@login_required(login_url='/')
def modify_room(request, room_id):
    if request.POST:
        new_camera = get_object_or_404(Camera, pk=room_id,user = request.user)
        new_camera.numero = request.POST.get('numero')
        new_camera.numero_posti = request.POST.get('numero_posti')
        new_camera.numero_posti_extra = request.POST.get('numero_posti_extra')
        new_camera.tipo = get_object_or_404(TipoCamera, pk=request.POST.get('tipo'))
        new_camera.save()
    return redirect('/room/'+room_id)

@login_required(login_url='/')
def eliminate_room(request, room_id):
    this_camera = get_object_or_404(Camera, pk=room_id,user = request.user)
    prenotazioni = Prenotazione.objects.filter(camera = this_camera, user=request.user)
    for prenotazione in prenotazioni:
        prenotazione.delete()
    note = Note_Camera.objects.filter(camera = this_camera, user=request.user)
    for nota in note:
        nota.delete()
    this_camera.delete()
    return redirect(viewroom)

@login_required(login_url='/')
def eliminate_prenotazione(request, prenotazione_id):
    this_prenotazione = get_object_or_404(Prenotazione, pk=prenotazione_id,user = request.user)
    note = Note_Prenotazione.objects.filter(prenotazione = this_prenotazione, user=request.user)
    for nota in note:
        nota.delete()
    this_prenotazione.delete()
    return redirect(index)

@login_required(login_url='/')
def myprofile(request):
    user = get_object_or_404(Utente, pk=request.user)
    return render(request,'myprofile.html',context(user,request))

@login_required(login_url='/')
def eliminate_note_camera(request,note_id):
    nota = get_object_or_404(Note_Camera, pk=note_id)
    if nota.user == request.user:
        nota.delete()   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def eliminate_note_client(request,note_id):
    nota = get_object_or_404(Note_Cliente, pk=note_id)
    if nota.user == request.user:
        nota.delete()   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def eliminate_note_prenotazione(request,note_id):
    nota = get_object_or_404(Note_Prenotazione, pk=note_id)
    if nota.user == request.user:
        nota.delete()   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def add_extra(request):   
    extrakey = request.POST.get('extra',None)
    prenotazionekey = request.POST.get('prenotazione',None)
    extra = get_object_or_404(Extra,pk = extrakey)
    prenotazione = get_object_or_404(Prenotazione,pk = prenotazionekey)
    if PrenotazioneHasExtra.objects.filter(extra = extra, prenotazione = prenotazione).count() != 0:
        temp = PrenotazioneHasExtra.objects.filter(extra = extra, prenotazione = prenotazione)[0]
        temp.quantita = temp.quantita+1
        temp.save()
    else:
        temp = PrenotazioneHasExtra()
        temp.extra = extra
        temp.prenotazione = prenotazione
        temp.quantita = 1
        temp.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def eliminatextrafromprenotazione(request,extra_id):   
    extra = get_object_or_404(PrenotazioneHasExtra, pk=extra_id)
    if extra.quantita > 1:
        extra.quantita -= 1
        extra.save()
    else:
        extra.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def eliminate_extra(request,extra_id):
    extra = get_object_or_404(Extra, pk=extra_id)
    if extra.user == request.user:
        PrenotazioneHasExtra.objects.filter(extra = extra).delete()
        extra.delete()   
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def add_sconto(request):   
    scontokey = request.POST.get('sconto',None)
    prenotazionekey = request.POST.get('prenotazione',None)
    sconto = get_object_or_404(Sconto,pk = scontokey)
    prenotazione = get_object_or_404(Prenotazione,pk = prenotazionekey)
    if PrenotazioneHasSconto.objects.filter(sconto = sconto, prenotazione = prenotazione).count() != 0:
        temp = PrenotazioneHasSconto.objects.filter(sconto = sconto, prenotazione = prenotazione)[0]
        temp.quantita = temp.quantita+1
        temp.save()
    else:
        temp = PrenotazioneHasSconto()
        temp.sconto = sconto
        temp.prenotazione = prenotazione
        temp.quantita = 1
        temp.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def eliminatescontofromprenotazione(request,sconto_id):   
    sconto = get_object_or_404(PrenotazioneHasSconto, pk=sconto_id)
    if sconto.quantita > 1:
        sconto.quantita -= 1
        sconto.save()
    else:
        sconto.delete()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/')
def eliminate_sconto(request,sconto_id):
    sconto = get_object_or_404(Sconto, pk=sconto_id)
    if sconto.user == request.user:
        PrenotazioneHasSconto.objects.filter(sconto = sconto).delete()
        sconto.delete()   
    return redirect(request.META.get('HTTP_REFERER'))


def calendar(a,b):
    lista = [None]* (int ((b - a).days))
    for n in range(int ((b - a).days)):
        lista[n] = a + timedelta(days = n)
    return lista 

def occupati(camere,periodo,request):
    periodolen = len(periodo)
    cameralen = len(camere)
    today = date.today() 
    dictionary = {}
    prenotazioni = Prenotazione.objects.filter(user = request.user).exclude(data_fine__lt = periodo[0]).exclude(data_inizio__gt = periodo[-1])
    for camera in camere:
        temproom = {}
        x = 0
        for day in periodo:
            temp = {'fine':None,'start':None}
            prenotazione = prenotazioni.filter(camera = camera , data_fine = day)
            if prenotazione.count() != 0:
                temp['fine'] = prenotazione[0]
            prenotazione = prenotazioni.filter(camera = camera , data_inizio = day)
            if prenotazione.count() != 0:
                temp['start'] = prenotazione[0]
            prenotazione = prenotazioni.filter(camera = camera , data_inizio__lt = day,data_fine__gt = day)
            if prenotazione.count() != 0:
                temp['start'] = prenotazione[0]
                temp['fine'] = prenotazione[0]
            temproom[x] = temp
            x += 1
        dictionary[camera] = temproom
    return dictionary


@login_required(login_url='/login')
def tableau(request):
    user = request.user
    camere = Camera.objects.filter(user = request.user).order_by('numero')
    if request.POST:
        periodostart_data = datetime.strptime(request.POST['start'], '%d/%m/%Y').date()
        periodoend_data = datetime.strptime(request.POST['end'], '%d/%m/%Y').date()
    else:
        periodostart_data = date.today()
        periodoend_data = date.today() + timedelta(days=30)
    periodoattuale = calendar(periodostart_data,periodoend_data + timedelta(days=1))
    datagobackstart = periodostart_data - timedelta(days=30)
    datagobackend = periodostart_data
    datagobackshortstart = periodostart_data - timedelta(days=15)
    datagobackshortend = periodostart_data + timedelta(days=15)
    datagoforwardstart = periodoend_data 
    datagoforwardend = periodoend_data + timedelta(days=30)
    datagoforwardshortstart = periodostart_data + timedelta(days=15)
    datagoforwardshortend = periodostart_data + timedelta(days=45)
    
    
    return render(request,'tableau.html',{'datagobackstart':datagobackstart,'datagobackend':datagobackend,'datagobackshortstart':datagobackshortstart,'datagobackshortend':datagobackshortend,'datagoforwardstart':datagoforwardstart,'datagoforwardend':datagoforwardend,'datagoforwardshortstart':datagoforwardshortstart,'datagoforwardshortend':datagoforwardshortend,'camere':camere,'date':periodoattuale,'matrix':occupati(camere,periodoattuale,request)})



@login_required(login_url='/login')
def viewroom(request):
    user = get_object_or_404(Utente, pk=request.user)
    camere = Camera.objects.filter(user = request.user)
    today=date.today()
    totalprenotation = Prenotazione.objects.filter(user = request.user)
    for camera in camere:
        prenotazioni = totalprenotation.filter(camera = camera)
        prenotazione =  prenotazioni.filter(data_inizio__lt = today,data_fine__gte=today)
        if prenotazione.count() == 1:
            camera.prenotazione1 = prenotazione[0]
        else:
            camera.prenotazione1 = 0
        prenotazione = prenotazioni.filter(data_inizio__lte = today,data_fine__gt=today)
        if prenotazione.count() == 1:
            camera.prenotazione2 = prenotazione[0]
        else:
            camera.prenotazione2 = 0
    return render(request,'viewroom.html',dict(context(user,request).items()+{'camere':camere}.items()))


@login_required(login_url='/login')
def maketipi(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        end = False
        num = 1
        while end == False:
            print(num)
            name = request.POST.get('name-'+str(num),None)
            if name is None:
                end = True
            else:
                new_type = TipoCamera()
                new_type.user = request.user
                new_type.name = name
                new_type.save()
                num = num +1        
        return redirect('index')        
    return render(request,'maketipi.html',context(user,request))

@login_required(login_url='/login')
def prenotazioni(request):
    user = get_object_or_404(Utente, pk=request.user)
    prenotazioni = Prenotazione.objects.filter(user = request.user)
    return render(request,'prenotazioni.html',dict(context(user,request).items() + {'prenotazioni':prenotazioni}.items()))


@login_required(login_url='/login')
def addprenotazione(request):
    user = get_object_or_404(Utente, pk=request.user)
    return render(request,'addprenotazione.html',context(user,request))


def tariffa(camera,start,end,request):
    prezzo = 0
    giorni = calendar(start,end)
    for giorno in giorni:
        giorno= datetime(2017,giorno.month,giorno.day)
        periodo = get_object_or_404(Periodo,user = request.user, start_data__lte=giorno,end_data__gte=giorno)
        tariffa = get_object_or_404(Tariffa,user= request.user, tipo = camera.tipo, periodo = periodo )
        prezzo = prezzo + tariffa.cost
    return prezzo

def libera(camera,start,end,request):
    check = True
    prenotazioni = Prenotazione.objects.filter(user = request.user, camera = camera)
    for prenotazione in prenotazioni:
        if (prenotazione.data_inizio < start and prenotazione.data_fine > start)or(prenotazione.data_inizio < end and prenotazione.data_fine > end)or(prenotazione.data_inizio >= start and prenotazione.data_fine <= end):
            check = False
    return check


def disponibilita(start,end,num_ospiti,request):
    camere_tot = Camera.objects.filter(user = request.user)
    camere = []
    for camera in camere_tot:
        contain = (camera.numero_posti + camera.numero_posti_extra) >= num_ospiti
        if contain and libera(camera,start,end,request):
            camera.tariffa = tariffa(camera,start,end,request)
            camere.append(camera)
    return camere


@login_required(login_url='/login')
def addprenotazione2(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        start = request.POST.get('start',None)
        end = request.POST.get('fine',None)
        num_ospiti = int(request.POST.get('num_ospiti',None))
        if start and end and num_ospiti:
            start = datetime.strptime(request.POST['start'], '%d/%m/%Y').date()
            end = datetime.strptime(request.POST['fine'], '%d/%m/%Y').date()
            if end <= start:
                temp = end
                end = start
                start = temp
            camere = disponibilita(start,end,num_ospiti,request)     
            return render(request,'addprenotazione2.html',dict(context(user,request).items() + {'start':start,'end':end,'num_ospiti':num_ospiti, 'camere':camere}.items()))
    return redirect(addprenotazione)

@login_required(login_url='/login')
def addprenotazione3(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        start = request.POST.get('start',None)
        end = request.POST.get('fine',None)
        num_ospiti = int(request.POST.get('num_ospiti',None))
        camera = get_object_or_404(Camera, user = request.user, id=request.POST.get('room',None))
        if camera and start and num_ospiti and camera:
            start = datetime.strptime(start, '%d/%m/%Y').date()
            end = datetime.strptime(end, '%d/%m/%Y').date()
            conto = tariffa(camera,start,end,request)
            clienti = Client.objects.filter(user = request.user)
            return render(request,'addprenotazione3.html',dict(context(user,request).items() + {'start':start,'end':end,'num_ospiti':num_ospiti,'conto':conto, 'camera':camera,'clienti':clienti }.items()))
    return redirect(addprenotazione)

@login_required(login_url='/login')
def addprenotazione4(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        start = request.POST.get('start',None)
        end = request.POST.get('fine',None)
        num_ospiti = int(request.POST.get('num_ospiti',None))
        camera = get_object_or_404(Camera, user = request.user, id=request.POST.get('room',None))
        clientemode = request.POST.get('clientmode',None)
        if clientemode:
            if clientemode == '0':
                cliente = get_object_or_404(Client, user = request.user, id=request.POST.get('client',None))
            else:
                cliente = Client()
                cliente.user = request.user
                cliente.nome = request.POST.get('nome')
                cliente.cognome = request.POST.get('cognome')
                cliente.telefono = request.POST.get('tel')
                cliente.mail = request.POST.get('email')
                cliente.pericolo = 'M'
                cliente.save()
        else:
            '''gestire 404'''
        conto = int(request.POST.get('conto',None))
        if start and end and num_ospiti:    
            new_prenotazione = Prenotazione()
            new_prenotazione.user = request.user
            new_prenotazione.data_inizio = datetime.strptime(start, '%d/%m/%Y').date()
            new_prenotazione.data_fine = datetime.strptime(end, '%d/%m/%Y').date()
            new_prenotazione.cliente = cliente
            new_prenotazione.camera = camera
            new_prenotazione.adulti = num_ospiti
            new_prenotazione.conto_base = conto
            new_prenotazione.acconto_fatto = 0
            new_prenotazione.sconto = 0
            new_prenotazione.notti = int((new_prenotazione.data_fine - new_prenotazione.data_inizio).days)
            new_prenotazione.save()
            return redirect('/prenotazione/'+str(new_prenotazione.id))
    return redirect(addprenotazione)

@login_required(login_url='/login')
def info_prenotazione(request,prenotazione_id):
    user = get_object_or_404(Utente, pk=request.user)
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id,user = request.user)
    if request.POST:
        new_note = Note_Prenotazione()
        new_note.user = request.user
        new_note.causale = request.POST.get('nota')
        new_note.prenotazione = prenotazione
        new_note.data = date.today()
        new_note.save()
    extras = Extra.objects.filter(user = request.user)
    sconti = Sconto.objects.filter(user = request.user)
    extrasprenotazione = PrenotazioneHasExtra.objects.filter(prenotazione = prenotazione)
    scontiprenotazione = PrenotazioneHasSconto.objects.filter(prenotazione = prenotazione)
    note_prenotazione = Note_Prenotazione.objects.filter(user = request.user).filter(prenotazione = prenotazione)
    tot = prenotazione.conto_base
    for sconto in scontiprenotazione:
        if sconto.sconto.tipo == 'N':
            for x in xrange(sconto.quantita):
                tot -= (prenotazione.conto_base/prenotazione.adulti)/100 * sconto.sconto.percentage
        else:
            for x in xrange(sconto.quantita):
                tot -= prenotazione.conto_base/100 * sconto.sconto.percentage
    for extra in extrasprenotazione:
        for x in xrange(extra.quantita):
            tot += extra.extra.costo
    return render(request,'info_prenotazione.html',dict(context(user,request).items() + {'prenotazione':prenotazione,'note':note_prenotazione,'extras':extras,'sconti':sconti,'extrasprenotazione':extrasprenotazione,'scontiprenotazione':scontiprenotazione, 'tot':tot}.items()))






@login_required(login_url='/login')
def maketariffe(request):
    user = get_object_or_404(Utente, pk=request.user)
    periodi = Periodo.objects.filter(user = request.user).all()
    tipiCamera = TipoCamera.objects.filter(user = request.user).all()
    if request.POST:
        for periodo in periodi:
            print periodo.id
            for tipo in tipiCamera:
                print tipo.id
                costo = request.POST.get(str(tipo.id)+"-"+str(periodo.id))
                tariffa = Tariffa()
                tariffa.user = request.user
                tariffa.tipo = tipo
                tariffa.periodo = periodo
                tariffa.cost = costo
                tariffa.save()
        return redirect('index')

    return render(request,'maketariffe.html', dict(context(user,request).items() + {'periodi':periodi,'tipi':tipiCamera}.items()))



@login_required(login_url='/login')
def addroom(request):
    user = get_object_or_404(Utente, pk=request.user)
    tipiCamera = TipoCamera.objects.filter(user = request.user).all()

    if request.POST:
        new_camera = Camera()
        new_camera.user = request.user
        new_camera.numero = request.POST.get('numero')
        new_camera.numero_posti = request.POST.get('numero_posti')
        new_camera.numero_posti_extra = request.POST.get('numero_posti_extra')
        new_camera.tipo = get_object_or_404(TipoCamera, pk=request.POST.get('tipo'))
        new_camera.save()
        
    tocomplete = user.num_camere - Camera.objects.filter(user = request.user).count()
    if tocomplete <= 0:
        return redirect('index')
    return render(request,'addroom.html',dict(context(user,request).items() + {'tipi':tipiCamera}.items()))
    

@login_required(login_url='/login')
def rubrica(request):
    user = get_object_or_404(Utente, pk=request.user)
    clienti = Client.objects.filter(user = request.user)
    return render(request,'rubrica.html',dict(context(user,request).items()+{'clienti':clienti}.items()))

@login_required(login_url='/login')
def addclienti(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        name = request.POST.get('nome',None)
        surname = request.POST.get('cognome',None)
        telefono = request.POST.get('telefono',None)
        mail = request.POST.get('mail',None)
        tipo = request.POST.get('tipo',None)
        if name and surname and telefono and mail and tipo:
            new_client = Client()
            new_client.user = request.user
            new_client.nome = name
            new_client.cognome = surname
            new_client.telefono = telefono
            new_client.mail = mail
            new_client.pericolo = tipo
            new_client.save()
            return redirect(rubrica)
        else:
            return render(request,'addclienti.html',dict(context(user,request).items()+{'errore':'Errore generico!'}.items()))
    return render(request,'addclienti.html',context(user,request))

@login_required(login_url='/login')
def info_client(request, client_id):
    user = get_object_or_404(Utente, pk=request.user)
    cliente = get_object_or_404(Client,pk=client_id,user=request.user)
    if request.POST:
        new_note = Note_Cliente()
        new_note.user = request.user
        new_note.causale = request.POST.get('nota')
        new_note.cliente = cliente
        new_note.data = date.today()
        new_note.save()
    note_cliente = Note_Cliente.objects.filter(user = request.user).filter(cliente = cliente)
    prenotazioni = Prenotazione.objects.filter(user = request.user).filter(cliente = cliente)
    return render(request,'info_client.html',dict(context(user,request).items()+{'cliente':cliente,'note':note_cliente,'prenotazioni':prenotazioni}.items()))

@login_required(login_url='/login')
def modify_client(request, client_id):
    if request.POST:
        cliente = get_object_or_404(Client, pk=client_id,user = request.user)
        cliente.nome = request.POST.get('nome')
        cliente.cognome = request.POST.get('cognome')
        cliente.telefono = request.POST.get('telefono')
        cliente.mail = request.POST.get('mail')
        cliente.pericolo = request.POST.get('pericolo')
        cliente.save()
    return redirect('/client/'+client_id)

@login_required(login_url='/login')
def eliminate_client(request, client_id):
    this_client = get_object_or_404(Client, pk=client_id,user = request.user)
    prenotazioni = Prenotazione.objects.filter(cliente = this_client, user=request.user)
    for prenotazione in prenotazioni:
        prenotazione.delete()
    note = Note_Cliente.objects.filter(cliente = this_client, user=request.user)
    for nota in note:
        nota.delete()
    this_client.delete()
    return redirect(rubrica)


@login_required(login_url='/login')
def payment(request):
    user = get_object_or_404(Utente, pk=request.user)
    return render(request,'payment.html',context(user,request))    
    
@login_required(login_url='/login')
def makeperiod(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        end = False
        num = 1
        while end == False:
            print(num)
            name = request.POST.get('periodo-'+str(num),None)
            if name is None:
                end = True
            else:
                periodo = Periodo()
                periodo.user = request.user
                periodo.name = request.POST.get('periodo-'+str(num))
                if(num == 1):
                    periodo.start_data = datetime(2017,01,01).date()
                else:
                    periodo.start_data = datetime.strptime(request.POST['fine-'+str(num-1)], '%d/%m').date()
                    periodo.start_data= datetime(2017,periodo.start_data.month,periodo.start_data.day)
                periodo.end_data = datetime.strptime(request.POST['fine-'+str(num)], '%d/%m').date()
                periodo.end_data= datetime(2017,periodo.end_data.month,periodo.end_data.day)
                periodo.save()
                num = num +1        
        return redirect('index')
    periodi = Periodo.objects.filter(user = request.user)
    return render(request,'makeperiod.html',dict(context(user,request).items() + {'periodi':periodi}.items()))    


@login_required(login_url='/login')
def note(request):
    user = get_object_or_404(Utente, pk=request.user)
    note_prenotazioni = Note_Prenotazione.objects.filter(user = request.user)
    note_camere = Note_Camera.objects.filter(user = request.user)
    note_clienti = Note_Cliente.objects.filter(user = request.user)
    return render(request,'note.html',dict(context(user,request).items() + {'note_prenotazioni':note_prenotazioni,'note_camere':note_camere,'note_clienti':note_clienti}.items()))


@login_required(login_url='/login')
def extra(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        if(request.POST.get('extra-1') and request.POST.get('prezzo-1') and request.POST.get('tipo-1')):
            newextra = Extra()
            newextra.user = request.user
            newextra.name = request.POST.get('extra-1')
            newextra.costo = request.POST.get('prezzo-1')
            newextra.tipo = request.POST.get('tipo-1')
            newextra.save()
    extras = Extra.objects.filter(user = request.user)
    return render(request,'extra.html',dict(context(user,request).items() + {'extras':extras}.items()))


@login_required(login_url='/login')
def sconti(request):
    user = get_object_or_404(Utente, pk=request.user)
    if request.POST:
        if(request.POST.get('sconto-1') and request.POST.get('percentuale-1') and request.POST.get('tipo-1')):
            newsconto = Sconto()
            newsconto.user = request.user
            newsconto.name = request.POST.get('sconto-1')
            newsconto.percentage = request.POST.get('percentuale-1')
            newsconto.tipo = request.POST.get('tipo-1')
            newsconto.save()    
    sconti = Sconto.objects.filter(user = request.user)
    return render(request,'sconti.html',dict(context(user,request).items() + {'sconti':sconti}.items()))

def login_(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('index')
            else:
                return render(request,'login.html',{'errore':1})
        else:
            return render(request,'login.html',{'errore':1})
    return render(request,'login.html')

def logout_(request):
    logout(request)
    return render(request,'logout.html')

def registration_(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        nome_locale = request.POST.get('local_name')
        num_camere = request.POST.get('num_camere')
        
        if (password == password2) and password and password2 and email and nome_locale and num_camere:
            user = User.objects.create_user(username,email,password)
            userinfo = Utente()
            userinfo.user = user
            userinfo.name_structure = nome_locale
            userinfo.num_camere = num_camere
            userinfo.start_data = date.today()
            userinfo.end_data = date.today() + timedelta(days=30)
            userinfo.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request,'registration.html',{'errore':"Errore generico!"})        
    return render(request,'registration.html')

    



def validate_period(request):
    currdata = request.GET.get('fine', None)
    data = {
        'end': currdata == "31/12"
    }
    return JsonResponse(data)




def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def validate_password(request):
    password = request.GET.get('pass', None)
    password2 = request.GET.get('pass2',None)
    
    data = {
        'is_same': password == password2
    }
    
    return JsonResponse(data)
