import bottle
from model import Igralec, Ekipa, Tekmovanje

# Nastavitev Bottle aplikacije
app = bottle.Bottle()

# Nastavitev statične datoteke
@app.get('/static/<pot:path>')
def vrni_staticno(pot):
    return bottle.static_file(pot, root="static")

# Naslovna stran
@app.get('/')
def naslovna_stran():
    return bottle.template('naslovna_stran.html', napaka=None)

# Iskanje igralca
@app.get('/igralec/')
def isci_igralca():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    igralci = list(Igralec.poisci(""))
    if iskalni_niz:
        igralci = [igralec for igralec in igralci if iskalni_niz.lower() in igralec.igralec.lower()]
    return bottle.template(
        'igralec.html',
        iskalni_niz=iskalni_niz,
        igralci=igralci
    )

# Podrobnosti o igralcu
@app.get('/igralec/<id_igralec:int>/')
def podrobnosti_igralca(id_igralec):
    igralec = Igralec(id_igralec=id_igralec)
    ekipe = list(igralec.poisci_ekipe())
    return bottle.template(
        'igralec_podrobnosti.html',
        igralec=igralec,
        ekipe=ekipe
    )

# Iskanje ekipe
@app.get('/ekipa/')
def isci_ekipo():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    ekipe = list(Ekipa.poisci(""))
    if iskalni_niz:
        ekipe = [ekipa for ekipa in ekipe if iskalni_niz.lower() in ekipa.ime.lower()]
    return bottle.template(
        'ekipa.html',
        iskalni_niz=iskalni_niz,
        ekipe=ekipe
    )

# Podrobnosti o ekipi
@app.get('/ekipa/<id_ekipa:int>/')
def podrobnosti_ekipe(id_ekipa):
    ekipa = Ekipa(id_ekipa=id_ekipa)
    vozniki = list(ekipa.poisci_igralce())
    return bottle.template(
        'ekipa_podrobnosti.html',
        ekipa=ekipa,
        vozniki=vozniki
    )

# Iskanje tekmovanja
@app.get('/tekmovanje/')
def isci_tekmovanje():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    tekmovanja = list(Tekmovanje.poisci(""))
    if iskalni_niz:
        tekmovanja = [tekmovanje for tekmovanje in tekmovanja if iskalni_niz.lower() in tekmovanje.tip.lower()]
    return bottle.template(
        'tekmovanje.html',
        iskalni_niz=iskalni_niz,
        tekmovanja=tekmovanja
    )

# Podrobnosti o tekmovanju
@app.get('/tekmovanje/<id_tekmovanja:int>/')
def podrobnosti_tekmovanja(id_tekmovanja):
    tekmovanje = Tekmovanje(id_tekmovanja=id_tekmovanja)
    zmagovalci = list(tekmovanje.poisci_zmagovalce())
    return bottle.template(
        'tekmovanje_podrobnosti.html',
        tekmovanje=tekmovanje,
        zmagovalci=zmagovalci
    )

# Zagon Bottle aplikacije
if __name__ == '__main__':
    bottle.run(app, debug=True, reloader=True)
