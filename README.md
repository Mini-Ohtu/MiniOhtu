## Viitteidenhallintaohjelma

[![GHA workflow badge](https://github.com/Mini-Ohtu/MiniOhtu/actions/workflows/codelint.yaml/badge.svg)](https://github.com/Mini-Ohtu/MiniOhtu/actions)

[![GHA workflow badge](https://github.com/Mini-Ohtu/MiniOhtu/actions/workflows/robot.yaml/badge.svg)](https://github.com/Mini-Ohtu/MiniOhtu/actions)
  
[![codecov](https://codecov.io/gh/Mini-Ohtu/MiniOhtu/graph/badge.svg?token=1B01LC5460)](https://codecov.io/gh/Mini-Ohtu/MiniOhtu)

 [Backlog](https://docs.google.com/spreadsheets/d/1Gf4uw0c0myjrpMIgQNJ6P5u_mz90s6L_LBdPb7gv93k/edit?usp=sharing)

### Definition of done

- User story täyttää siille määritellyt hyväksymiskriteerit.
- Toteutetun koodin testikattavuus on kohtuullinen (vähintään  80 %).
- Asiakas pääsee näkemään koko ajan koodin ja testien tilanteen CI-palvelusta.
- Koodi ylläpidettävyys on hyvää:
    - luokat, muuttujat ja metodit on nimetty selkeästi.
    - sovelluksen arkkitehtuuri on järkevä.
    - koodityyli on yhtenäinen (valvotaan Pylintin avulla).


### Asennus- ja käyttöohjeet
1. Kloonaa repositorio
SSH:
```
git clone git@github.com:Mini-Ohtu/MiniOhtu.git
```
HTTPS:
```
git clone git@github.com:Mini-Ohtu/MiniOhtu.git
```
https://github.com/Mini-Ohtu/MiniOhtu.git

2. Asenna riippuvuudet
```
poetry install
```
3. Luo .env-tiedosto sovelluksen juureen 
Lisää seuraava sisältö .env-tiedostoon.
Lisää tietokannan osoite, voit käyttää esim. ilmaista aiven.io-pilvipalvelua. 
```
DATABASE_URL=postgresql://xxx
TEST_ENV=true
SECRET_KEY=satunnainen_merkkijono
```

4. Siirry  virtuaaliympäristöön
```
eval "$(poetry env activate)"
```

5. Alusta tietokanta
```
python src/db_helper.py
```
 
6. Käynnistä ohjelma
```
python src/index.py
```