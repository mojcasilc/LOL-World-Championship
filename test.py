import os
import baza
import sqlite3
from sqlite3 import IntegrityError

os.remove('lol.db')
conn = sqlite3.connect('lol.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

# uporabnik, zanr, oznaka, film, oseba, vloga, pripada = baza.pripravi_tabele(conn)
ekipa, igralci, pripada = baza.pripravi_tabele(conn)
