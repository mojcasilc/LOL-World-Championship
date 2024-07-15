import os
import baza
import sqlite3
from sqlite3 import IntegrityError

# os.remove('lol.db')
conn = sqlite3.connect('lol.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

ekipa, tekmovanje, igralec, tekma, nastopa, pripada = baza.pripravi_tabele(conn)

class Igralec:
    '''
    Razred za igralca.
    '''
    def __init__(self, id=None, ime=None):
        """
        Konstruktor igralca.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev filma.
        Vrne naslov filma.
        """
        return self.ime
    
    @staticmethod
    def z_id(id):
        """
        Vrne igralca z navedenim ID-jem.
        """
        sql = """
          SELECT id, ime FROM igralec WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [id])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Film z ID-jem {id} ne obstaja!")
            return Igralec(*vrstica)
        finally:
            cur.close()

    @staticmethod
    def seznam(seznam_idjev):
        if not seznam_idjev:
            return []
        elif len(seznam_idjev) == 1:
            id, = seznam_idjev
            return [Igralec.z_id(id)]
        sql = f"""
          SELECT id, ime FROM igralec
           WHERE id IN ({', '.join(['?'] * len(seznam_idjev))})
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, seznam_idjev)
            slovar = {id: Igralec(id, ime) for id, ime in cur}
            return [slovar[id] for id in seznam_idjev]
        finally:
            cur.close()
    
    def poisci_tekmovanja(self):
        """
        Vrne tekmovanja igralca po letih ko je igral.
        """
        sql = """
            SELECT t.id, t.tip, t.leto
            FROM igralec i
            JOIN pripada p ON i.id = p.igralec
            JOIN tekmovanje t ON p.tekmovanje = t.id
            WHERE i.id = ?
            ORDER BY t.leto DESC, t.tip
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [(Tekmovanje(*podatki)) for podatki in cur]
        finally:
            cur.close()

    @staticmethod
    def poisci(niz):
        """
        Vrne vse igralce, ki v imenu vsebujejo dani niz.
        """
        sql = "SELECT id, ime FROM igralec WHERE ime LIKE ?"
        cur = conn.cursor()
        try:
            cur.execute(sql, ['%' + niz + '%'])
            return [Igralec(*vrstica) for vrstica in cur]
        finally:
            cur.close()

class Ekipa:
    """
    Razred za ekipo.
    """
    def __init__(self, id=None, ime=None):
        """
        Konstruktor ekipe.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev ekipe.
        Vrne ime ekipe.
        """
        return self.ime  

    @staticmethod
    def z_id(id):
        """
        Vrne igralca z navedenim ID-jem.
        """
        sql = """
          SELECT id, ime FROM ekipa WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [id])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Ekipa z ID-jem {id} ne obstaja!")
            return Ekipa(*vrstica)
        finally:
            cur.close()

    @staticmethod
    def seznam(seznam_idjev):
        if not seznam_idjev:
            return []
        elif len(seznam_idjev) == 1:
            id, = seznam_idjev
            return [Ekipa.z_id(id)]
        sql = f"""
          SELECT id, ime FROM ekipa
           WHERE id IN ({', '.join(['?'] * len(seznam_idjev))})
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, seznam_idjev)
            slovar = {id: Ekipa(id, ime) for id, ime in cur}
            return [slovar[id] for id in seznam_idjev]
        finally:
            cur.close()
    
    def poisci_tekmovanja(self):
        """
        Vrne tekmovanja ekipe po letih ko je igrala.
        """
        sql = """
            SELECT e.ime, t.tip, t.leto
            FROM ekipa e
            JOIN pripada p ON e.id = p.ekipa
            JOIN tekmovanje t ON p.tekmovanje = t.id
            WHERE e.id = 4
            ORDER BY t.leto DESC, t.tip
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [(ime, tip, leto) for ime, tip, leto in cur]
        finally:
            cur.close()

    @staticmethod
    def poisci(niz):
        """
        Vrne vse igralce, ki v imenu vsebujejo dani niz.
        """
        sql = "SELECT id, ime FROM ekipa WHERE ime LIKE ?"
        cur = conn.cursor()
        try:
            cur.execute(sql, ['%' + niz + '%'])
            return [Igralec(*vrstica) for vrstica in cur]
        finally:
            cur.close()

class Tekmovanje:
    """
    Razred za ekipo.
    """
    def __init__(self, id=None, tip=None, leto=None):
        """
        Konstruktor ekipe.
        """
        self.id = id
        self.tip = tip
        self.leto = leto

    def __str__(self):
        """
        Znakovna predstavitev ekipe.
        Vrne ime ekipe.
        """
        return self.tip + " " + self.leto  




# class Tekmovanje:
#     """
#     Razred za tekmovanje.
#     """

#     def __init__(self, tip, leto, id_tekmovanja):
#         """
#         Konstruktor tekmovanja.
#         """
#         self.id_tekmovanja = id_tekmovanja
#         self.tip = tip
#         self.leto = leto

#     def __str__(self):
#         """
#         Znakovna predstavitev tekmovanja.
#         Vrne tip in leto.
#         """
#         return self.tip + ", " + self.leto  
    
#     def poisci_zmagovalce(self, conn, league=None, year=None):
#         """
#         Vrne zmagovalce tekmovanja po ligi in/ali letu.
#         """
#         if league and year:
#             sql = """
#                 SELECT e.Team, t.league, n.datum 
#                 FROM tekmovanje t
#                 JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                 JOIN ekipe e ON n.id_ekipa = e.id_ekipa
#                 WHERE t.league = ? AND t.year = ? AND n.rezultat = 1
#                 ORDER BY n.datum DESC
#                 LIMIT 1
#             """
            
#             cursor = conn.execute(sql, (league, year))

#         elif league:
#             sql = """
#                 SELECT e.Team, t.league, n.datum
#                 FROM tekmovanje t
#                 JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                 JOIN ekipe e ON n.id_ekipa = e.id_ekipa
#                 WHERE t.league = ? AND n.rezultat = 1 AND (t.year, n.datum) IN (
#                     SELECT t.year, MAX(n.datum)
#                     FROM tekmovanje t
#                     JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                     WHERE t.league = ? AND n.rezultat = 1
#                     GROUP BY t.year)
#                 ORDER BY t.year DESC;
#             """
#             cursor = conn.execute(sql, (league, league)) 

#         elif year:
#             sql = """
#                 SELECT e.Team, t.league, n.datum
#                 FROM tekmovanje t
#                 JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                 JOIN ekipe e ON n.id_ekipa = e.id_ekipa
#                 WHERE t.year = ? AND n.rezultat = 1 AND (t.league, n.datum) IN (
#                     SELECT t.league, MAX(n.datum)
#                     FROM tekmovanje t
#                     JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                     WHERE t.year = ? AND n.rezultat = 1
#                     GROUP BY t.league)
#                 ORDER BY t.league, n.datum DESC;
#             """
#             cursor = conn.execute(sql, (year, year)) 

#         else:
#             sql = """
#                 SELECT e.Team, t.league, t.year, n.datum
#                 FROM tekmovanje t
#                 JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                 JOIN ekipe e ON n.id_ekipa = e.id_ekipa
#                 WHERE n.rezultat = 1 AND (t.league, t.year, n.datum) IN (
#                     SELECT t.league, t.year, MAX(n.datum)
#                     FROM tekmovanje t
#                     JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
#                     WHERE n.rezultat = 1
#                     GROUP BY t.league, t.year)
#                 ORDER BY n.datum DESC, t.league
#             """
#             cursor = conn.execute(sql)

#         return cursor.fetchall()  