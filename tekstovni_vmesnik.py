from model import Igralec, Ekipa, Tekmovanje
from enum import Enum
import sqlite3

# Povezava z bazo
conn = sqlite3.connect('lol.db')

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

def izpisi_igralce(ekipa):
    """
    Izpiše igralce podane ekipe po letih.
    """
    for team, leto, player, pos in ekipa.poisci_igralce(conn):
        print(f'- {player}, {pos}, {leto}')

def izpisi_ekipo(igralec):
    """
    Izpiše ekipe podanega igralca po letih.
    """
    for player, leto, team, pos in igralec.poisci_ekipe():
        print(f'- {leto}: {team}')

def poisci_igralca():
    """
    Poišče igralca, ki ga vnese uporabnik.
    """
    while True:
        vnos = input('Kateri igralec te zanima? ')
        igralci = list(Igralec.poisci(vnos, conn))
        if len(igralci) == 1:
            print(igralci[0].igralec)
            return igralci[0]
        elif len(igralci) == 0:
            print('Tega igralca ne najdem. Poskusi znova.')
        else:
            print('Našel sem več igralcev, kateri od teh te zanima?')
            return vnesi_izbiro(igralci)

def poisci_ekipo():
    """
    Poišče ekipo, ki jo vnese uporabnik.
    """
    while True:
        vnos = input('Katera ekipa te zanima? ')
        ekipe = list(Ekipa.poisci(vnos, conn))
        if len(ekipe) == 1:
            print(ekipe[0].ime)
            return ekipe[0]
        elif len(ekipe) == 0:
            print('Te ekipe ne najdem. Poskusi znova.')
        else:
            print('Našel sem več ekip, katera od teh te zanima?')
            return vnesi_izbiro(ekipe)

def izpisi_zmagovalce_tekmovanja():
    """
    Izpiše zmagovalce tekmovanja po ligi in/ali letu.
    """
    league = input('Vnesi ligo tekmovanja (prazno za vse lige): ')
    year = input('Vnesi leto tekmovanja (prazno za vsa leta): ')
    tekmovanje = Tekmovanje('', '', '')  # Dummy instance
    results = tekmovanje.poisci_zmagovalce(conn, league=league, year=year)
    for result in results:
        print(f'- Ekipa: {result[0]}, Liga: {result[1]}, Datum: {result[2]}')

def igralec_meni():
    """
    Prikazuje igralčev meni, dokler uporabnik ne izbere izhoda.
    """
    igralec = poisci_igralca()
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(IgralecMeni)
        if izbira == IgralecMeni.SEL_NAZAJ:
            return
        izbira.funkcija(igralec)

def ekipa_meni():
    """
    Prikazuje meni ekipe, dokler uporabnik ne izbere izhoda.
    """
    ekipa = poisci_ekipo()
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(EkipaMeni)
        if izbira == EkipaMeni.SEL_NAZAJ:
            return
        izbira.funkcija(ekipa)

def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi LoL!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return

def domov():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')

class Meni(Enum):
    """
    Razred za izbire v menijih.
    """
    def __init__(self, ime, funkcija):
        """
        Konstruktor izbire.
        """
        self.ime = ime
        self.funkcija = funkcija

    def __str__(self):
        """
        Znakovna predstavitev izbire.
        """
        return self.ime

class IgralecMeni(Meni):
    """
    Izbire v meniju igralca.
    """
    IZPISAL_EKIPE = ('Izpisal ekipe', izpisi_ekipo)
    SEL_NAZAJ = ('Šel nazaj', glavni_meni)

class EkipaMeni(Meni):
    """
    Izbire v meniju ekipe.
    """
    IZPISAL_IGRALCE = ('Izpisal igralce', izpisi_igralce)
    SEL_NAZAJ = ('Šel nazaj', glavni_meni)

class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    ISKAL_IGRALCA = ('Iskal igralca', igralec_meni)
    ISKAL_EKIPO = ('Iskal ekipo', ekipa_meni)
    ISKAL_TEKMOVANJE = ('Iskal zmagovalce tekmovanja', izpisi_zmagovalce_tekmovanja)
    SEL_DOMOV = ('Šel domov', domov)


glavni_meni()
