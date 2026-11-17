# SiSAsm

Sanoista **Si**mple **S**low **As**se**m**bly.

## Asentaminen

Lataa repo itsellesi komennolla `git clone https://github.com/PythonFormula/sisasm`

Asenna python kirjastot komennoll `uv sync` tai jos uv ei ole asennettuna, niin `pip install . --group dev`

Venv:in aktivointi: `.venv\Scripts\Activate.ps1`

## Testaaminen

Suorita yksikkötestit komennolla `uv run pytest` tai `python -m pytest tests/test_all.py`

## Omat ohjelmat

Samassa kansiossa omia ohjelmia voi suorittaa komennolla `python cli.py <polku ohjelmaasi>`. Testitiedostot käyttävät päätettä .sa mutta mikä tahansa tiedostopääte kelpaa. Jos haluat asentaa sisasm:n omaksi komennoksi, niin `uv tool install .` ja sen jälkeen `sisasm <polku ohjelmaasi>` toimii (komentokehote kannatta käynnistää uudestaan).

## Tekoälyn käyttö

Tekoälyä on käytetty ainoastaan `pyproject.toml` tiedostossa, jotta asentaminen olisi helpompaa, ja muutamien tässä mainittujen komentojen kirjoittamisessa. Tekoälyltä olen saattanut myös pyytää selityksiä virheisiin. Yhtään koodia tekoäly ei ole kuitenkaan kirjoittanut.
