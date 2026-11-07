# Brustwerk (Zöblitz) CODM Pilot – plan implementacije

> **Za agentne izvršitelje:** OBAVEZNA PODVJEŠTINA: koristiti superpowers:subagent-driven-development (preporučeno) ili superpowers:executing-plans za izvršavanje ovog plana task-po-task. Koraci koriste checkbox (`- [ ]`) sintaksu za praćenje.

**Cilj:** Python alat koji generira Hauptwerkovu Custom Organ Design Module (CODM) definicijsku datoteku (`.CustomOrgan_Hauptwerk_xml`) za samostalnu, jednomanualnu probnu orgulju koja sadrži svih 9 registara budućeg Brustwerka iz glavnog hibridnog projekta (rekonstrukcija Freiberške katedralne orgulje, Silbermann 1714), isključivo iz već instaliranog seta "Stadtkirche Zöblitz standard". Ovo je "probna verzija" iz korisnikovog vlastitog plana (korak 2), koja mora proraditi u Hauptwerku prije širenja na sva 3 manuala + pedal i 44 registra.

**Arhitektura:** Hauptwerkov native ODF format je interno "kompaktiran" (kratke oznake polja poput `<a>`,`<b>`...) i nema pouzdano javno dokumentiranu shemu za to kompaktiranje, pa ručno pisanje native ODF-a nije sigurno. Umjesto toga koristimo Hauptwerkov **Custom Organ Design Module (CODM)**: jednostavniji, potpuno čitljiv XML format (`.CustomOrgan_Hauptwerk_xml`, bez kompaktiranja, pun naziva polja) koji Hauptwerk sam "kompilira" u punu orgulju kad ga korisnik učita preko `Other | Design tools | Load custom organ...`. Python alat čita deklarativni opis divizije/registara/rankova (iz malog modela podataka) i renderira ga u CODM XML tablični format, popunjavajući sva obavezna polja razumnim zadanim vrijednostima i prepisujući samo ono što znamo. Izlazna datoteka ide direktno u Hauptwerkov `CustomOrganDefinitions` folder.

**Tech Stack:** Python 3 (stdlib samo: `dataclasses`, `pathlib`, string-templating za XML — ne `xml.etree`, jer CODM format zahtijeva da prazna polja budu `<Tag></Tag>`, nikad samozatvarajući `<Tag/>`, a etree to ne garantira lako), `unittest` za testove. Bez trećestranih paketa (Homebrew je na ovom Macu nefunkcionalan — vidi memoriju "Homebrew neupotrebljiv na ovom Macu" — ali `python3`/`pip` rade).

**Spec:** Nema odvojenog spec dokumenta; korisnikov izvorni brief (razgovor) + istraživačka saznanja dokumentirana u ovom planu (Global Constraints odjeljak) čine spec. Referentni izvori:
- `/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/ExampleCustomOrgan3-StAnnes-Simplified.CustomOrgan_Hauptwerk_xml` — lokalni, stvarno učitljiv primjer CODM formata (format verzija koju ovaj Hauptwerk stvarno koristi).
- `/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458/` — izvorni sample podaci ("Stadtkirche Zöblitz standard", package ID 000458, supplier PROSPECTUM).

## Global Constraints

- Izlazna datoteka: `/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/BrustwerkZoblitzPilot.CustomOrgan_Hauptwerk_xml`.
- Root tagovi: `<?xml version="1.0" encoding="UTF-8"?>` zatim `<Hauptwerk FileFormat="CustomOrgan" FileFormatVersion="5.00">` — "5.00" je verzija koju doslovno koriste svi primjeri trenutno instaliranog Hauptwerka na ovom računalu (provjereno; priručnik s Hauptwerk.com spominje "6.00" za softver v9.0.1, ali lokalno instalirana verzija koristi 5.00, i to je ono što će stvarno učitati naš file — vjerovati lokalnim datotekama, ne PDF-u).
- Svako opcionalno/nepostojeće polje mora se renderirati kao `<Tag></Tag>`, NIKAD kao `<Tag/>` (potvrđeno u lokalnom primjeru).
- `UniqueOrganID` mora biti u rezerviranom CODM rasponu 800000–899999. Koristiti `800100`.
- `RequiredInstallationPackage` tablica mora sadržavati paket ID `1` (Hauptwerk Standard Components) i paket ID `458` (Name: "Stadtkirche Zöblitz standard", PackageSupplierID `11`, SupplierName "PROSPECTUM", MinimumPackageVersion `2.01` — iz `PackageID000458.InstallationPackageDefinition_Hauptwerk_xml`).
- Svih 9 pilot-registara dolazi iz installation package ID `458`, iz dvije podmape: `samples/ow/...` (Oberwerk u izvornoj Zöblitz orgulji) i `samples/ma/...` (Hauptwerk/glavni manual u izvornoj Zöblitz orgulji). Raspon nota je **036–091** (56 tipki, C–g''', povijesni opseg — potvrđeno brojanjem datoteka na disku za svih 9 rankova), NE moderni opseg C–f''''/c''''. `MIDINoteNumberOfFirstPipe = 36`, `NumberOfPipes = 56` za svaki od 9 rankova.
- Svaka rank-mapa ima dvije varijante snimke, `kurz` i `lang` (njemački: kratko/dugo), svaka u podmapi `haupt`. Provjereno na Gedackt 8' (note 060): `lang` = 12.31s, 8 cue-pointova (glavna attack+loop+release snimka); `kurz` = 5.51s, 1 cue-point (kraća release varijanta za kratko pritisnutu tipku). Zato: `Samples_MainSampleFileFolder` = `.../lang/haupt`, `Samples_ShortNoteReleaseSampleFileFolderIfAny` = `.../kurz/haupt` (nema medium-note varijante u ovom setu — to polje ostaje prazno).
- WAV datoteke već sadrže `smpl` chunk s točnom visinom tona (potvrđeno), tako da se pitch oslanja na automatsku detekciju iz sample-a, a NE na `Samples_RankBasePitch64ftHarmNumIfAssumedTunedToConcertPitch` (ostaje `0`/prazno).
- Mapiranje 9 Brustwerk registara → stvarne mape na disku (iz korisnikove specifikacije i pregleda diska):
  | Registar (Brustwerk) | Izvor (Zöblitz) | Mapa |
  |---|---|---|
  | Gedackt 8' | OW: Gedackt 8' | `samples/ow/01_gedackt8` |
  | Principal 4' | HW: Octava 4' | `samples/ma/04_octava4` |
  | Rohrflöte 4' | OW: Rohrflöte 4' | `samples/ow/02_rohrfloethe4` |
  | Nasat 3' | OW: Nassat 3' | `samples/ow/03_nasat3` |
  | Octava 2' | OW: Octava 2' | `samples/ow/04_octava2` |
  | Tertia 1 3/5' | OW: Tertia 1 3/5' | `samples/ow/05_tertia135` |
  | Quinta 1 1/2' | OW: Quinta 1 1/2' | `samples/ow/06_quinta112` |
  | Sifflöt 1' | OW: Sufflet 1' | `samples/ow/07_sufflet1` |
  | Mixtur 3f | OW: Cimbel II | `samples/ow/08_cimbel2f` |
- `08_cimbel2f` (Cimbel II, dvoredni mikstur) sadrži SAMO jednu pre-miksanu snimku po tipki (ista `lang`/`kurz`/`haupt` struktura kao svi ostali, 56 datoteka) — znači modelira se kao JEDAN `Rank` + JEDAN `StopRank` zapis, ne kao multi-rank. Potvrđeno pregledom foldera, nije potrebno dalje istraživanje.
- `Pitch_RankBaseOutputPitch64ftHarmonicNum` (= 64/stopaža) za registre s "čistom" stopažom su cijeli brojevi: 8'→8, 4'→16, 2'→32, 1-3/5'→40, 1'→64. Za **Nasat 3'** (→21.33) i **Quinta 1 1/2'** (→42.67) vrijednost NIJE cijeli broj — to je otvoreno pitanje, vidi Review Focus i Task 3.
- Nema cross-pitch korekcije (440 Hz/Neidhardt III dio glavnog projekta) u ovom pilotu — pilot koristi isključivo Zöblitzovo izvorno ugađanje, bez mijenjanja. Ta se komplikacija rješava tek u fazi punog hibridnog spoja (izvan opsega ovog plana).
- Nema custom grafičke konzole, nema kuplera, nema tremulanta, nema akcijskih šumova — samo zadani (standard generated) konzolni display, da pilot bude što jednostavniji i brži za provjeru.
- Nijedan automatski test u ovom planu ne pokreće stvarni Hauptwerk (nema alata za upravljanje tom desktop aplikacijom u ovoj sesiji) — završna provjera (Task 4) je ručni korak za korisnika.

## Review Focus

- **Case-sensitivity putanja**: generirani stringovi za `Samples_MainSampleFileFolder`/`Samples_ShortNoteReleaseSampleFileFolderIfAny` moraju TOČNO (byte-za-byte, uključujući velika/mala slova) odgovarati stvarnim nazivima mapa na disku — macOS je case-insensitive pa bi pogrešan case ovdje tiho prošao lokalno, ali bi organ prestao raditi na Windowsu/Linuxu ili pri distribuciji. Test u Tasku 2/3 uspoređuje generirani put s `pathlib` listingom stvarnog direktorija.
- **Samozatvarajući tagovi**: ako serializator ikad izbaci `<Tag/>` za prazno polje umjesto `<Tag></Tag>`, Hauptwerk može odbiti učitati datoteku. Test u Tasku 2 provjerava da izlazni XML string ne sadrži nijedan `/>` obrazac.
- **Neusklađen broj pipeova i stvarnih datoteka**: ako se `NumberOfPipes`/`MIDINoteNumberOfFirstPipe` ne poklapa sa stvarnim brojem/rasponom `.wav` datoteka u `lang/haupt` mapi, Hauptwerk će tiho izostaviti pipeove ili pucati pri učitavanju. Task 3 eksplicitno broji datoteke na disku za svih 9 rankova i uspoređuje s hardkodiranim vrijednostima prije pisanja.
- **Jedinstvenost ID-eva**: `RankID` i `StopCode` moraju biti jedinstveni unutar datoteke, a `UniqueOrganID` u rasponu 800000–899999. Test u Tasku 3 provjerava da nema duplikata i da je organID u rasponu.
- **Escapiranje posebnih znakova u nazivima**: nazivi registara sadrže apostrofe (oznaka stope, npr. `Sifflöt 1'`) i njemačke umlaute (`ö`). Test u Tasku 2 provjerava da se `&`, `<`, `>`, `"` escapiraju po XML pravilima, a UTF-8 znakovi (`ö`) ostaju netaknuti i čitljivi.

---

### Task 1: Model podataka za Rank/Stop/StopRank/Division

**Files:**
- Create: `src/codm/model.py`
- Test: `tests/test_model.py`

**Interfaces:**
- Produces: `Rank` dataclass (`rank_id: int`, `name: str`, `num_pipes: int`, `first_midi_note: int`, `package_id: int`, `main_folder: str`, `short_release_folder: str | None`, `pitch_harmonic_num: float`), `Stop` dataclass (`stop_code: int`, `name: str`, `display_name: str`), `StopRank` dataclass (`stop_code: int`, `rank_id: int`, `first_mapped_key: int`, `num_mapped_keys: int`), `Division` dataclass (`division_code: int`, `name: str`, `short_name: str`, `number_of_keys: int`, `first_key_midi_note: int`).

- [ ] **Step 1: Napiši padajući test koji konstruira `Rank`, `Stop`, `StopRank` i `Division` s poznatim vrijednostima i provjerava da su polja dostupna i ispravnog tipa**

```python
def test_rank_holds_expected_fields():
    r = Rank(rank_id=1, name="Gedackt 8'", num_pipes=56, first_midi_note=36,
              package_id=458, main_folder="samples/ow/01_gedackt8/lang/haupt",
              short_release_folder="samples/ow/01_gedackt8/kurz/haupt",
              pitch_harmonic_num=8)
    assert r.rank_id == 1 and r.num_pipes == 56 and r.pitch_harmonic_num == 8
```

- [ ] **Step 2: Pokreni test, provjeri da pada ("Rank not defined")**

Run: `python3 -m unittest tests.test_model -v`
Expected: FAIL s `NameError` ili `ImportError`

- [ ] **Step 3: Implementiraj `Rank`, `Stop`, `StopRank`, `Division` kao `@dataclass` u `src/codm/model.py`, točno s poljima iz Interfaces bloka**

- [ ] **Step 4: Pokreni test, provjeri da prolazi**

Run: `python3 -m unittest tests.test_model -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/codm/model.py tests/test_model.py
git commit -m "feat: add CODM data model (Rank, Stop, StopRank, Division)"
```

---

### Task 2: CODM XML serializator

**Files:**
- Create: `src/codm/writer.py`
- Test: `tests/test_writer.py`

**Interfaces:**
- Consumes: `Rank`, `Stop`, `StopRank`, `Division` iz `src/codm/model.py` (Task 1).
- Produces: `render_custom_organ(organ_id: int, name: str, divisions: list[Division], stops: list[Stop], ranks: list[Rank], stopranks: list[StopRank], required_packages: list[tuple[int,str,int,str,str]]) -> str` — vraća kompletan XML string spreman za pisanje u datoteku.

- [ ] **Step 1: Napiši padajući test koji renderira jedan minimalni `Rank` zapis i provjerava ključne invarijante**

```python
def test_render_rank_has_no_self_closing_tags_and_escapes_apostrophe():
    rank = Rank(rank_id=1, name="Sifflöt 1'", num_pipes=56, first_midi_note=36,
                package_id=458, main_folder="samples/ow/07_sufflet1/lang/haupt",
                short_release_folder="samples/ow/07_sufflet1/kurz/haupt",
                pitch_harmonic_num=64)
    xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                ranks=[rank], stopranks=[], required_packages=[])
    assert "/>" not in xml
    assert "Sifflöt 1&apos;" in xml or "Sifflöt 1'" in xml  # provjeri stvarno pravilo escapiranja iz guidea (apostrof se NE escapira po CODM guideu - samo & < > ")
    assert "<Samples_ShortNoteReleaseSampleFileFolderIfAny>samples/ow/07_sufflet1/kurz/haupt</Samples_ShortNoteReleaseSampleFileFolderIfAny>" in xml
```

- [ ] **Step 2: Pokreni test, provjeri da pada**

Run: `python3 -m unittest tests.test_writer -v`
Expected: FAIL s `NameError`/`ImportError`

- [ ] **Step 3: Implementiraj `render_custom_organ(...)` u `src/codm/writer.py`**

Koristi string-templating (ne `xml.etree`) kako bi se zagarantiralo `<Tag></Tag>` za prazne vrijednosti. Za escapiranje koristiti `xml.sax.saxutils.escape` (escapira samo `&`, `<`, `>`; `"` ručno ako se koristi u atributima — ovdje nema XML atributa s korisničkim sadržajem, samo tekst elemenata, pa je `escape()` dovoljan). Root: `<?xml version="1.0" encoding="UTF-8"?>\n<Hauptwerk FileFormat="CustomOrgan" FileFormatVersion="5.00">`, zatim `ObjectList` blokovi za `_general`, `requiredinstallationpackage`, `division`, `rank`, `stop`, `stoprank` (prazni `coupler`, `tremulant`, `enclosure`, `externalrank`, `shortcutpiston`, `customdisplay*` blokovi i u minimalnom slučaju). Za `_general` i `division` koristiti puni set `CustomDisplay*` polja praznih (vidi lokalni primjer `ExampleCustomOrgan3-StAnnes-Simplified...xml` redovi 3-80 i 502-650 za točan popis i redoslijed).

- [ ] **Step 4: Pokreni test, provjeri da prolazi**

Run: `python3 -m unittest tests.test_writer -v`
Expected: PASS

- [ ] **Step 5: Napiši i prođi dodatni test za case-sensitivity (Review Focus #1): generirani `main_folder`/`short_release_folder` string mora se točno (case-sensitive) poklapati s nazivom stvarne mape dobivenim preko `pathlib.Path(...).resolve()` listinga na `/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458/samples/ow/07_sufflet1/lang/haupt`**

- [ ] **Step 6: Commit**

```bash
git add src/codm/writer.py tests/test_writer.py
git commit -m "feat: add CODM XML serializer with empty-tag and escaping guarantees"
```

---

### Task 3: Brustwerk pilot definicija i generiranje datoteke

**Files:**
- Create: `src/codm/brustwerk_pilot.py`
- Test: `tests/test_brustwerk_pilot.py`

**Interfaces:**
- Consumes: `render_custom_organ(...)` iz Task 2, `Rank`/`Stop`/`StopRank`/`Division` iz Task 1.
- Produces: `build_brustwerk_pilot(zoblitz_root: Path) -> str` — vraća kompletan XML string za svih 9 registara; `main()` koji poziva `build_brustwerk_pilot` s putanjom `/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458` i piše rezultat u `/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/BrustwerkZoblitzPilot.CustomOrgan_Hauptwerk_xml`.

- [ ] **Step 1: Prije pisanja koda, ručno/skriptom potvrdi stvarni broj `.wav` datoteka u `lang/haupt` za svih 9 mapa iz tablice u Global Constraints i zapiši ih (očekivano 56 za svih 9, prema ranijoj provjeri — ovo je provjera regresije ako se podaci na disku promijene)**

Run: `for d in <9 mapa>/lang/haupt; do echo "$d: $(ls "$d" | wc -l)"; done`
Expected: svih 9 redaka ispisuje `56`

- [ ] **Step 2: Napiši padajući test koji provjerava da `build_brustwerk_pilot` vraća XML sa svih 9 `<StopCode>` vrijednosti i jedinstvenim `RankID`/`StopCode` (Review Focus #4)**

```python
def test_build_brustwerk_pilot_has_nine_unique_stops():
    xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
    stop_codes = re.findall(r"<StopCode>(\d+)</StopCode>", xml)
    assert len(stop_codes) >= 9
    assert len(set(stop_codes)) == len(stop_codes)
    organ_id = re.search(r"<UniqueOrganID>(\d+)</UniqueOrganID>", xml).group(1)
    assert 800000 <= int(organ_id) <= 899999
```

- [ ] **Step 3: Pokreni test, provjeri da pada**

Run: `python3 -m unittest tests.test_brustwerk_pilot -v`
Expected: FAIL

- [ ] **Step 4: Implementiraj `build_brustwerk_pilot(zoblitz_root)` koristeći tablicu mapiranja iz Global Constraints — za Nasat 3' i Quinta 1 1/2' koristi `pitch_harmonic_num` zaokružen na najbliži cijeli broj (21 i 43) kao privremenu vrijednost UZ komentar da ovo treba potvrditi u Hauptwerkovoj ugrađenoj CODM format dokumentaciji (`Other | Design tools | View Custom Organ Design Module … format documentation`) prije finalnog slanja korisniku — ja (Claude) nemam alat za upravljanje Hauptwerk desktop aplikacijom, pa ovo korisnik mora sam otvoriti i potvrditi**

- [ ] **Step 5: Pokreni test, provjeri da prolazi**

Run: `python3 -m unittest tests.test_brustwerk_pilot -v`
Expected: PASS

- [ ] **Step 6: Pokreni `main()` i provjeri da je datoteka stvarno napisana na ciljnu putanju**

Run: `python3 -m src.codm.brustwerk_pilot`
Expected: datoteka `/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/BrustwerkZoblitzPilot.CustomOrgan_Hauptwerk_xml` postoji i sadrži `<UniqueOrganID>800100</UniqueOrganID>`

- [ ] **Step 7: Commit**

```bash
git add src/codm/brustwerk_pilot.py tests/test_brustwerk_pilot.py
git commit -m "feat: generate Brustwerk Zoblitz pilot custom organ definition"
```

---

### Task 4: Ručna provjera u Hauptwerku (korisnik)

Ovaj task NEMA automatske testove — zahtijeva da korisnik otvori Hauptwerk GUI, jer ova sesija nema alat za upravljanje macOS desktop aplikacijama.

- [ ] **Step 1 (korisnik): Otvoriti Hauptwerk i provjeriti `Settings | General: Preferences` da "Simplify | Disable design tools…" NIJE uključeno**

- [ ] **Step 2 (korisnik): `Other | Design tools | Load custom organ...` → odabrati `BrustwerkZoblitzPilot` → OK na svim zadanim postavkama**

Expected: orgulja se učitava bez greške; ako se javi greška o neispravnom XML-u ili nedostupnom paketu, zapisati točan tekst greške i vratiti se na Task 2/3 radi ispravke.

- [ ] **Step 3 (korisnik): Provjeriti da se svih 9 registara prikazuje i da svaki od njih svira po cijelom opsegu 36–91 (C–g''') bez pucanja/tišine**

- [ ] **Step 4 (korisnik, ako Step 2 javi grešku o `Pitch_RankBaseOutputPitch64ftHarmonicNum`): Otvoriti `Other | Design tools | View Custom Organ Design Module … format documentation` i potvrditi dopušta li to polje necijele brojeve; javiti rezultat natrag da se Task 3 Step 4 po potrebi ispravi**

- [ ] **Step 5: Ako sve radi, commit potvrde (napomena, ne kod)**

```bash
git add -A
git commit -m "docs: confirm Brustwerk Zoblitz pilot loads and plays correctly in Hauptwerk"
```
