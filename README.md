# League of Legends World Championship
AVTORICI: Nežka Srnel, Mojca Šilc

V League of Legends se dve petčlanski ekipi pomerita v spletnem dvoboju, kjer vsak igralec izbere lik s svojimi edinstvenimi sposobnostmi. Cilj je uničiti nasprotnikovo bazo, pri čemer igralci kujejo taktike, nabirajo zlato za opremo ter se spopadajo v bitkah.
Svetovno prvenstvo v LOL je najbolj pomembno tekmovanje v igri, kjer se spopadejo najboljše ekipe s celega sveta. Dogodek se odvija dvakrat na leto (MSI, WORLDS), kjer ekipe tekmujejo za naslov svetovnih prvakov.
Namen najinega projekta je sledenje ekipam na svetovnem prvenstvu skozi čas. Imava bazo s tabelami o igralcih, ekipah, regijah in tekmovanjih. Zanima naju...(coming soon)

cilji:
* lahko iščemo po ekipah in dobimo podatke o njenih trenutnih igralcih, sodelovanju v ligah in dosežke
* lahko iščemo po igralcih in dobimo podatke o njihovi trenutni ekipi, sodelovanju na tekmovanjih 
* lahko izberemo določeno tekmovanje poljubnega leta, in dobimo podatke o ekipah in njenih igralcih ki so sodelovali na tekmovanju in o zmagovalcu 

## Načrt projekta
1. Pridobivanje podatkov
2. Podatki urejeni v bazo
3. Spletni vmesnik za prikazovanje podatkov

## ER-diagram baze
![image](https://github.com/user-attachments/assets/8fefeb43-6984-4063-a6cc-d73a4856d084)

Vsaka ekipa ima pet igralcev, ki se lahko med tekmovanji zamenjajo, prav tako lahko igralci menjajo ekipe. Tekmovanje je sestavljeno iz več tekem, kjer se na vsaki tekmi pomerita dve ekipi. Vsaka tekma je igrana na točno enem tekmovanju. Prisotnost vseh ekip na tekmovanjih ni zagotovljena, saj je število mest omejeno. Vsaka ekipa ima edinstveno ime, vsak igralec pa svoje univerzalno uporabniško ime. Tabela "pripada" povezuje igralce z ekipami za vsako leto. Tabela "nastopa" povezuje ekipe s tekmami, na katerih so igrale, ter nam pove tudi zmagovalca in poraženca. Tekma vsebuje podatke o datumu, času, številu igre ter o tekmovanju, na katerem je bila igrana. Tabela o tekmovanju vsebuje podatke o tipu in letu.


## Povezave do podatkov
* https://oracleselixir.com/


 
