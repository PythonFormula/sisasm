# SiSAsm

Sanoista **Si**mple **S**low **As**se**m**bly.

Kaikki koodi, kommentit, git versiohistoria, yms. on englanniksi. Suomenkieliset selityksen ohjelman toiminnasta löytyy [täältä](#Ohjelman-toiminta).

## Asentaminen

Lataa repo itsellesi komennolla `git clone https://github.com/PythonFormula/sisasm`

Asenna python kirjastot komennoll `uv sync` tai jos uv ei ole asennettuna, niin `pip install . --group dev`

Venv:in aktivointi: `.venv\Scripts\Activate.ps1`

## Testaaminen

`./tests` kansiossa on yksikkotestejä. Nämä ovat samat testiti jotka myös Villestä löytyy. Testit on jaettu v1-v4 sen mukaan missä Villen tehtävässä ne ovat. Yksikkötestit voi suorittaa komennolla `uv run pytest` tai `python -m pytest tests/test_all.py`

## Omat ohjelmat

Samassa kansiossa omia ohjelmia voi suorittaa komennolla `python cli.py <polku ohjelmaasi>`. Testitiedostot käyttävät päätettä .sa mutta mikä tahansa tiedostopääte kelpaa. Jos haluat asentaa sisasm:n omaksi komennoksi, niin `uv tool install .` ja sen jälkeen `sisasm <polku ohjelmaasi>` toimii (komentokehote kannatta käynnistää uudestaan).

## Ohjelman toiminta

Tätä osiota lukiessa olisi hyvä olla koodi auki vieressä.

### Toiminta korkealla tasolla

Pythonilla tulkattu kieli määräytyi tehtävänannon perusteella, oikeastihan tämä kuuluisi kirjoittaa c:llä tai c++:lla ja kääntää oikeaksi assemblyksi.

Harkitsin kahta eri vaihtoehtoa, kun mietin tämän toteutustapaa.

Yksi vaihtoehto oli jakaa tehtävä moneen yksinkertaisempaan vaiheeseen, hyödyntäen paljon luokkia, noudattelemalla enemmän oikeiden ohjelmointikielien kääntäjiä ja tulkkeja. Vaiheet olisivat: lähdekoodi &rarr; tokenit &rarr; käskyt, ja suoritus käskyjen perusteella

Toinen idea, oli kirjoittaa kirjoittaa yksi funktio, joka lukisi yhden rivin, ja sen jälkeen suorittaisi sen. Tämä idea oli ehkä lähempänä sitä, mite tehtävä oli villessä tarkoitettu tehtäväksi.

Valitsin lopulta ensimmäisen vaihtoehdon. Muutamia syitä miksi:

- Komennon suorittaminen suoraan lähdekoodin perusteella kuulosti turhan monimutkaiselta.
- Minulla oli jo kokemusta tästä tavasta, koska kirjoitin yhden pienen compilerin suunnilleen samalla tavalla.
- Tämä muistuttaa enemmän oikeita käänätjiä.
- Tästä kieltä on huomattavsti helpompi kehittää eteenpäin, jos joku joskus haluaa.
- Pääsen osoittamaan taitojani paremmin.

### Toiminta tiedosto kerrallaan:

### `pointer.py`

Tiedosto määrittelee vain yhden luokan `PointerClass` jota kätetään useasti myöhemmin, kun halutaan edetä jotakin listaa yksi elementti kerrallaan. `peek()` palauttaa seuraavan arvon ja `consume()` palauttaa arvon ja etenee yhden eteenpäin.

### `lexer.py`

#### `Lexer(PointerClass[str])`

Luokan tehtävä on muunta lähdekoodi listaksi tokeneja. Hyödyntää `PointerClass` luokkaa.

`tokenize()` funktio tekee kyseisen työn. Se asettaa seuraavan merkin muuttujaan, kunnes sellaista ei enää ole. `while`-looppi jakautuu kolmeen osaan. Jos merkki on jokin yksimerkkinen tokeni, niin lisätään kyseinen tokeni talteen. Jos merkki on kirjain, niin katsotaan seuraavia merkkejä kunnes seuraava ei ole merkki tai numero, ja talletetaan teksti tokeni. Jos merkki taas on numero, tehdään sama numeroille.

#### `Token`

Tokenit ovat yksittäisiä sanoja tai merkkeijä, joiksi lähdekoodi voidaan pilkkoa. Tokenilla on tyyppi (`TokenType`) ja sisältö (`str`).

#### `TokenType(Enum)`

Enum luokka jossa on kaikki eri tyypit, jota `Token` olio voi olla.

### `parser.py`

Ohjelma (`Program`) koostuu käskyistä (`Instruction`). Käsky alkaa avainsanalla jota seuraa expressiot (`Expression`). Avainsana määrittelee mitä alaluokkaa käsky on (esim. `PrintInst` tai `GotoInst`).

`Parser` luokka järjestää tokenit haluttuun muotoon. Päämethodeja on kaksi: `parse_expression()` kun halutaan expressio ja `parse_program()` kun halutaan ohjelma. `parse_program()` käy läpi tokenit ja erottelee eri expression toisistaa. `parse_expression()` saa expression tokenit. Sen sisällä määritely `parse_singelton()` otta yleensä yhden tokenin kerrallaan, ja palautta sen expressiona. Ulompi koodi kutsuu tätä funktiota, hoitaa myös `==` merkin. Tämä rakenne on jäänteitä toteutuksessa jossa sisäkkäiset expressiot, esim monta `==` yhdellä rivillä olivat salittuja, mutta päätin lopulta luopua ideasta.

### `exec.py`

`VarValType` tyyppi kertoo mitä tyyppejä muuttjien (tai expressioiden) arvot voivat olla.

`ExecutionEnvironment` on luokka jolla suoritetaan ohjelmia. `evaluate_expression()` nimensä mukaan evaluoi expression. `execute_instruction()` suorittaa yhden käskyn, joka sille annetaan. `np_exec()` ja `ip_exec()` molemmat suorittavat koko ohjelman, mutta eroavat tulostuksessa. `np_exec()` eli **n**o **p**rint execution palauttaa vain ohjelman tuloseen, eikä tulosta näytölle mitään. Tämä on se, mitä varsinainen tehtävä villessä halusi, ja tätä käytetään myös yksikkötesteissä. `ip_exec()` eli **i**mmidiate **p**rint execution tulostaa ulostulopuskurin (`output_buffer`) joka käskyn suorittamisen jälkeen. Tätä tapaa käytetään kun koodia suoritetaan `cli.py` ohjelmalla tai itse `sisasm` käskyllä.

### Koodin rajoitukset

Villen tehtävässä oli annettu paljon rajoituksia, joiden poistaminen silti läpäisee tehtävän, koska saa olettaa että annettu koodi on aina virheetöntä. Toisin sanoen siis virheistä ei tarvitse valittaa, joten voin antaa enemmän vapauksia. Esimerkiksi muuttujien nimenä sai olla vain a, b, c tai d. Tämä kääntäjä kuitenkin hyväksyy minkä tahansa nimen muuttujalle. Toinen iso ero toteutuksessa on se, että muttujalle voi antaa totuusarvon esimerkiksi `LET a = b==c`, ja tätä voi myöhemmin käyttää JUMP käskyn ehdossa esim `JUMP alku IF a`.

## Tekoälyn käyttö

Tekoälyä on käytetty ainoastaan `pyproject.toml` tiedostossa, jotta asentaminen olisi helpompaa, ja muutamien tässä mainittujen komentojen kirjoittamisessa. Tekoälyltä olen saattanut myös pyytää selityksiä virheisiin. Yhtään koodia tekoäly ei ole kuitenkaan kirjoittanut.
