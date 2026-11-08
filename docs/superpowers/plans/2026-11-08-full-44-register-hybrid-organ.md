# Freiberg Hibridna Orgulja — Plan implementacije (sva 4 odjeljka, 44 registra)

> **Za agentne izvršitelje:** OBAVEZNA PODVJEŠTINA: koristiti superpowers:subagent-driven-development (preporučeno) ili superpowers:executing-plans za izvršavanje ovog plana task-po-task. Koraci koriste checkbox (`- [ ]`) sintaksu za praćenje.

**Cilj:** Proširiti i iskoristiti CODM alat izgrađen u Brustwerk-pilot planu da generira kompletnu, svirivu hibridnu orgulju sa svim 44 registra (Hauptwerk, Oberwerk, Brustwerk, Pedal), spojenu u jednu `.CustomOrgan_Hauptwerk_xml` datoteku s kuplerima i tremulantima, prema korisnikovoj izvornoj specifikaciji (rekonstrukcija Freiberške katedralne orgulje, G. Silbermann 1714).

**Arhitektura:** Brustwerk-pilot je već dokazao da je CODM (ne native kompaktirani ODF) pravi put, i da `src/codm/model.py` (Rank/Stop/StopRank/Division) + `src/codm/writer.py` (XML serializator) rade pouzdano (14/14 testova, recenziran i popravljen). Ovaj plan:
1. Proširuje `Rank` model s poljima za korekciju ugađanja (potrebno za izvore koji nisu na 440 Hz/Neidhardt III).
2. Dodaje tri nova division-modula (Hauptwerk, Oberwerk, Pedal), svaki po uzoru na `src/codm/brustwerk_pilot.py`, ali svaki sa svojom specifičnom konvencijom imenovanja mapa (svaki dobavljač snima/organizira sample-ove drugačije — to je potvrđeno istraživanjem, ne pretpostavka).
3. Spaja svih 9+13+13+9=44 registra u JEDNU konačnu `.CustomOrgan_Hauptwerk_xml` datoteku s kuplerima i tremulantima.
4. Primjenjuje cross-pitch korekciju za izvore koji nisu na Görlitzovih 440 Hz (Waltershausen 466,8 Hz → korekcija po registru).

**Tech Stack:** Isti kao pilot — Python 3 stdlib, `unittest`, postojeći `src/codm/model.py`/`writer.py`.

**Spec:** Korisnikov izvorni brief (razgovor) + [2026-11-07-brustwerk-zoblitz-codm-pilot.md](2026-11-07-brustwerk-zoblitz-codm-pilot.md) (dokazana arhitektura) + istraživačka saznanja ispod (Global Constraints), prikupljena izravnim pregledom diska, ZIP arhiva, `smpl` chunkova i Hauptwerkovih vlastitih primjera u ovoj sesiji.

## Global Constraints

### Opće
- Svih 9 Brustwerk registara već postoji i radi (`src/codm/brustwerk_pilot.py`, grana `brustwerk-zoblitz-codm-pilot`, commit `37ba183`). Ovaj plan ga NE dira, samo ga spaja s ostalima u Tasku 5.
- `UniqueOrganID` za KONAČNU spojenu orgulju mora biti NOV broj u rasponu 800000–899999, različit od pilota (800100). Koristiti `800200`.
- DivisionCode raspon je fiksan Hauptwerkov identitet (potvrđeno u pilotu): `1=PEDAL, 2=GREAT`. Za preostale divizije u ovom projektu: `3=SWELL, 4=CHOIR` su slobodni (prema primjerima). Mapiranje:
  - **Hauptwerk → DivisionCode 2** (GREAT) — glavni manual.
  - **Oberwerk → DivisionCode 3** (SWELL) — drugi manual.
  - **Brustwerk → DivisionCode 4** (CHOIR) — treći manual (već izgrađen kao DivisionCode 2 u pilotu jer je tada bio JEDINI manual! **Pri spajanju u Tasku 5 treba promijeniti Brustwerkov DivisionCode s 2 na 4** i sve njegove StopCode vrijednosti s raspona 21xx na raspon 24xx, inače će se sudariti s Hauptwerkovim StopCode-ovima.)
  - **Pedal → DivisionCode 1** (PEDAL) — već korišten ispravno u nativnom smislu.
  - StopCode raspon po diviziji: `2000 + (DivisionCode-1)*100 + index` (potvrđeno u pilotu). Pedal: 2000-2099, Hauptwerk: 2100-2199, Oberwerk: 2200-2299, Brustwerk: 2300-2399 (NE 2100 kao u pilotu).
- Opseg tipki (keyboard compass) — **OTVORENO PITANJE iz korisnikove specifikacije, sada s konkretnim podacima**: Görlitz (izvorni proizvođač specifikacije) ima manuale C-a''' (58 tipki, MIDI 36-93) i pedal C-f' [-g' extended] (prošireno u Hauptwerku). Zöblitz (Brustwerk, već izgrađen) ima 56 tipki C-g''' (MIDI 36-91). Wasselonne-ovi registri (Echo/Vox humana za Oberwerk) nisu provjereni za opseg u ovom planu — provjeriti u Tasku 3.
  - **Moja odluka (potvrdite ili promijenite)**: master opseg manuala za CIJELU orgulju = **Görlitzov izvorni opseg, 58 tipki, MIDI 36-93 (C-a''')**, jer Görlitz opskrbljuje većinu registara u 2 od 3 manuala. Brustwerk (Zöblitz, 56 tipki) i svi Wasselonne-registri imaju **2 tipke manje na vrhu (g'''-a''')** — za te registre `NumberOfPipes` ostaje njihov stvarni broj (56), a `Division.number_of_keys` za Brustwerk ostaje 56 (Brustwerk kao divizija ima SVOJ manji opseg od 56 tipki, odvojeno od Hauptwerka/Oberwerka koji imaju 58) — CODM to dopušta (`NumberOfKeys` je po-divizijski parametar). Cijena ako je ovo pogrešna odluka: gornje 2 tipke Brustwerka jednostavno nisu dostupne; lako se promijeni u Tasku 5 prije finalnog spajanja ako korisnik odluči drugačije.
- Hauptwerkova instalacija na ovom računalu vjerojatno NEMA registrirane pakete za Görlitz/Wasselonne/Waltershausen (potvrđeno za Zöblitz u pilotu — isti problem će postojati i za ove). To je PRECONDITION za bilo kakvo stvarno učitavanje u Hauptwerk, ne nešto što kod rješava.

### Hauptwerk divizija (13 registara) — izvori i mape

Svi "Görlitz" izvori dolaze iz `/Volumes/Samsung T7/Orgulje/Sonus paradisi Goerlitz Sonnenorgel/Sonus paradisi Goerlitz Sonnenorgel Hauptwerk (Part N).zip` — **ZIP arhive, NE raspakirane!** Prvi korak Taska 2 je selektivno raspakiravanje (ne cijeli ZIP — svaki je ~11-21GB) SAMO potrebnih mapa, koristeći `zipfile.ZipFile.extract()` po točnoj putanji.

Görlitzova stvarna orgulja: Casparini 1703 / **Mathis 1997-2006** (moderna orgulja u baroknom stilu, NE povijesna — potvrđeno iz `html/index.html` unutar paketa 1811). To je u skladu s ulogom "glavni izvor, 440 Hz" iz izvorne specifikacije.

Kanali: Görlitz nudi 3 para kanala po registru — `01-AB` (front-direct, blizu piska), `02-Re` (rear/stražnji), `03-LR` (front-diffuse, daleko) za manuale; pedal koristi `01-AB`/`02-Re`/`04-LRint` (ista logika, drugačiji brojevi). **Moja odluka**: koristiti `01-AB` kao `front-direct` (zahtjev iz izvorne specifikacije) za SVE Görlitz registre u ovom projektu — potvrđeno iz `specification.htm`: "the front-direct ranks... direct (near to the pipes)". Nisam 100% siguran koji je slovni kod točno "direct" vs "diffuse" (dokumentacija ne kaže eksplicitno koji je AB a koji LR) — ako nakon slušanja zvuči preudaljeno, zamijeniti `01-AB` s `03-LR`.

Release-mapa konvencija (Görlitz, RAZLIČITA od Zöblitza!): svaki rank ima glavnu mapu (npr. `01-AB_grossoct8/`) s `NNN-Note.wav` datotekama (attack+loop+primary release), PLUS podmape `rel00200/` i `rel00440/` s dodatnim release-only datotekama za note kraće od 200ms / 440ms. Ovo se mapira izravno na CODM-ova polja:
- `Samples_MainSampleFileFolder` = glavna mapa (npr. `.../01-AB_grossoct8`)
- `Samples_ShortNoteReleaseSampleFileFolderIfAny` = `.../01-AB_grossoct8/rel00200`, `..._MaxNoteTimeMsForShortNoteReleaseSamplesIfAny` = 200
- `Samples_MediumNoteReleaseSampleFileFolderIfAny` = `.../01-AB_grossoct8/rel00440`, `..._MaxNoteTimeMsForMediumNoteReleaseSamplesIfAny` = 440

Neki fajlovi imaju `_bis` sufiks (npr. `040-E_bis.wav`) — alternativna/dodatna snimka iste note. **Otvoreno pitanje za Task 2**: provjeriti igraju li `_bis` datoteke ikakvu posebnu ulogu u CODM-u ili ih jednostavno treba ignorirati (ne referencirati) pri brojanju/validaciji po note-raspon. Ne postoje u priručniku CODM-a spomenuti kao posebni; najvjerojatnije se sigurno ignoriraju jer `_validate_rank_folder` (iz pilota) treba filtrirati `*-*.wav` po točnom uzorku `NNN-*.wav` bez `_bis`, ne gledati broj datoteka total.

Potvrđeno (ImageSet rudarenje iz kompaktiranog `Goerlitz Sonnenorgel Surround, full edition.Organ_Hauptwerk_xml`, usporedbom s `specification.htm`) — mapiranje registar → stvarna Görlitz mapa → paket:

| Registar (Hauptwerk) | Görlitz naziv | Mapa (pod `OrganInstallationPackages/<pkg>/pipes/<div>/`) | Paket (ZIP Part) |
|---|---|---|---|
| Principal 8' | Gross-Octava 8' | `HW/01-AB_grossoct8` | 1811 (Part 1) |
| Viol di Gamba 8' | Viol di Gamba 8' | `HW/01-AB_violdigam8` | 1812 (Part 2) |
| Rohrflöte 8' | Rohr-Flöt 8' | `HW/01-AB_rohrflot8` | 1813 (Part 3) |
| Octava 4' | Octava 4' | `HW/01-AB_octav4` | 1811 (Part 1) |
| Quinta 3' | Quinta 3' | `HW/01-AB_quinta3` | 1812 (Part 2) |
| Super-Octava 2' | Super-Octava 2' | `HW/01-AB_superoct2` | 1812 (Part 2) |
| Tertia 1 3/5' | Tertia (BW!) | `BW/01-AB_tercia` | 1812 (Part 2) — **napomena: BW mapa, ne HW** |
| Mixtur 4f | Mixtur IV | `HW/01-AB_mix4x` | 1812 (Part 2) |
| Cimbeln 3f | Cymbel III | `HW/01-AB_cimbal` | 1812 (Part 2) |
| Cornet 5f | Cornet V | `HW/01-AB_cornet` | 1813 (Part 3) |
| Trompet 8' | Trompet 8' | `HW/01-AB_trompet8` | 1811 (Part 1) |
| Clarin 4' | Clarin 4' | `HW/01-AB_clarin4` | 1813 (Part 3) |
| Bordun 16' | Trost: Portun-Untersatz 16' | `HW-PortunUntersatz16` (glavna) + `HW-PortunUntersatz16-R1`/`-R2` (releases, paket 256) | Waltershausen pkg **255** (glavna) + **256** (releases/trem) — **ODVOJENI izvor, 466,8 Hz, treba pitch-korekciju (Task 6)** |

Sve Görlitz HW/BW mape u gornjoj tablici provjereno sadrže `NNN-C.wav` imenovanje; note raspon nije još brojčano potvrđen za svaki rank (Task 2 mora to učiniti, isti postupak kao pilot).

Pakete `1811`, `1812`, `1813` treba registrirati u `RequiredInstallationPackage` tablici — metapodaci (`Name`, `PackageSupplierID`, `SupplierName`, `MinimumPackageVersion`) čitaju se iz `packageidNNNNNN.InstallationPackageDefinition_Hauptwerk_xml` unutar odgovarajućeg ZIP-a (isti postupak kao za Zöblitz paket 458 u pilotu).

### Oberwerk divizija (13 registara) — izvori i mape

| Registar (Oberwerk) | Izvor naziv | Mapa | Paket |
|---|---|---|---|
| Quintaden 16' | Görlitz OW: Quintadena 16' | `OW/01-AB_quintd16` | 1813 |
| Principal 8' | Görlitz OW: Principal 8' | `OW/01-AB_Principal8` | 1812 |
| Gedackt 8' | Görlitz OW: Grob-Gedackt 8' | `OW/01-AB_Gedackt8` | 1812 |
| Quintaden 8' | Görlitz OW: Quintadena 8' | `OW/01-AB_Quintadena8` | 1812 |
| Octava 4' | Görlitz OW: Octava 4' | `OW/01-AB_Octava4` | 1812 |
| Spitzflöte 4' | Görlitz HW: Spitz-Flöt 4' (cross-divizijsko posuđivanje!) | `HW/01-AB_spitzflt4` | 1812 |
| Super-Oktava 2' | Görlitz OW: Sedecima 2' | `OW/01-AB_sedecima2` | 1812 |
| Flaschlöt 1' | Görlitz BW: Super-Sedecima 1' | `BW/01-AB_supersed1` | 1813 |
| Mixtur 3f | Görlitz BW: Scharff-Mixtur III | `BW/01-AB_scharfmix3` | 1813 |
| Cimbeln 2f | Görlitz OW: Scharff-Cymbel III | `OW/01-AB_scharfcimbel` | 1812 |
| Echo 5f | Wasselonne: EchoCornet (J.A.Silbermann echo-cornet) | `EchoCornet` (short/medium/long) | Wasselonne pkg 802 |
| Krumbhorn 8' | Görlitz OW: Krumb-Horn 8' | `OW/01-AB_krumhorn8` | 1812 |
| Vox humana 8' | Wasselonne: GoVoixHumaine8 (Voix humaine) | `GoVoixHumaine8` (short/medium/long) | Wasselonne pkg 802 |

Rezerve (ne koristiti osim ako primarni izvor zapne): Echo 5f rezerva = `Görlitz OW/01-AB_cornetti` (pkg 1813); Vox humana 8' rezerva = Waltershausen (treba locirati folder, nije dio ovog taska dok primarni Wasselonne izvor ne zatreba zamjenu).

Wasselonne release-konvencija: `short`/`medium`/`long` podmape (POTVRĐENO ranije u ovoj sesiji za `EchoCornet` i `GoVoixHumaine8`) — treća, drugačija konvencija od Zöblitza (kurz/lang) i Görlitza (glavna+relXXXXX). **Treba odrediti koja od 3 (short/medium/long) odgovara CODM-ovom `Samples_MainSampleFileFolder` (najduža, s loop-om) vs `..._ShortNoteReleaseSampleFileFolderIfAny` vs `..._MediumNoteReleaseSampleFileFolderIfAny`** — pretpostavka: `long`=glavna, `medium`=medium-release, `short`=short-release (analogno nazivima), ali to treba potvrditi mjerenjem trajanja/cue-pointova kao što je učinjeno za Zöblitzov kurz/lang u pilotu (Task 3, Step 1).

Wasselonne paket 802 ima prazan `CustomOrganRank`, kao i Zöblitz — nije prepreka, isti CODM pristup radi bez tog tablice (potvrđeno u pilotu).

### Pedal divizija (9 registara) — izvori i mape

| Registar (Pedal) | Görlitz naziv | Mapa | Paket |
|---|---|---|---|
| Untersatz 32'+16' | Gross Principal-Bass 32' **+** Contra-Bass 16' (DVA rank-a, JEDAN stop!) | `Pedal/01-AB_principalbas32` (1813) **+** `Pedal/01-AB_Contrabass16` (1814) | 1813 + 1814 |
| Principalbaß 16' | Principal-Bass 16' | `Pedal/01-AB_principalbas16` | 1812 |
| Subbaß 16' | Sub-Bass 16' | `Pedal/01-AB_Subbass16` | **1811** (ne 1812/1813!) |
| Octavbaß 8' | Octav-Bass 8' | `Pedal/01-AB_octavbas8` | 1812 |
| Octavbaß 4' | Super-Octav-Bass 4' | `Pedal/01-AB_Superoctbas4` | 1812 |
| Pedalmixtur 6f | Mixtur VI | `Pedal/01-AB_mix6` | 1813 |
| Posaunenbaß 16' | Posaunen 16' | `Pedal/01-AB_posaun16` | 1813 |
| Trompetenbaß 8' | Trompeten-Bass 8' | `Pedal/01-AB_TrompBass8` | 1812 |
| Clarinbaß 4' | Clarinen-Bass 4' | `Pedal/01-AB_ClarinBass4` | 1813 |

Paket 1814 sadrži i jednu nevezanu, modernu "SW" (Schwellwerk) diviziju (Salicional, Viola Pomposa, Vox Coelestis, Clarinette, Harmonia Aetheria...) koja se **u potpunosti ignorira** — dio je Görlitzove 2006. dogradnje, nije dio ovog hibridnog projekta, osim njenog Pedal-sadržaja (Contrabass16, koji JE potreban, gore).

Pedal opseg: Görlitzov izvorni `C-f' [-g' extended]`. **Moja odluka**: koristiti Hauptwerkovu standardnu pedal konvenciju iz pilota/primjerâ (`MIDINoteNumOfFirstKey=36`, `NumberOfKeys=30`), budući da to već odgovara "C-f' extended" opisu (30 tonova od C2).

`Untersatz 32'+16'` kao JEDAN Stop s DVA Rank-a: implementacijski, jedan `Stop` zapis + DVA `StopRank` zapisa (oba referenciraju isti `StopCode`, različite `RankID`) — izravno podržano CODM-ovom many-to-many Stop↔Rank relacijom (potvrđeno u CODM priručniku, "many-to-many relationship between stops and ranks").

### Zajednička infrastruktura — proširenje modela

CODM `Rank` tablica već ima polja `Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones` i `..._PipeMIDINoteNum096_...` (writer.py ih već renderira, trenutno hardkodirano na `0`). Potrebno je dodati 2 nova polja u `Rank` dataclass (`tuning_adjust_semitones_036: float = 0`, `tuning_adjust_semitones_096: float = 0`, s default vrijednošću 0 da postojeći pilot-kod i njegovi testovi ne puknu), i writer.py mora čitati iz njih umjesto hardkodirane nule.

### Coupler/Tremulant tablice (za Task 5)

`Coupler` tablica (potvrđeno polje-po-polje iz lokalnog `ExampleCustomOrgan1`): `CouplerCode, Name, CustomDisplay1_* (10 polja), CustomDisplay2_* (10 polja), DisplayName, DefaultToEngaged, SwitchIsLatching, StoreInDivisionalCombinations, StoreInGeneralCombinations, AccessibleForMIDIInputAndOutput, PercussiveEngagingSoundEffect_RankID, ..._MIDINoteNumber, PercussiveDisengagingSoundEffect_RankID, ..._MIDINoteNumber, SustainingSoundEffect_RankID, ..._MIDINoteNumber, OverrideSourceDivisionToSpecifiedDivisionCode, OverrideDestDivisionToSpecifiedDivisionCode, CoupleDestinationKeyboardRatherThanKeyAction, CouplerCodeFromWhichToCopyState, CustomCoupler_MIDINoteNumIncrementFromSourceToDest, CustomCoupler_KeyActionTypeCode, CustomCoupler_KeyActionEffectCode, CustomCoupler_PipeMIDINoteNum036_PizzOrReitPeriodMs, CustomCoupler_PipeMIDINoteNum096_PizzOrReitPeriodMs` (36 polja ukupno).

`Tremulant` tablica (potvrđeno iz `ExampleCustomOrgan2`): `TremulantCode, Name, CustomDisplay1_* (10), CustomDisplay2_* (10), DisplayName, DefaultToEngaged, SwitchIsLatching, StoreInDivisionalCombinations, StoreInGeneralCombinations, AccessibleForMIDIInputAndOutput, PercussiveEngagingSoundEffect_RankID, ..._MIDINoteNumber, PercussiveDisengagingSoundEffect_RankID, ..._MIDINoteNumber, SustainingSoundEffect_RankID, ..._MIDINoteNumber, TremulantCodeFromWhichToCopyState, FrequencyHz, MaxFrequencyRandomisationPct, MaxDepthRandomisationPct` (29 polja ukupno). Standard default: `FrequencyHz=5.2, MaxFrequencyRandomisationPct=15, MaxDepthRandomisationPct=15` (iz primjera).

**Moja odluka za kuplere/tremulante (nije bilo u izvornoj specifikaciji — korisnik treba potvrditi ili promijeniti)**: standardni set po uzoru na Görlitzovu vlastitu orgulju (koja ima `II/I, III/I, III/II, I-P, II-P, III-P` za ekvivalentan 3-manual+pedal raspored):
- Kupleri: Oberwerk/Hauptwerk (II/I), Brustwerk/Hauptwerk (III/I), Brustwerk/Oberwerk (III/II), Hauptwerk/Pedal (I-P), Oberwerk/Pedal (II-P), Brustwerk/Pedal (III-P) — 6 kuplera, svi "normal" (unisono) kuplovanje, sve `CouplerCode` u 1xxx rasponu po pravoj konvenciji (treba utvrditi exact coupler-code shemu iz primjera — nije dosad istražena, dio Taska 5).
- Tremulanti: jedan po manualu (Hauptwerk, Oberwerk, Brustwerk) = 3 tremulanta, bez tremulanta na Pedalu (standardna barokna praksa). Primjenjuju se na SVE rankove te divizije postavljanjem `Trem_TremulantCode` na odgovarajući rank.
- Cijena ako ovo nije ono što korisnik želi: lako se promijeni u Tasku 5 (samo podaci, ne arhitektura).

## Review Focus

- **Pogrešna visina tona za necjelobrojne/mutacijske registre** (ponovljena C1-greška iz pilota): svaki novi rank MORA imati harmonijski broj potvrđen mjerenjem `smpl` chunka (omjer prema referentnom 8' registru), NE izračunat kao `64/stopaža`. Test u svakom division-tasku mora provjeriti ove vrijednosti, po uzoru na `test_pitch_harmonic_numbers_match_measured_sample_pitch_ratios`.
- **DivisionCode/StopCode sudar pri spajanju** (ponovljena C2/C3-greška): Brustwerkov DivisionCode mora se promijeniti s 2 na 4 (i StopCode-ovi s 21xx na 24xx) PRIJE spajanja u Tasku 5 — ako se to zaboravi, Brustwerk i Hauptwerk će se oba pokušati vezati na GREAT diviziju. Test u Tasku 5 mora provjeriti da su sva 4 DivisionCode-a (1,2,3,4) jedinstvena i da nijedan StopCode raspon ne preklapa drugi.
- **`_bis` datoteke i `relXXXXX` podmape krivo ubrojene u broj pipeova**: `_validate_rank_folder` (iz pilota) trenutno broji SVE `*.wav` u glavnoj mapi — ako se ne filtrira striktno na `NNN-Note.wav` uzorak, `_bis` datoteke i (ako se ne paze putanje) datoteke iz `relXXXXX` podmapa mogu lažno promijeniti broj. Test u Tasku 2 mora imati sintetički fixture s `_bis` datotekom i potvrditi da se broji ispravno.
- **Wasselonneov short/medium/long pogrešno dodijeljen main/release ulogama**: ako se pretpostavka (long=main) pokaže pogrešnom mjerenjem trajanja/cue-pointova (isti postupak kao pilot Task 3 Step 1 za Zöblitz kurz/lang), rezultat je zvučno pogrešan Echo/Vox humana registar bez vidljive greške pri učitavanju. Task 3 mora sadržavati taj mjerni korak kao eksplicitni step, ne pretpostavku.
- **Cross-pitch korekcija primijenjena na pogrešan izvor, zaboravljena za Zöblitz/Wasselonne, ili pogrešnim predznakom**: Waltershausen (466,8 Hz) NIJE jedini necjelobrojni izvor — Zöblitz (Brustwerk, Chorton, +1,118 poluton) je pilot-planom eksplicitno odgodio ovu korekciju za "fazu punog hibrida", a Wasselonne nije dosad mjeren. Ako se bilo koji od ta 3 izvora zaboravi ili se predznak pobrka (previsoko umjesto prenisko), odgovarajuća divizija/registar zvuči pogrešno uštiman bez ikakve XML-greške koja bi to otkrila. Task 6 mora imati test za SVA 3 izvora koji potvrđuje iznos i smjer korekcije izračunat iz stvarnog izmjerenog Hz-omjera, ne nagađanje.

---

### Task 1: Proširi Rank model s poljima za korekciju ugađanja

**Files:**
- Modify: `src/codm/model.py`
- Modify: `src/codm/writer.py`
- Test: `tests/test_model.py`, `tests/test_writer.py`

**Interfaces:**
- Produces: `Rank` dataclass dobiva 2 nova polja: `tuning_adjust_semitones_036: float = 0.0`, `tuning_adjust_semitones_096: float = 0.0` (default 0 — postojeći pilot-poziv `Rank(...)` bez ovih argumenata mora nastaviti raditi nepromijenjeno).

- [ ] **Step 1: Napiši padajući test koji provjerava da `render_custom_organ` ispisuje nenul vrijednost za `Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones` kad je `Rank.tuning_adjust_semitones_036` postavljen**

```python
def test_render_applies_tuning_adjust_from_rank():
    rank = Rank(rank_id=1, name="Test", num_pipes=56, first_midi_note=36,
                package_id=1, main_folder="x", short_release_folder=None,
                pitch_harmonic_num=8, windchest_division_code=2,
                tuning_adjust_semitones_036=-11.8, tuning_adjust_semitones_096=-11.8)
    xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                               ranks=[rank], stopranks=[], required_packages=[])
    assert "<Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>-11.8</Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>" in xml
```

- [ ] **Step 2: Pokreni test, provjeri da pada (vrijednost je trenutno hardkodirano `0`)**

Run: `python3 -m unittest tests.test_writer -v`
Expected: FAIL (assertion mismatch, `0` umjesto `-11.8`)

- [ ] **Step 3: Dodaj `tuning_adjust_semitones_036`/`_096` polja (default `0.0`) u `Rank` u `src/codm/model.py`; u `src/codm/writer.py`'s `_rank_fields` zamijeni hardkodirane `0` vrijednosti za `Pitch_PipeMIDINoteNum036/096_TuningAdjustPercentSemitones` s `r.tuning_adjust_semitones_036`/`_096`**

- [ ] **Step 4: Pokreni test, provjeri da prolazi; zatim pokreni CIJELI postojeći suite da ništa iz pilota nije pokvareno**

Run: `python3 -m unittest discover -s tests -v`
Expected: svih 15 testova (14 postojećih + 1 novi) PASS

- [ ] **Step 5: Commit**

```bash
git add src/codm/model.py src/codm/writer.py tests/test_model.py tests/test_writer.py
git commit -m "feat: expose per-rank pitch tuning correction fields"
```

---

### Task 2: Hauptwerk divizija — ekstrakcija, mapiranje, generiranje

**Files:**
- Create: `src/codm/hauptwerk_division.py`
- Test: `tests/test_hauptwerk_division.py`
- Create (scratch, ne commitati): privremena mapa za selektivno raspakirane Görlitz/Waltershausen datoteke (npr. `/private/tmp/claude-501/.../goerlitz-extract/` ili slično u scratchpadu)

**Interfaces:**
- Consumes: `Rank`/`Stop`/`StopRank`/`Division` (Task 1), `render_custom_organ` (postojeći), `_validate_rank_folder` (postojeći iz `brustwerk_pilot.py` — ili lokalna kopija/generalizacija ako se raspon direktorija razlikuje).
- Produces: `build_hauptwerk_division(goerlitz_extract_root: Path, waltershausen_root: Path) -> tuple[Division, list[Rank], list[Stop], list[StopRank], list[tuple]]` — vraća komponente (NE cijeli XML string) da ih Task 5 može spojiti s ostalim divizijama. `required_packages` kao 5. element.

- [ ] **Step 1: Selektivno raspakiraj SAMO potrebne Görlitz mape** (ne cijeli ZIP) koristeći `zipfile.ZipFile.extract()` za svih 12 mapa iz tablice u Global Constraints (glavna mapa + `rel00200`/`rel00440` podmape za svaku), plus odgovarajuće `packageidNNNNNN.InstallationPackageDefinition_Hauptwerk_xml` datoteke za pakete 1811/1812/1813, u privremenu mapu u scratchpadu

- [ ] **Step 2: Napiši skriptu (jednokratnu, u scratchpadu, NE dio `src/`) koja za svih 12 Görlitz rankova izmjeri `smpl`-chunk omjer visine tona prema `Principal 8'` (grossoct8) na noti 060, po uzoru na mjerenje iz pilota, i ispiše tablicu rank→harmonijski_broj**

Run: ta skripta
Expected: tablica s 12 redaka, harmonijski brojevi (provjeriti da li iznose cijele brojeve kao kod Zöblitza, ili treba zaokruživanje — zapisati nalaz)

- [ ] **Step 3: Napiši padajući test koji provjerava da `build_hauptwerk_division` vraća 13 Rank/Stop/StopRank zapisa s DivisionCode=2 i StopCode u rasponu 2100-2199, i da su harmonijski brojevi jednaki onima izmjerenim u Step 2**

- [ ] **Step 4: Pokreni test, provjeri da pada**

Run: `python3 -m unittest tests.test_hauptwerk_division -v`
Expected: FAIL (`ImportError`)

- [ ] **Step 5: Implementiraj `build_hauptwerk_division(...)` koristeći mapiranje iz Global Constraints i izmjerene harmonijske brojeve iz Step 2. Za svaki Görlitz rank: `_validate_rank_folder`-style provjera (glavna mapa + rel00200 + rel00440, filtrirano striktno na `NNN-*.wav` uzorak da se `_bis` datoteke ne krivo broje). Za Waltershausen Bordun 16' rank: provjeri stvarnu strukturu `HW-PortunUntersatz16`/`-R1`/`-R2` mapa (paketi 255/256) prije pisanja koda — NE pretpostavljati da je identična Görlitzovoj konvenciji**

- [ ] **Step 6: Pokreni test, provjeri da prolazi**

Run: `python3 -m unittest tests.test_hauptwerk_division -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/codm/hauptwerk_division.py tests/test_hauptwerk_division.py
git commit -m "feat: build Hauptwerk division (13 stops, Görlitz + Waltershausen Bordun)"
```

---

### Task 3: Oberwerk divizija — ekstrakcija, mapiranje, generiranje

**Files:**
- Create: `src/codm/oberwerk_division.py`
- Test: `tests/test_oberwerk_division.py`

**Interfaces:**
- Consumes: isto kao Task 2.
- Produces: `build_oberwerk_division(goerlitz_extract_root: Path, wasselonne_root: Path) -> tuple[Division, list[Rank], list[Stop], list[StopRank], list[tuple]]`.

- [ ] **Step 1: Selektivno raspakiraj Görlitz OW/BW/HW(spitzflt4) mape iz tablice u Global Constraints (11 mapa) na isti način kao Task 2**

- [ ] **Step 2: Na Wasselonneovim `EchoCornet` i `GoVoixHumaine8` mapama, mjeri trajanje i broj cue-pointova za `short`/`medium`/`long` varijante (isti postupak kao pilot Task 3 Step 1 za kurz/lang) da se potvrdi koja je glavna (s loop-om) a koje su release-only**

Run: skripta za mjerenje
Expected: `long` ima najviše cue-pointova/najdulje trajanje (potvrđuje pretpostavku iz Global Constraints) — ili dokumentirati suprotan nalaz ako mjerenje to pokaže

- [ ] **Step 3: Izmjeri `smpl`-chunk harmonijske brojeve za svih 11 Görlitz OW/BW/HW rankova (isti postupak kao Task 2 Step 2) + za Wasselonneov EchoCornet/GoVoixHumaine8 (ovi su već 8' po nominalnoj specifikaciji — provjeriti odgovara mjerenju)**

- [ ] **Step 4: Napiši padajući test (isti obrazac kao Task 2 Step 3) koji provjerava 13 registara, DivisionCode=3, StopCode 2200-2299**

- [ ] **Step 5: Pokreni test, provjeri FAIL**

- [ ] **Step 6: Implementiraj `build_oberwerk_division(...)`**

- [ ] **Step 7: Pokreni test, provjeri PASS**

- [ ] **Step 8: Commit**

```bash
git add src/codm/oberwerk_division.py tests/test_oberwerk_division.py
git commit -m "feat: build Oberwerk division (13 stops, Görlitz + Wasselonne Echo/Vox humana)"
```

---

### Task 4: Pedal divizija — ekstrakcija, mapiranje, generiranje

**Files:**
- Create: `src/codm/pedal_division.py`
- Test: `tests/test_pedal_division.py`

**Interfaces:**
- Consumes: isto kao Task 2.
- Produces: `build_pedal_division(goerlitz_extract_root: Path) -> tuple[Division, list[Rank], list[Stop], list[StopRank], list[tuple]]`.

- [ ] **Step 1: Selektivno raspakiraj Görlitz Pedal mape (9 mapa, uključujući `Subbass16` iz paketa 1811 i `Contrabass16` iz paketa 1814 — provjeri Review Focus napomenu o tome da 1814 sadrži i nevezanu SW diviziju koju NE raspakiravati)**

- [ ] **Step 2: Izmjeri harmonijske brojeve za svih 8 jednostavnih Pedal rankova (sve osim Untersatz-a)**

- [ ] **Step 3: Napiši padajući test koji provjerava: 9 `Stop` zapisa (DivisionCode=1, StopCode 2000-2099), 10 `Rank` zapisa (8 jednostavnih registara + 2 za Untersatz = principalbas32 i Contrabass16), i 10 `StopRank` zapisa (8 jednostavnih stop↔rank veza + 2 veze za Untersatzov jedan StopCode prema njegova dva RankID-a)**

- [ ] **Step 4: Pokreni test, FAIL**

- [ ] **Step 5: Implementiraj `build_pedal_division(...)` — Untersatz 32'+16' kao jedan `Stop` + dva `StopRank` zapisa (jedan po principalbas32, jedan po Contrabass16), oba mapirana na puni pedal raspon**

- [ ] **Step 6: Pokreni test, PASS**

- [ ] **Step 7: Commit**

```bash
git add src/codm/pedal_division.py tests/test_pedal_division.py
git commit -m "feat: build Pedal division (9 stops, Görlitz, Untersatz as dual-rank stop)"
```

---

### Task 5: Spajanje sve 4 divizije + kupleri + tremulanti

**Files:**
- Create: `src/codm/full_organ.py`
- Modify: `src/codm/writer.py` (dodati `Coupler`/`Tremulant` podršku ako nedostaje — provjeriti prije pisanja koda, writer trenutno generira SAMO prazne `coupler`/`tremulant` ObjectList blokove)
- Test: `tests/test_full_organ.py`

**Interfaces:**
- Consumes: `build_hauptwerk_division`, `build_oberwerk_division`, `build_pedal_division` (Taskovi 2-4); Brustwerk podaci iz postojećeg `src/codm/brustwerk_pilot.py` (**napomena: treba dodati `build_brustwerk_division(zoblitz_root) -> tuple(...)` funkciju analognu ostalima u `brustwerk_pilot.py` — trenutno `build_brustwerk_pilot` vraća gotov XML string, ne komponente; potrebna mala izmjena/refaktor da vrati tuple komponenti, uz zadržavanje postojeće `build_brustwerk_pilot` funkcije i njenih testova nepromijenjenima za pilot).
- Produces: `Coupler`, `Tremulant` dataclasses u `src/codm/model.py`; proširen `render_custom_organ` koji prima `couplers: list[Coupler]` i `tremulants: list[Tremulant]` parametre (trenutno ih prima kao prazne liste implicitno — provjeriti potpisnicu prije izmjene); `build_full_organ() -> str`.

- [ ] **Step 1: Napiši padajući test koji provjerava da je Brustwerkov DivisionCode promijenjen na 4 i StopCode-ovi na 23xx kad se poziva kroz novu `build_brustwerk_division` funkciju (regresijski test za Review Focus stavku o DivisionCode sudaru)**

- [ ] **Step 2: Pokreni test, FAIL**

- [ ] **Step 3: Dodaj `build_brustwerk_division(zoblitz_root, division_code=4) -> tuple(...)` u `brustwerk_pilot.py` koja interno koristi isti mapping ali parametrizirano po `division_code` (ne hardkodirano `DIVISION_CODE=2`); `build_brustwerk_pilot` ostaje kao tanki wrapper koji zove `build_brustwerk_division(zoblitz_root, division_code=2)` radi kompatibilnosti s postojećim testovima**

- [ ] **Step 4: Pokreni test iz Step 1, PASS; pokreni CIJELI postojeći suite da pilot nije pokvaren**

Run: `python3 -m unittest discover -s tests -v`
Expected: svih postojećih 15 testova + novi, PASS

- [ ] **Step 5: Napiši padajući test koji provjerava da `build_full_organ()` vraća XML sa svih 44 `<StopCode>` (u `stop` tablici), 4 jedinstvena `DivisionCode` (1,2,3,4), i bez preklapanja StopCode raspona među divizijama (Review Focus stavka)**

- [ ] **Step 6: Pokreni test, FAIL**

- [ ] **Step 7: Dodaj `Coupler`/`Tremulant` dataclasses u `model.py` (polja prema Global Constraints tablici); proširi `writer.py`'s `render_custom_organ` da prihvaća i renderira `couplers`/`tremulants` liste umjesto praznih blokova; implementiraj `build_full_organ()` koji poziva sve 4 `build_*_division` funkcije, spaja njihove liste, dodaje 6 kuplera + 3 tremulanta prema Global Constraints odluci, i poziva `render_custom_organ(...)` s kompletnim podacima**

- [ ] **Step 8: Pokreni test, PASS**

- [ ] **Step 9: Pokreni `build_full_organ()` i zapiši rezultat u `/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/FreibergHybrid.CustomOrgan_Hauptwerk_xml`**

- [ ] **Step 10: Commit**

```bash
git add src/codm/full_organ.py src/codm/model.py src/codm/writer.py src/codm/brustwerk_pilot.py tests/
git commit -m "feat: merge all 4 divisions into complete 44-stop hybrid organ with couplers/tremulants"
```

---

### Task 6: Cross-pitch harmonizacija (svi izvori koji nisu na Görlitzovih 440 Hz)

**Zašto ovo nije samo o Waltershausenu**: pilot-recenzent je (usput, pri provjeri C1) izmjerio da je **Zöblitz** (Brustwerk, već izgrađen) na Chorton ugađanju, **+1,118 poluton iznad 440 Hz** — pilot-plan je to eksplicitno odgodio za "fazu punog hibridnog spoja" (vidi `2026-11-07-brustwerk-zoblitz-codm-pilot.md`, Global Constraints) — to je SADA. Wasselonne (Echo/Vox humana, Oberwerk) nije dosad mjeren niti u pilotu niti u ovom planu — treba ga mjeriti ovdje prvi put.

**Files:**
- Modify: `src/codm/brustwerk_pilot.py` (sve rankove, Chorton korekcija)
- Modify: `src/codm/hauptwerk_division.py` (Bordun 16' rank, Waltershausen korekcija)
- Modify: `src/codm/oberwerk_division.py` (Echo 5f i Vox humana 8' rankovi, ako mjerenje pokaže da Wasselonne nije na 440 Hz)
- Test: `tests/test_brustwerk_pilot.py`, `tests/test_hauptwerk_division.py`, `tests/test_oberwerk_division.py`

**Interfaces:**
- Consumes: `tuning_adjust_semitones_036`/`_096` polja iz Task 1.

- [ ] **Step 1: Izmjeri apsolutnu visinu tona (ne samo omjer među rankovima, već stvarni Hz na noti 060) za jedan referentni Görlitz rank (npr. HW grossoct8, note 060-C) kao "440 Hz master" baseline, zatim za: jedan Zöblitz rank (npr. Brustwerk Gedackt8, note 060), jedan Waltershausen rank (Bordun16/PortunUntersatz16, note 060), i Wasselonneov EchoCornet/GoVoixHumaine8 (note 060) — izračunaj svaki odnos u polutonovima: `12 * log2(izvor_Hz / goerlitz_Hz)`**

Run: skripta za mjerenje (čita `smpl` chunkove svih 4 izvora)
Expected: potvrda da je Görlitz stvarno na ~440 Hz referenci (ili bliže toj vrijednosti od ostalih), Zöblitz oko +1,118 poluton (potvrda prošlog nalaza), Waltershausen oko `12*log2(466.8/440)≈+1,037` poluton, Wasselonne nepoznato dok se ne izmjeri

- [ ] **Step 2: Napiši padajući test za svaki od 3 izvora (Zöblitz, Waltershausen, Wasselonne ako treba korekciju) koji provjerava da je `tuning_adjust_semitones_036`/`_096` postavljen na NEGATIVNU vrijednost izmjerenog poluton-odstupanja iz Step 1 (korekcija nadolje prema 440 Hz referenci) za SVAKI rank tog izvora**

- [ ] **Step 3: Pokreni testove, FAIL (trenutno 0 za sve)**

- [ ] **Step 4: Postavi `tuning_adjust_semitones_036`/`_096` na izmjerene vrijednosti za sve rankove triju izvora. Napomena: `TuningAdjustPercentSemitones` je nazvan "Percent" — provjeriti u Hauptwerkovoj ugrađenoj CODM dokumentaciji (`Other | Design tools | View ... format documentation`, korisnik mora otvoriti, ja nemam pristup) točnu definiciju prije finalnog postavljanja broja (je li 100=jedan poluton ili je vrijednost izravno u polutonovima) — primijeniti dosljedno na sva 3 izvora odjednom kad se konvencija utvrdi, ne pogađati po izvoru**

- [ ] **Step 5: Pokreni testove, PASS; pokreni cijeli suite**

Run: `python3 -m unittest discover -s tests -v`
Expected: svi testovi PASS

- [ ] **Step 6: Regeneriraj `FreibergHybrid.CustomOrgan_Hauptwerk_xml` (Task 5 Step 9 ponovno) i provjeri da su sve 3 korekcije prisutne**

- [ ] **Step 7: Commit**

```bash
git add src/codm/brustwerk_pilot.py src/codm/hauptwerk_division.py src/codm/oberwerk_division.py tests/
git commit -m "fix: harmonize pitch of Zoblitz (Chorton), Waltershausen (466.8Hz) and Wasselonne to 440Hz reference"
```

---

### Task 7: Ručna provjera u Hauptwerku (korisnik)

Isto kao pilot Task 4 — nema automatskih testova, zahtijeva Hauptwerk GUI.

- [ ] **Step 1 (korisnik): Instalirati/registrirati Görlitz, Wasselonne i Waltershausen pakete kroz Hauptwerkov vlastiti instalacijski postupak (isti problem kao za Zöblitz u pilotu — provjeriti ima li Prospectum/Sonus Paradisi/OrganArt svoj `.hwi`/instalacijski paket radije nego ručno kopiranje)**
- [ ] **Step 2 (korisnik): `Other | Design tools | Load custom organ...` → `FreibergHybrid`**
- [ ] **Step 3 (korisnik): Provjeriti svih 44 registra, 6 kuplera, 3 tremulanta; posebno osluškivanje Bordun 16' (pitch-korigiran) i Untersatz 32'+16' (dual-rank stop)**
- [ ] **Step 4 (korisnik, ako nešto zvuči pogrešno): Javiti točno koji registar/efekt, vraćamo se na odgovarajući Task**
