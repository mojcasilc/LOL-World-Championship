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

ekipe = teams[['Team']] # naredi kategorijo in preimenuj v ime

# to spremeni v csv (glej primer spodaj)
# igralci = players[['player', 'pos']]
# tekmovanje = celota[['league', 'year', 'teamname']]
# pripada = players[['leto', 'team', 'player']]
# nastop = celota[['teamname', 'league', 'year', 'result']]

ekipe.to_csv('ekipe.csv', index=False)

