import csv

PARAM_FMT = ":{}" # za SQLite


class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.

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
            podatki = csv.reader(datoteka)
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
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


class Ekipe(Tabela):
    """
    Tabela za ekipe.
    """
    ime = "ekipe"
    podatki = "podatki/ekipe.csv"

    def ustvari(self):
        """
        Ustvari tabelo ekipe.
        """
        self.conn.execute("""
            CREATE TABLE ekipe (
                id_ekipa    INTEGER PRIMARY KEY AUTOINCREMENT,
                Team TEXT UNIQUE
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj ekipo.

        Če ekipe že obstaja, vrne obstoječi ID.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert "Team" in podatki
        cur = self.conn.execute("""
            SELECT id_ekipa FROM ekipe
            WHERE Team = :Team;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id


class Igralci(Tabela):
    """
    Tabela za igralce.
    """
    ime = "igralci"
    podatki = "podatki/igralci.csv"

    def ustvari(self):
        """
        Ustvari tabelo igralci.
        """
        self.conn.execute("""
            CREATE TABLE igralci (
                id_igralec        INTEGER PRIMARY KEY AUTOINCREMENT,
                Player       TEXT,
                Pos     TEXT
            );
        """)
    
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj igralca.
        Če igralec že obstaja, vrne obstoječi ID.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
    
        igralec = podatki['Player']
        position = podatki['Pos']

        cur = self.conn.execute("""
            SELECT id_igralec FROM igralci
            WHERE Player = ? AND Pos = ?;
        """, (igralec, position))
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
    podatki = "podatki/tekmovanje.csv"

    def ustvari(self):
        """
        Ustvari tabelo tekmovanje.
        """
        self.conn.execute("""
            CREATE TABLE tekmovanje (
                id_tekmovanja         INTEGER PRIMARY KEY,
                league       TEXT,
                year       INTEGER
            );
        """)
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj tekmovanje.

        Če tekmovanje že obstaja, vrne obstoječi ID.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        assert "id_tekmovanja" in podatki
        cur = self.conn.execute("""
            SELECT id_tekmovanja FROM tekmovanje
            WHERE id_tekmovanja = :id_tekmovanja;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id


class Pripada(Tabela):
    """
    Tabela za relacijo pripadnosti tekmovalca ekipi.
    """
    ime = "pripada"
    podatki = "podatki/pripada.csv"

    def ustvari(self):
        """
        Ustvari tabelo pripada.
        """
        self.conn.execute("""
            CREATE TABLE pripada (
                id_igralec   INTEGER REFERENCES igralci(id_igralec),
                id_ekipa     INTEGER REFERENCES ekipe(id_ekipa),
                leto         INTEGER,
                PRIMARY KEY(id_igralec, id_ekipa, leto)
            );
        """)
        
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj relacijo med igralcem in ekipo.

        Če relacija že obstaja, vrne obstoječi ID.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        
        igralec = podatki['Player']
        ekipa = podatki['Team']
        leto = podatki['leto']

        id_igralec = self.conn.execute("""
            SELECT id_igralec FROM igralci
            WHERE Player = ? 
        """, (igralec,)).fetchone()

        id_ekipa = self.conn.execute("""
            SELECT id_ekipa FROM ekipe
            WHERE Team = ? 
        """, (ekipa,)).fetchone()

        if id_igralec is None or id_ekipa is None:
            return None
        
        id_igralec = id_igralec[0]
        id_ekipa = id_ekipa[0]

        r = self.conn.execute("""
            SELECT * FROM pripada
            WHERE id_igralec = ? AND id_ekipa = ? AND leto = ?
        """, (id_igralec, id_ekipa, leto)).fetchone()

        if r is None:
            return super().dodaj_vrstico(id_igralec=id_igralec, id_ekipa=id_ekipa, leto=leto)
        else:
            return r[0]

        
        
class Nastop(Tabela):
    """
    Tabela za relacijo pripadnosti ekipe tekmovanju.
    """
    ime = "nastop"
    podatki = "podatki/nastop.csv"

    def ustvari(self):
        """
        Ustvari tabelo nastopov.
        """
        self.conn.execute("""
            CREATE TABLE nastop (
                id_tekmovanja   INTEGER REFERENCES tekmovanje(id_tekmovanja),
                id_ekipa        INTEGER REFERENCES ekipe(id_ekipa),
                datum           DATE,
                st_tekme        INTEGER,
                rezultat        INTEGER,  
                PRIMARY KEY(id_tekmovanja, id_ekipa, datum, st_tekme)
            );
        """)
    
    def dodaj_vrstico(self, **podatki):
        """
        Dodaj relacijo med igralcem in ekipo.

        Če relacija že obstaja, vrne obstoječi ID.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        
        tekmovanje = podatki['league']
        leto = podatki['date'].split(' ')[0].split('-')[0]
        ekipa = podatki['teamname']
        datum = podatki['date']
        rezultat = podatki['result']
        st_tekme = podatki['game']
        
        id_tekmovanja = self.conn.execute("""
            SELECT id_tekmovanja FROM tekmovanje
            WHERE league = ? AND year = ?
        """, (tekmovanje, leto)).fetchone()

        id_ekipa = self.conn.execute("""
            SELECT id_ekipa FROM ekipe
            WHERE Team = ? 
        """, (ekipa,)).fetchone()

        if id_tekmovanja is None or id_ekipa is None:
            return None
        
        id_tekmovanja = id_tekmovanja[0]
        id_ekipa = id_ekipa[0]

        r = self.conn.execute("""
            SELECT * FROM nastop
            WHERE id_tekmovanja = ? AND id_ekipa = ? AND datum = ? AND st_tekme = ? AND rezultat = ?
        """, (id_tekmovanja, id_ekipa, datum, st_tekme, rezultat)).fetchone()

        if r is None:
            return super().dodaj_vrstico(id_tekmovanja=id_tekmovanja, id_ekipa=id_ekipa, datum=datum, st_tekme=st_tekme, rezultat=rezultat)
        else:
            return r[0]
        


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
    ekipe = Ekipe(conn)
    igralci = Igralci(conn)
    tekmovanje = Tekmovanje(conn)
    nastopa = Nastop(conn)
    pripada = Pripada(conn)
    return [ekipe, igralci, pripada, tekmovanje, nastopa]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)