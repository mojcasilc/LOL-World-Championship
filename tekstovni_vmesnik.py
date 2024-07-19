from model import Igralec, Ekipa

ISKAL_IGRALCE = 'Iskal igralce'
ISKAL_EKIPO = 'Iskal ekipo'
SEL_DOMOV = 'Šel domov'
MOZNOSTI = [ISKAL_IGRALCE, ISKAL_EKIPO, SEL_DOMOV]

def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")

def poisci_igralca():
    """
    Zahteva vnos (dela) imena
    in vrne ustreznega igralca.
    """
    while True:
        vnos = input('Kdo te zanima? ')
        igralci = list(Igralec.poisci(vnos))
        if len(igralci) == 1:
            return igralci[0]
        elif len(igralci) == 0:
            print('Tega igralca ne najdem. Poskusi znova.')
            return poisci_igralca()
        else:
            print('Našel sem več igralcev, kateri od teh te zanima?')
            return vnesi_izbiro(igralci)
     
def izpisi_tekmovanja(igralec):
    """
    Izpiši ime igralca ter vse tekme,
    v katerih je igral
    """
    print(igralec.ime)
    for tekmovanje in igralec.poisci_tekmovanja():
        print(f'- {tekmovanje.tip} {tekmovanje.leto}')

def poisci_ekipo():
    """
    Zahtevaj vnos (dela) imena
    in vrni ustrezno osebo.
    """
    while True:
        vnos = input('Katera ekipa te zanima? ')
        ekipe = list(Ekipa.poisci(vnos))
        if len(ekipe) == 1:
            return ekipe[0]
        elif len(ekipe) == 0:
            print('Te ekipe ne najdem. Poskusi znova.')
            return poisci_ekipo()
        else:
            print('Našel sem več ekip, katera od teh te zanima?')
            return vnesi_izbiro(ekipe)

def izpisi_tekmovanja_ekipe(ekipa):
    """
    Izpiše ime ekipe ter vse tekme,
    v katerih je sodelovala
    """
    print(ekipa.ime)
    for tekmovanje in ekipa.poisci_tekmovanja():
        print(f'- {tekmovanje.tip} {tekmovanje.leto}')

def glavni_meni():
    print('Pozdravljen v bazi prvenstev Leage if legends!')
    while True:
        print('Kaj bi rad delal?')
        try:
            izbira = vnesi_izbiro(MOZNOSTI)
        except KeyboardInterrupt:
            izbira = SEL_DOMOV
        if izbira == ISKAL_IGRALCE:
            try:
                igralec = poisci_igralca() # vrne en objekt igralca
                izpisi_tekmovanja(igralec)
            except KeyboardInterrupt:
                continue
        elif izbira == ISKAL_EKIPO:
            try:
                ekipa = poisci_ekipo() # vrne en objekt igralca
                izpisi_tekmovanja_ekipe(ekipa)
            except KeyboardInterrupt:
                continue
        elif izbira == SEL_DOMOV:
            print('Adijo!')
            return

if __name__ == '__main__':
    glavni_meni()
