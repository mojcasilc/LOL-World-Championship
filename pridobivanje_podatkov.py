import pandas as pd 

seznam1 = pd.DataFrame()

# podatki za tekmovanje tipa WLDs in MSI
for leto in range(2014, 2025):
    podatki = pd.read_csv(f"match_data/{leto}_LoL_esports_match_data_from_OraclesElixir.csv", low_memory=False)
    podatki = podatki[['league', 'year', 'date', 'game', 'position', 'playername', 'teamname', 'result']]
    podatki[['date', 'time']] = podatki['date'].str.split(' ', expand=True)
    podatki = podatki[(podatki['league']=="WLDs") | (podatki['league']=="MSI")] # izberemo uporabne podatke
    podatki = podatki[((podatki['position'])!="team")] # zanimajo nas igralci
    seznam1 = pd.concat([seznam1, podatki], ignore_index=True)

# Preimenujemo stolpce
new_column_names = {
    'league': 'tip',
    'year': 'leto',
    'date': 'datum',
    'game': 'st_igre',
    'position': 'pozicija',
    'playername': 'ime_igralca',
    'teamname': 'ime_ekipe',
    'result': 'zmaga',
    'time': 'cas'}
seznam1 = seznam1.rename(columns=new_column_names)

pripada = seznam1[['ime_ekipe', 'ime_igralca', 'tip', 'leto']].drop_duplicates()
igra = seznam1[['tip', 'leto', 'datum', 'cas', 'st_igre', 'ime_ekipe', 'zmaga']].drop_duplicates()

igra.to_csv('podatki/igra.csv', index=False)
pripada.to_csv('podatki/pripada.csv', index=False)



