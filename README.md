# League of Legends World Championship
AVTORICI: Nežka Srnel, Mojca Šilc

V League of Legends se dve petčlanski ekipi pomerita v spletnem dvoboju, kjer vsak igralec izbere lik s svojimi edinstvenimi sposobnostmi. Cilj je uničiti nasprotnikovo bazo, pri čemer igralci kujejo taktike, nabirajo zlato za opremo ter se spopadajo v bitkah.
Svetovno prvenstvo v LOL je najbolj pomembno tekmovanje v igri, kjer se spopadejo najboljše ekipe s celega sveta. Dogodek se odvija dvakrat na leto (MSI, WORLDS), kjer ekipe tekmujejo za naslov svetovnih prvakov.

Namen najinega projekta je sledenje ekipam na svetovnem in medsezonskem prvenstvu skozi čas.
V primeru, da želite vse skupaj stestirati, je postopek sledeč:
1. prenesite celoten repozitorij
2. poženite pridobivanje_podatkov.py
3. poženite model.py
4. poženite spletni_vmesnik.py in kliknite na ustvarjeno povezavo

cilji:
* lahko iščemo po ekipah in dobimo podatke o njenih trenutnih igralcih, sodelovanju v ligah in dosežke
* lahko iščemo po igralcih in dobimo podatke o sodelovanju na tekmovanjih 
* lahko izberemo določeno tekmovanje poljubnega leta, in dobimo podatke o ekipah in njenih igralcih ki so sodelovali na tekmovanju in top treh ekipah.

## Načrt projekta
1. Pridobivanje podatkov
2. Podatki urejeni v bazo
3. Spletni vmesnik za prikazovanje podatkov

## ER-diagram baze
![image](https://github.com/user-attachments/assets/8fefeb43-6984-4063-a6cc-d73a4856d084)

Vsaka ekipa je sestavljena iz petih igralcev, ki se lahko med tekmovanji zamenjajo, prav tako lahko igralci zamenjajo ekipe. Vsaka ekipa ima edinstveno ime, vsak igralec pa svoje univerzalno uporabniško ime. Tekmovanje je sestavljeno iz več tekem, kjer se na vsaki tekmi pomerita dve ekipi. Vsaka tekma je igrana na točno enem tekmovanju. Posamezna tekma je sestavljena iz 3 do 5 iger, pri čemer zmaga ekipa, ki prva doseže 3 zmage v igrah. Prisotnost vseh ekip na tekmovanjih ni zagotovljena, saj je število mest omejeno. Igralci znotraj ekipe ostajajo enaki na vseh tekmah v okviru istega tekmovanja. Tabela "pripada" povezuje igralce z ekipami za vsako tekmovanje. Tabela "nastopa" povezuje ekipe z igrami, na katerih so igrale, ter nam pove tudi zmagovalca in poraženca. Tabela "igra" vsebuje podatke o datumu, času, številu igre ter o tekmovanju, na katerem je bila igrana. Tabela "tekmovanje" vsebuje podatke o tipu (MSI, WORLDS) in letu.


## Povezave do podatkov
* https://oracleselixir.com/


 
