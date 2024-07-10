import os
import baza
import sqlite3
from sqlite3 import IntegrityError

#os.remove('lol.db')
conn = sqlite3.connect('lol.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

ekipa, igralci, pripada, tekmovanje, nastopa = baza.pripravi_tabele(conn)

class Igralec:
    '''
    Razred za igralca.
    '''
    def __init__(self, igralec, pos, *, id_igralec):
        """
        Konstruktor igralca.
        """
        self.id_igralec = id_igralec
        self.igralec = igralec
        self.pos = pos

    def __str__(self):
        """
        Znakovna predstavitev igralca. 
        Vrne ime igralca in katero pozicijo igra.
        """
        return self.igralec + " " + self.pos
    
    def poisci_ekipe(self):
        """
        Vrne ekipo igralca po letih in pozicijo, ki jo je igral.
        """
        sql = """
            SELECT i.Player, p.leto, e.Team, i.Pos 
            FROM igralci i
            JOIN pripada p ON i.id_igralec = p.id_igralec
            JOIN ekipe e ON p.id_ekipa = e.id_ekipa
            WHERE i.id_igralec = ?
            ORDER BY p.leto, e.Team
        """
        cursor = conn.execute(sql, (self.id_igralec,))
        for row in cursor.fetchall():
            player, leto, team, pos = row
            yield (player, leto, team, pos)

    @staticmethod
    def poisci(niz, conn):
        """
        Vrne vse igralce, ki v imenu vsebujejo dani niz.
        """
        if not niz:
            return "Vnesi nekaj!"
        
        sql = "SELECT id_igralec, Player, Pos FROM igralci WHERE Player LIKE ? "
        for id_igralec, igralec, pos in conn.execute(sql, [f'%{niz}%']).fetchall():
            yield Igralec(igralec=igralec, pos=pos, id_igralec=id_igralec)

# for igralec in Igralec.poisci('ker', conn):
#     print(f'ID: {igralec.id_igralec}, Player: {igralec.igralec}, Position: {igralec.pos}')

class Ekipa:
    """
    Razred za ekipo.
    """
    def __init__(self, ime, id_ekipa):
        """
        Konstruktor ekipe.
        """
        self.id_ekipa = id_ekipa
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev ekipe.
        Vrne ime ekipe.
        """
        return self.ime  

    def poisci_igralce(self, conn, leto=None):
        """
        Vrne igralce ekipe po letih.
        Če je leto podano, filtrira igralce tudi po letu.
        """

        if leto is None:
            sql = """
                SELECT e.Team, p.leto, i.Player, i.Pos 
                FROM igralci i
                JOIN pripada p ON i.id_igralec = p.id_igralec
                JOIN ekipe e ON p.id_ekipa = e.id_ekipa
                WHERE e.id_ekipa = ?
                ORDER BY p.leto, e.Team
            """
            cursor = conn.execute(sql, (self.id_ekipa,))
        else:
            sql = """
                SELECT  e.Team, p.leto, i.Player, i.Pos 
                FROM igralci i
                JOIN pripada p ON i.id_igralec = p.id_igralec
                JOIN ekipe e ON p.id_ekipa = e.id_ekipa
                WHERE e.id_ekipa = ? AND p.leto = ?
                ORDER BY p.leto, e.Team
            """
            cursor = conn.execute(sql, (self.id_ekipa, leto))

        for row in cursor.fetchall():
            team, leto, player, pos = row
            yield (team, leto, player, pos)

    @staticmethod
    def poisci(niz, conn):
        """
        Vrne vse ekipe, ki v imenu vsebujejo dani niz.
        """
        if niz is None:
            return "Vnesi nekaj!"
        sql = "SELECT id_ekipa, Team FROM ekipe WHERE Team LIKE ?"
        for id_ekipa, ime in conn.execute(sql, [f'%{niz}%']):
            yield Ekipa(id_ekipa=id_ekipa, ime=ime)  

# # Uporaba metode poisci za iskanje ekip (primer)
# for ekipa in Ekipa.poisci('T1', conn):
#     print(f'ID ekipe: {ekipa.id_ekipa}, Ime ekipe: {ekipa.ime}')
    
# print("\nIskanje igralcev samo po ekipi:")
# for igralec in ekipa.poisci_igralce(conn):
#     print(f'Igralec: {igralec[2]}, Leto: {igralec[1]}, Ekipa: {igralec[0]}, Pozicija: {igralec[3]}')

# print("\nIskanje igralcev po ekipi in letu:")
# leto = 2022  # Primer določenega leta
# for igralec in ekipa.poisci_igralce(conn, leto=leto):
#     print(f'Igralec: {igralec[2]}, Leto: {igralec[1]}, Ekipa: {igralec[0]}, Pozicija: {igralec[3]}')

class Tekmovanje:
    """
    Razred za tekmovanje.
    """

    def __init__(self, tip, leto, id_tekmovanja):
        """
        Konstruktor tekmovanja.
        """
        self.id_tekmovanja = id_tekmovanja
        self.tip = tip
        self.leto = leto

    def __str__(self):
        """
        Znakovna predstavitev tekmovanja.
        Vrne tip in leto.
        """
        return self.tip + ", " + self.leto  
    
    def poisci_zmagovalce(self, conn, league=None, year=None):
        """
        Vrne zmagovalce tekmovanja po ligi in/ali letu.
        """
        if league and year:
            sql = """
                SELECT e.Team, t.league, n.datum 
                FROM tekmovanje t
                JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
                JOIN ekipe e ON n.id_ekipa = e.id_ekipa
                WHERE t.league = ? AND t.year = ? AND n.rezultat = 1
                ORDER BY n.datum DESC
                LIMIT 1
            """
            
            cursor = conn.execute(sql, (league, year))

        elif league:
            sql = """
                SELECT e.Team, t.league, n.datum
                FROM tekmovanje t
                JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
                JOIN ekipe e ON n.id_ekipa = e.id_ekipa
                WHERE t.league = ? AND n.rezultat = 1 AND (t.year, n.datum) IN (
                    SELECT t.year, MAX(n.datum)
                    FROM tekmovanje t
                    JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
                    WHERE t.league = ? AND n.rezultat = 1
                    GROUP BY t.year)
                ORDER BY t.year DESC;
            """
            cursor = conn.execute(sql, (league, league)) 

        elif year:
            sql = """
                SELECT e.Team, t.league, n.datum
                FROM tekmovanje t
                JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
                JOIN ekipe e ON n.id_ekipa = e.id_ekipa
                WHERE t.year = ? AND n.rezultat = 1 AND (t.league, n.datum) IN (
                    SELECT t.league, MAX(n.datum)
                    FROM tekmovanje t
                    JOIN nastop n ON t.id_tekmovanja = n.id_tekmovanja
                    WHERE t.year = ? AND n.rezultat = 1
                    GROUP BY t.league)
                ORDER BY t.league, n.datum DESC;
            """
            cursor = conn.execute(sql, (year, year)) 

        return cursor.fetchall()  
        

# tekmovanje = Tekmovanje('WLDs', 2020, 1)

# print("Iskanje zmagovalcev po ligi 'Worlds' in letu 2020:")
# results = tekmovanje.poisci_zmagovalce(conn, league='WLDs', year=2020)
# for result in results:
#     print(f"Ekipa: {result[0]}, Liga: {result[1]}, Datum: {result[2]}")
# print()

# # Primer uporabe za iskanje zmagovalcev tekmovanja samo po ligi
# print("Iskanje zmagovalcev po ligi 'MSI':")
# results = tekmovanje.poisci_zmagovalce(conn, league='MSI')
# for result in results:
#     print(f"Ekipa: {result[0]}, Liga: {result[1]}, Datum: {result[2]}")
# print()

# # Primer uporabe za iskanje zmagovalcev tekmovanja samo po letu
# print("Iskanje zmagovalcev v letu 2023:")
# results = tekmovanje.poisci_zmagovalce(conn, year=2020)
# for result in results:
#     print(f"Ekipa: {result[0]}, Liga: {result[1]}, Datum: {result[2]}")



