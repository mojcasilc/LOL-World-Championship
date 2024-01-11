import pandas as pd 
from pandas.api.types import CategoricalDtype

seznam = []
for leto in range(2014, 2024):
    podatki = pd.read_csv(f"{leto}_LoL_esports_match_data_from_OraclesElixir.csv", low_memory=False)
    podatki = podatki[['gameid', 'league', 'year', 'date', 'game', 'side', 'position', 'playername', 'teamname', 'champion', 'result']] 
    podatki = podatki[(podatki['league']=="WLDs") | (podatki['league']=="MSI")] #izberemo uporabne podatke
    podatki = podatki[((podatki['position'])!="team")]
    seznam.append(podatki)
celota = pd.concat(seznam, ignore_index=True)
celota.league = celota.league.astype(CategoricalDtype(celota.league.drop_duplicates()))
celota.side = celota.side.astype(CategoricalDtype(celota.side.drop_duplicates()))
celota.position = celota.position.astype(CategoricalDtype(celota.position.drop_duplicates()))

###dodaj regije
#regija = celota[[]]
###dodaj kraj tekmovanja

ekipe = celota[['teamname']]
igralci = celota[['playername', 'position']]
tekmovanje = celota[['league', 'year']]
pripada = celota[['year', 'teamname', 'playername']]
nastop = celota[['teamname', 'league', 'year', 'result']]

celota.to_csv('lol.csv', index=False) #podatkovno tabelo zapisemo v datoteko