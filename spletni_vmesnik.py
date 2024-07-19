import bottle
from model import Igralec, Ekipa, Tekmovanje

# Nastavitev statične datoteke
@bottle.get('/static/<pot:path>')
def vrni_staticno(pot):
    return bottle.static_file(pot, root="static")

# Naslovna stran
@bottle.get('/')
@bottle.view('zacetna_stran.html')
def zacetna_stran():
    pass

@bottle.get('/igralci/isci/')
@bottle.view('isci_igralce.html')
def isci():
    ime = bottle.request.query.ime
    igralci = Igralec.poisci(ime)
    if len(igralci) == 1:
        igralec, = igralci
        bottle.redirect(f'/igralci/{igralec.id}/') 
    return dict(ime=ime, igralec=igralci)

@bottle.get('/igralci/<id:int>/')
@bottle.view('igralec_podatki.html')
def igralci_tekmovanja(id):
    try:
        oseba = Igralec.z_id(id)
    except ValueError:
        bottle.abort(404, f'Oseba z ID-jem {id} ne obstaja!')
    tekmovanja = oseba.poisci_tekmovanja()
    return dict(oseba=oseba, tekmovanja=tekmovanja)

@bottle.get("/tekmovanje/<id:int>/")
@bottle.view('tekmovanje_podatki.html')
def podatki_tekmovanja(id):
    try:
        tekmovanje = Tekmovanje.z_id(id)
    except ValueError:
        bottle.abort(404, f'Film z ID-jem {id} ne obstaja!')
    tekme = tekmovanje.tekme() # slovar
    prvi, = tekmovanje.prva_ekipa()
    drugi, = tekmovanje.druga_ekipa()
    tretji1, tretji2 = tekmovanje.tretja_ekipa()
    return dict(tekmovanje=tekmovanje, tekme=tekme, prvi=prvi, drugi=drugi, tretji1=tretji1, tretji2=tretji2)

@bottle.get("/ekipa/<id:int>/")
@bottle.view('ekipa_podatki.html')
def podatki_tekmovanja(id):
    try:
        ekipa = Ekipa.z_id(id)
    except ValueError:
        bottle.abort(404, f'Film z ID-jem {id} ne obstaja!')
    tekmovanja = ekipa.poisci_tekmovanja()
    tek_igralci = {tekmovanje: ekipa.igralci(tekmovanje.id) for tekmovanje in tekmovanja}
    zmage = ekipa.zmage()
    return dict(ekipa=ekipa, tek_igralci=tek_igralci, zmage=zmage)

@bottle.get('/ekipa/isci/')
@bottle.view('isci_ekipe.html')
def isci():
    ime = bottle.request.query.ime
    ekipe = Ekipa.poisci(ime)
    if len(ekipe) == 1:
        ekipa, = ekipe
        bottle.redirect(f'/ekipa/{ekipa.id}/') 
    return dict(ime=ime, ekipe=ekipe)

@bottle.get('/tekmovanje/isci/')
@bottle.view('isci_tekmovanja.html')
def isci():
    tekmovanja = Tekmovanje().vsa_tekmovanja()
    return dict(tekmovanja=tekmovanja)

# Zagon Bottle aplikacije
if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
