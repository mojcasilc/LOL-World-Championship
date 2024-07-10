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
                id_ekipa    INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES pripada(id_ekipa),
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
        Ustavari tabelo igralci.
        """
        self.conn.execute("""
            CREATE TABLE igralci (
                id_igralec        INTEGER PRIMARY KEY AUTOINCREMENT REFERENCES pripada(id_igralec),
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
        assert "Player" in podatki
        cur = self.conn.execute("""
            SELECT id_igralec FROM igralci
            WHERE Player = :Player;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id


# class Tekmovanje(Tabela):
#     """
#     Tabela za tekmovanja.
#     """
#     ime = "tekmovanje"
#     podatki = "igre.csv"

#     def ustvari(self):
#         """
#         Ustvari tabelo tekmovanje.
#         """
#         self.conn.execute("""
#             CREATE TABLE tekmovanje (
#                 id         INTEGER PRIMARY KEY,
#                 liga       TEXT,
#                 leto       INTEGER
#             );
#         """)

# class Zmagovalci(Tabela):
#     """
#     Tabela za zmagovalce vseh tekmovanj.
#     """
#     ime = "zmagovalci"
#     podatki = ...

#     def ustvari(self):
#         """ustvari tabelo zmagovalci"""
#         self.conn.execute(""" 
#             CREATE TABLE zmagovalci (
#                 ekipa   INTEGER REFERENCES ekipe (id)
#                 tekmovanje INTEGER REFERENCES tekmovanje (id)
#                 PRIMARY KEY (ekipa, tekmovanje))
#         """)

#     def dodaj_vrstico(self, **podatki):
#         """
#         Dodaj relacijo med igralcem in ekipo.

#         Če relacija že obstaja, vrne obstoječi ID.

#         Argumenti:
#         - poimenovani parametri: vrednosti v ustreznih stolpcih
#         """
#         Player = podatki['Player']
#         Team = podatki['Team']

#         r = self.conn.execute("""
#             SELECT * FROM pripada
#             WHERE Player = ? AND Team = ?
#         """, (Player, Team)).fetchone()
#         if r is None:
#             return super().dodaj_vrstico(**podatki)
#         else:
#             id = r
#             return id

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
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                id_igralec   INTEGER,
                id_ekipa     INTEGER,
                leto      INTEGER
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

        
        
# class Nastopa(Tabela):
#     """
#     Tabela za relacijo pripadnosti ekipe tekmovanju.
#     """
#     ime = "nastopa"
#     podatki = "podatki/ekipe.csv"

#     def __init__(self, conn, ekipe, tekmovanje):
#         """
#         Konstruktor tabele pripadnosti tekmovanju.

#         Argumenti:
#         - conn: povezava na bazo
#         - ekipe: tabela za tekmovanja
#         """
#         super().__init__(conn)
#         self.ekipe = ekipe
#         self.tekmovanje = tekmovanje

#     def ustvari(self):
#         """
#         Ustvari tabelo tekmovanja.
#         """
#         self.conn.execute("""
#             CREATE TABLE nastopa (
#                 tekmovanje   INTEGER REFERENCES tekmovanje (id),
#                 ekipa        INTEGER REFERENCES ekipe (id),
#                 PRIMARY KEY (tekmovanje, ekipa)
#             );
#         """)
    
#     def dodaj_vrstico(self, **podatki):
#         """
#         Dodaj relacijo med igralcem in ekipo.
#         Če relacija že obstaja, vrne obstoječi ID.
#         Argumenti:
#         - poimenovani parametri: vrednosti v ustreznih stolpcih
#         """
#         Player = podatki['Player']
#         Team = podatki['Team']
#         r = self.conn.execute("""
#             SELECT * FROM pripada
#             WHERE Player = ? AND Team = ?
#         """, (Player, Team)).fetchone()
#         if r is None:
#             return super().dodaj_vrstico(**podatki)
#         else:
#             id = r
#             return id
        


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
    # tekmovanje = Tekmovanje(conn)
    # nastopa = Nastopa(conn, ekipe, tekmovanje)
    pripada = Pripada(conn)
    return [ekipe, igralci, pripada]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)