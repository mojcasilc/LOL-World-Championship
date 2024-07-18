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
        sql = """
            SELECT id, ime FROM igralec
            WHERE ime LIKE ?
            ORDER BY ime
            """
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
            SELECT DISTINCT t.id, t.tip, t.leto
            FROM ekipa e
            JOIN pripada p ON e.id = p.ekipa
            JOIN tekmovanje t ON p.tekmovanje = t.id
            WHERE e.id = ?
            ORDER BY t.leto DESC, t.tip
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [Tekmovanje(*podatki) for podatki in cur]
        finally:
            cur.close()

    @staticmethod
    def poisci(niz):
        """
        Vrne vse ekipe, ki v imenu vsebujejo dani niz.
        """
        sql = "SELECT id, ime FROM ekipa WHERE ime LIKE ?"
        cur = conn.cursor()
        try:
            cur.execute(sql, ['%' + niz + '%'])
            return [Igralec(*vrstica) for vrstica in cur]
        finally:
            cur.close()
    
    def igralci(self, tekmovanje):
        """
        Vrne igralce, ki so bili na tekmovanje 'tekmovanje' v ekipi
        """
        sql = """
            SELECT i.id, i.ime FROM ekipa e
            JOIN pripada p ON e.id = p.ekipa
            JOIN igralec i ON p.igralec = i.id
            JOIN tekmovanje t ON p.tekmovanje = t.id
            WHERE e.id = ? AND t.id = ?
            ORDER BY i.ime
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id, tekmovanje])
            return [Igralec(*podatki) for podatki in cur]
        finally:
            cur.close()
    
    def zmage(self):
        """
        Vrne tekmovanja na akterih je ekipa zmagala
        """
        sql = """
            WITH zmagovalci AS (
            SELECT t.id AS id, t.tip AS tip, t.leto AS leto, MAX(a.st_igre), n.zmaga, e.id AS id_ekipe
            FROM ekipa e
            JOIN nastopa n ON e.id = n.ekipa
            JOIN tekma a ON n.tekma = a.id
            JOIN tekmovanje t ON t.id = a.tekmovanje
            WHERE n.zmaga = 1 AND a.datum IN (
                SELECT MAX(a.datum) FROM tekma a
                JOIN tekmovanje t ON t.id = a.tekmovanje
                GROUP BY t.id
                )
            GROUP BY t.id
            ORDER BY t.id)

            SELECT id, tip, leto FROM zmagovalci
            WHERE id_ekipe = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [Tekmovanje(*podatki) for podatki in cur]
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
    
    @staticmethod
    def z_id(id):
        """
        Vrne tekmovanje z navedenim ID-jem.
        """
        sql = """
          SELECT id, tip, leto FROM tekmovanje WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [id])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Ekipa z ID-jem {id} ne obstaja!")
            return Tekmovanje(*vrstica)
        finally:
            cur.close()
        
    def tekme(self):
        """
        Vrne tekme,ki so se odvijale na tekmovanju
        """
        sql = """
            WITH ekipa1 AS (
            SELECT a.id, a.tekmovanje, a.datum, a.cas, a.st_igre, e.* FROM tekmovanje t
            JOIN tekma a ON t.id = a.tekmovanje
            JOIN nastopa n ON a.id = n.tekma
            JOIN ekipa e ON e.id = n.ekipa
            WHERE t.id = ? AND st_igre = 1 AND zmaga = 1),

                ekipa2 AS (
            SELECT a.id, a.tekmovanje, a.datum, a.cas, a.st_igre, e.*  FROM tekmovanje t
            JOIN tekma a ON t.id = a.tekmovanje
            JOIN nastopa n ON a.id = n.tekma
            JOIN ekipa e ON e.id = n.ekipa
            WHERE t.id = ? AND st_igre = 1 AND zmaga = 0)

            SELECT * FROM ekipa1 e1
            JOIN ekipa2 e2 USING (id, tekmovanje, datum, cas, st_igre)
            ORDER BY datum, cas
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id,self.id])
            return {Tekma(*podatki): [Ekipa(id=id1, ime=ime1),Ekipa(id=id2, ime=ime2)] for *podatki, id1, ime1, id2, ime2 in cur}
        finally:
            cur.close()
    
    def prva_ekipa(self):
        """
        Vrne zmagovalno ekipo
        """
        sql = """
            SELECT e.id, e.ime
            FROM tekmovanje t
            JOIN tekma a ON t.id = a.tekmovanje
            JOIN nastopa n ON a.id = n.tekma
            JOIN ekipa e ON n.ekipa = e.id
            WHERE t.id = ? AND n.zmaga = 1
            ORDER BY a.datum DESC, a.cas DESC
            LIMIT 1
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [Ekipa(*podatki) for podatki in cur]
        finally:
            cur.close()
    
    def druga_ekipa(self):
        """
        Vrne zmagovalno ekipo
        """
        sql = """
            SELECT e.id, e.ime
            FROM tekmovanje t
            JOIN tekma a ON t.id = a.tekmovanje
            JOIN nastopa n ON a.id = n.tekma
            JOIN ekipa e ON n.ekipa = e.id
            WHERE t.id = ? AND n.zmaga = 0
            ORDER BY a.datum DESC, a.cas DESC
            LIMIT 1
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [Ekipa(*podatki) for podatki in cur]
        finally:
            cur.close()

    def tretja_ekipa(self):
        """
        Vrne zmagovalno ekipo
        """
        sql = """
            SELECT e.id, e.ime, MAX(a.st_igre)
            FROM ekipa e
            JOIN nastopa n ON e.id = n.ekipa
            JOIN tekma a ON n.tekma = a.id
            JOIN tekmovanje t ON t.id = a.tekmovanje
            WHERE t.id = ? AND n.zmaga=0 AND a.datum IN (
                SELECT DISTINCT a.datum FROM tekma a
                JOIN tekmovanje t ON t.id = a.tekmovanje
                WHERE t.id = ?
                ORDER BY a.datum DESC
                LIMIT 2 OFFSET 1)
            GROUP BY a.datum
            ORDER BY e.ime
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id, self.id])
            return [Ekipa(*podatki) for *podatki, _ in cur]
        finally:
            cur.close()
    
    @staticmethod
    def vsa_tekmovanja():
        '''vrne vsa tekmovanja od leta 2014'''
        sql = """
            SELECT * FROM tekmovanje
            ORDER BY leto DESC
        """
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return [Tekmovanje(*podatki) for podatki in cur]
        finally:
            cur.close()

    

class Tekma:
    """
    Razred za ekipo.
    """
    def __init__(self, id=None, tekmovanje=None, datum=None, cas=None, st_igre=None):
        """
        Konstruktor ekipe.
        """
        self.id = id
        self.tekmovanje = tekmovanje
        self.datum = datum
        self.cas = cas
        self.st_igre = st_igre

    def __str__(self):
        """
        Znakovna predstavitev ekipe.
        Vrne ime ekipe.
        """
        return self.st_igre + " " + self.datum + " " + self.cas