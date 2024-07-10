import pandas as pd 
from pandas.api.types import CategoricalDtype

seznam1 = []
seznam2 = []
seznam3 = []
for leto in range(2014, 2024):
    podatki = pd.read_csv(f"match_data/{leto}_LoL_esports_match_data_from_OraclesElixir.csv", low_memory=False)
    podatki = podatki[['gameid', 'league', 'year', 'date', 'game', 'side', 'position', 'playername', 'teamname', 'champion', 'result']] 
    podatki = podatki[(podatki['league']=="WLDs") | (podatki['league']=="MSI")] #izberemo uporabne podatke
    podatki = podatki[((podatki['position'])!="team")]
    seznam1.append(podatki)

    podatki_players_wlds = pd.read_csv(f"worlds/Worlds {leto} - Player Stats - OraclesElixir.csv")
    podatki_players_wlds = podatki_players_wlds[['Player', 'Team', 'Pos', 'GP']]
    stolpec_leto1 = {'leto': leto, 'tekmovanje': 'WLDs'}
    podatki_players_wlds = podatki_players_wlds.assign(**stolpec_leto1)
    seznam2.append(podatki_players_wlds)

    podatki_teams_wlds = pd.read_csv(f"worlds/Worlds {leto} - Team Stats - OraclesElixir.csv")
    podatki_teams_wlds = podatki_teams_wlds[['Team', 'GP', 'W', 'L']]
    podatki_teams_wlds= podatki_teams_wlds.assign(**stolpec_leto1)
    seznam3.append(podatki_teams_wlds)

    if leto != 2019 and leto != 2023: 
        podatki_players_msi = pd.read_csv(f"msi/MSI {leto+1} - Player Stats - OraclesElixir.csv")
        podatki_players_msi = podatki_players_msi[['Player', 'Team', 'Pos', 'GP']]
        stolpec_leto2 = {'leto': leto+1, 'tekmovanje': 'MSI'}
        podatki_players_msi = podatki_players_msi.assign(**stolpec_leto2)
        seznam2.append(podatki_players_msi)

        podatki_teams_msi = pd.read_csv(f"msi/MSI {leto+1} - Team Stats - OraclesElixir.csv")
        podatki_teams_msi = podatki_teams_msi[['Team', 'GP', 'W', 'L']]
        podatki_teams_msi = podatki_teams_msi.assign(**stolpec_leto2)
        seznam3.append(podatki_teams_msi)

celota = pd.concat(seznam1, ignore_index=True)
players = pd.concat(seznam2, ignore_index=True)
teams = pd.concat(seznam3, ignore_index=True)

ekipe = teams[['Team']].drop_duplicates() # naredi kategorijo in preimenuj v ime, unique
igralci = players[['Player', 'Pos']].drop_duplicates().sort_values(by='Player')
pripada = players[['leto', 'Team', 'Player']].sort_values(by=['leto', 'Team'])
nastop = celota[['league', 'date', 'game', 'teamname', 'result']].drop_duplicates()
tekmovanje = celota[['league', 'year']].drop_duplicates()

# #spremenimo datum
# nastop['datum'] = nastop['date'].str.split(' ').str[0]

#dodamo id v datoteke
ekipe.insert(0,'id_ekipa', range(1, len(ekipe)+1))
igralci.insert(0,'id_igralec', range(1, len(igralci)+1))
nastop.insert(0,'id_igre', range(1, len(nastop)+1))
tekmovanje.insert(0, 'id_tekmovanja', range(1, len(tekmovanje)+1))

# to spremeni v csv 
ekipe.to_csv('podatki/ekipe.csv', index=False)
igralci.to_csv('podatki/igralci.csv', index=False)
pripada.to_csv('podatki/pripada.csv', index=False)
nastop.to_csv('podatki/nastop.csv', index=False)
tekmovanje.to_csv('podatki/tekmovanje.csv', index=False)


