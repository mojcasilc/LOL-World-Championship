import pandas as pd 
from pandas.api.types import CategoricalDtype

seznam1 = pd.DataFrame()
seznam2 = []
seznam3 = []

# podatki za tekmovanje tipa WLDs in MSI
for leto in range(2014, 2024):
    podatki = pd.read_csv(f"match_data/{leto}_LoL_esports_match_data_from_OraclesElixir.csv", low_memory=False)
    podatki = podatki[['gameid', 'league', 'year', 'date', 'game', 'side', 'position', 'playername', 'playerid', 'teamname', 'teamid', 'champion', 'result']]
    podatki[['date', 'time']] = podatki['date'].str.split(' ', expand=True)
    podatki = podatki[(podatki['league']=="WLDs") | (podatki['league']=="MSI")] # izberemo uporabne podatke
    podatki = podatki[((podatki['position'])!="team")] # zanimajo nas igralci
    seznam1 = pd.concat([seznam1, podatki], ignore_index=True)

#  gameid	       league	year	    date	          game   side        position	playername	       teamname	       champion	 result
# TRLH3/1000430019	WLDs	2014	18.09.2014 08:59	   1	 Blue	      top	      Korol	         EDward Gaming	    Maokai	    0
# TRLH3/1000430019	WLDs	2014	18.09.2014 08:59	   1	 Blue	      jng	      Clearlove	     EDward Gaming	    Jarvan IV	0

# Preimenujemo stolpce
new_column_names = {
    'gameid': 'id_tekme',
    'league': 'tip',
    'year': 'leto',
    'date': 'datum',
    'game': 'st_tekme',
    'side': 'stran',
    'position': 'pozicija',
    'playername': 'ime_igralca',
    'playerid' : 'id_igralca',
    'teamname': 'ime_ekipe',
    'teamid': 'id_ekipe',
    'champion': 'champion',
    'result': 'zmaga',
    'time': 'cas'}
seznam1 = seznam1.rename(columns=new_column_names)


    # podatki_players_wlds = pd.read_csv(f"worlds/Worlds {leto} - Player Stats - OraclesElixir.csv")
    # podatki_players_wlds = podatki_players_wlds[['Player', 'Team', 'Pos', 'GP']]
    # stolpec_leto1 = {'leto': leto, 'tekmovanje': 'WLDs'}
    # podatki_players_wlds = podatki_players_wlds.assign(**stolpec_leto1)
    # seznam2.append(podatki_players_wlds)


    # podatki_teams_wlds = pd.read_csv(f"worlds/Worlds {leto} - Team Stats - OraclesElixir.csv")
    # podatki_teams_wlds = podatki_teams_wlds[['Team', 'GP', 'W', 'L']]
    # podatki_teams_wlds= podatki_teams_wlds.assign(**stolpec_leto1)
    # seznam3.append(podatki_teams_wlds)

    # if leto != 2019 and leto != 2023: 
    #     podatki_players_msi = pd.read_csv(f"msi/MSI {leto+1} - Player Stats - OraclesElixir.csv")
    #     podatki_players_msi = podatki_players_msi[['Player', 'Team', 'Pos', 'GP']]
    #     stolpec_leto2 = {'leto': leto+1, 'tekmovanje': 'MSI'}
    #     podatki_players_msi = podatki_players_msi.assign(**stolpec_leto2)
    #     seznam2.append(podatki_players_msi)

    #     podatki_teams_msi = pd.read_csv(f"msi/MSI {leto+1} - Team Stats - OraclesElixir.csv")
    #     podatki_teams_msi = podatki_teams_msi[['Team', 'GP', 'W', 'L']]
    #     podatki_teams_msi = podatki_teams_msi.assign(**stolpec_leto2)
    #     seznam3.append(podatki_teams_msi)

# celota = pd.concat(seznam1, ignore_index=True)
# celota.loc[celota['teamname'] == 'KaBuM! e-Sports', 'teamname'] = 'KaBuM! Esports'

# players = pd.concat(seznam2, ignore_index=True)
# teams = pd.concat(seznam3, ignore_index=True)

# igralci = seznam1[['ime_igralca']].drop_duplicates()
# ekipe = seznam1[['ime_ekipe']].drop_duplicates()
# tekmovanje = seznam1[['tip', 'leto']].drop_duplicates()
pripada = seznam1[['ime_ekipe', 'ime_igralca', 'tip', 'leto']].drop_duplicates()
tekma = seznam1[['tip', 'leto', 'datum', 'cas', 'st_tekme', 'ime_ekipe', 'zmaga']].drop_duplicates()
# tekma = tekma[(tekma['zmaga']==1)]
# tekma = tekma[['id_tekme', 'tip', 'leto', 'datum', 'cas', 'st_tekme', 'id_ekipe']].drop_duplicates()
# nastopa = seznam1[['id_ekipe', 'id_tekme']].drop_duplicates()

# to spremeni v csv 
# ekipe.to_csv('podatki/ekipa.csv', index=False)
# igralci.to_csv('podatki/igralec.csv', index=False)
tekma.to_csv('podatki/tekma.csv', index=False)
# tekmovanje.to_csv('podatki/tekmovanje.csv', index=False)
pripada.to_csv('podatki/pripada.csv', index=False)
# nastopa.to_csv('podatki/nastopa.csv', index=False)


