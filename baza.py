import csv
import sqlite3

PARAM_FMT = ":{}" # za SQLite


class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.

    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    """
    ime = None #ime tabele
    podatki = None #ime datoteke s podatki

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")

    def uvozi(self, encoding="UTF-8"):
        """
        Metoda za uvoz podatkov.
        """
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka) # seznam seznamov
            stolpci = next(podatki) # seznam
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)} # slovar
                self.dodaj_vrstico(**vrstica)

    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.

        Argumenti:
        - stolpci: seznam stolpcev
        """
        return f"""
            INSERT INTO {self.ime} ({", ".join(stolpci)})
            VALUES ({", ".join(PARAM_FMT.format(s) for s in stolpci)});
        """

    def dodaj_vrstico(self, **podatki):
        """
        Metoda za dodajanje vrstice.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items()
                   if vrednost is not None}
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid


class Ekipa(Tabela):
    """
    Tabela za ekipe.
    """
    ime = "ekipa"


    def ustvari(self):
        """
        Ustvari tabelo ekipe.
        """
        self.conn.execute("""
            CREATE TABLE ekipa (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                ime     TEXT
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj oznako.

        Če oznaka že obstaja, je ne dodamo še enkrat.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert "ime" in podatki
        cur = self.conn.execute("""
            SELECT id FROM ekipa
            WHERE ime = :ime;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id
        

class Tekmovanje(Tabela):
    """
    Tabela za tekmovanja.
    """
    ime = "tekmovanje"

    def ustvari(self):
        """
        Ustvari tabelo tekmovanje.
        """
        self.conn.execute("""
            CREATE TABLE tekmovanje (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                tip               TEXT,
                leto              INTEGER
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj oznako.

        Če oznaka že obstaja, je ne dodamo še enkrat.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert "tip", "leto" in podatki
        cur = self.conn.execute("""
            SELECT id FROM tekmovanje
            WHERE tip = :tip AND leto = :leto;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id


class Igralec(Tabela):
    """
    Tabela za igralce.
    """
    ime = "igralec"

    def ustvari(self):
        """
        Ustvari tabelo igralci.
        """
        self.conn.execute("""
            CREATE TABLE igralec (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                ime       TEXT
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj oznako.

        Če oznaka že obstaja, je ne dodamo še enkrat.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert "ime" in podatki
        cur = self.conn.execute("""
            SELECT id FROM igralec
            WHERE ime = :ime;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id

class Tekma(Tabela):
    """
    Tabela za tekme.
    """
    ime = "tekma"

    def __init__(self, conn):
        """
        Konstruktor tabele filmov.

        Argumenti:
        - conn: povezava na bazo
        - oznaka: tabela za oznake
        """
        super().__init__(conn)

    def ustvari(self):
        """
        Ustvari tabelo iger.
        """
        self.conn.execute("""
            CREATE TABLE tekma (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                tekmovanje        INTEGER REFERENCES tekmovanje(id),
                datum             DATE,
                cas               TEXT,
                st_igre          INTEGER,
                UNIQUE(tekmovanje, datum, cas, st_igre)          
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj oznako.

        Če oznaka že obstaja, je ne dodamo še enkrat.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert all(key in podatki for key in ["tekmovanje", "datum", "cas", "st_igre"])
        cur = self.conn.execute("""
            SELECT id FROM tekma
            WHERE tekmovanje = :tekmovanje AND datum = :datum AND cas = :cas AND st_igre = :st_igre;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id
        
class Nastopa(Tabela):
    """
    Tabela za relacijo pripadnosti ekipe tekmi.
    """
    ime = "nastopa"
    podatki = "podatki/tekma.csv"

    def __init__(self, conn, tekmovanje, ekipa, tekma):
        """
        Konstruktor tabele pripadnosti ekipi in igralcem.

        Argumenti:
        - conn: povezava na bazo
        - ekipa: tabela za ekipe
        - igralec: tabela za igralce
        """
        super().__init__(conn)
        self.tekmovanje = tekmovanje
        self.ekipa = ekipa
        self.tekma = tekma

    def ustvari(self):
        """
        Ustvari tabelo nastopov.
        """
        self.conn.execute("""
            CREATE TABLE nastopa (
                tekma             INTEGER REFERENCES tekma(id),
                ekipa             INTEGER REFERENCES ekipa(id),
                zmaga             INTEGER,
                PRIMARY KEY(tekma, ekipa)
            );
        """)
    
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj tekmo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """

        # dobimo id tekmovanja (rabimo za tekmo)
        if podatki.get("tip", None) is not None and podatki.get("leto", None) is not None:
            podatki["tekmovanje"] = self.tekmovanje.dodaj_vrstico(tip=podatki["tip"], leto=podatki["leto"])
            del podatki["tip"]
            del podatki["leto"]

        # dobimo id ekipe
        if podatki.get("ime_ekipe", None) is not None:
            podatki["ekipa"] = self.ekipa.dodaj_vrstico(ime=podatki["ime_ekipe"])
            del podatki["ime_ekipe"]

        # dobimo id tekme
        if podatki.get("tekmovanje", None) is not None and podatki.get("datum", None) is not None and \
            podatki.get("cas", None) is not None and podatki.get("st_igre", None) is not None:

            podatki["tekma"] = self.tekma.dodaj_vrstico(tekmovanje=podatki["tekmovanje"],datum=podatki["datum"],\
                                                        cas=podatki["cas"],st_igre=podatki["st_igre"])
            del podatki["tekmovanje"]
            del podatki["datum"]
            del podatki["cas"]
            del podatki["st_igre"]
        
        return super().dodaj_vrstico(**podatki)


class Pripada(Tabela):
    """
    Tabela za relacijo pripadnosti igralca ekipi.
    """
    ime = "pripada"
    podatki = "podatki/pripada.csv"

    def __init__(self, conn, ekipa, igralec, tekmovanje):
        """
        Konstruktor tabele pripadnosti ekipi in igralcem.

        Argumenti:
        - conn: povezava na bazo
        - ekipa: tabela za ekipe
        - igralec: tabela za igralce
        """
        super().__init__(conn)
        self.ekipa = ekipa
        self.igralec = igralec
        self.tekmovanje = tekmovanje

    def ustvari(self):
        """
        Ustvari tabelo pripada.
        """
        self.conn.execute("""
            CREATE TABLE pripada (
                igralec           INTEGER REFERENCES igralec(id),
                ekipa             INTEGER REFERENCES ekipa(id),
                tekmovanje        INTEGER REFERENCES tekmovanje(id),
                PRIMARY KEY(igralec, ekipa, tekmovanje)
            );
        """)
        
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj tekmo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        if podatki.get("tip", None) is not None and podatki.get("leto", None) is not None:
            podatki["tekmovanje"] = self.tekmovanje.dodaj_vrstico(tip=podatki["tip"], leto=podatki["leto"])
            del podatki["tip"]
            del podatki["leto"]
        if podatki.get("ime_ekipe", None) is not None:
            podatki["ekipa"] = self.ekipa.dodaj_vrstico(ime=podatki["ime_ekipe"])
            del podatki["ime_ekipe"]
        if podatki.get("ime_igralca", None) is not None:
            podatki["igralec"] = self.igralec.dodaj_vrstico(ime=podatki["ime_igralca"])
            del podatki["ime_igralca"]
        return super().dodaj_vrstico(**podatki)



def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    ekipa = Ekipa(conn)
    tekmovanje = Tekmovanje(conn)
    igralec = Igralec(conn)
    tekma = Tekma(conn)
    nastopa = Nastopa(conn, tekmovanje, ekipa, tekma)
    pripada = Pripada(conn, ekipa, igralec, tekmovanje)
    return [ekipa, tekmovanje, igralec, tekma, nastopa, pripada]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)