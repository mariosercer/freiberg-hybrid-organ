# Generička grafička konzola (Hauptwerkova standardna biblioteka) — plan implementacije

> **Za agentne izvršitelje:** OBAVEZNA PODVJEŠTINA: koristiti superpowers:subagent-driven-development (preporučeno) ili superpowers:executing-plans za izvršavanje ovog plana task-po-task. Koraci koriste checkbox (`- [ ]`) sintaksu za praćenje.

**Cilj:** Zamijeniti FreibergHybridov trenutni plain-text prikaz registara jednom prilagođenom grafičkom konzolnom stranicom (knobovi, tipke, pozadina) iz Hauptwerkove ugrađene standardne biblioteke slika — korisnikov izričit zahtjev: "generički izgled iz Hauptwerkove biblioteke", sve na jednoj stranici.

**Arhitektura:** CODM podržava prilagođeni grafički konzolni prikaz preko tri tablice (`CustomDisplayPage`, `CustomDisplayControlStyle`, `CustomDisplayKeyboardStyle`) + `CustomDisplay1_*` polja na `Stop`/`Coupler`/`Tremulant`/`Division` objektima. Istraženo izravno iz Hauptwerkovih vlastitih primjera (`ExampleCustomOrgan2`, `ExampleCustomOrgan4`) i standardne biblioteke slika (`HauptwerkStandardImages`, paket 1, instaliran lokalno) — ništa od niže navedenog nije nagađanje:
- Jedan `ControlStyleID` (drawknob s ugrađenim tekstom na licu) dovoljan je za SVIH 44 registra + 6 kuplera + 2 tremulanta — nema potrebe za zasebnim label-kontrolama.
- Tipkovnica se postavlja JEDNIM X,Y sidrom po diviziji (`Division.CustomDisplay1_Keyboard_PosPixels_X/Y` + `_KeyboardStyleID`) — Hauptwerk interno računa poziciju svake pojedine tipke iz stilom definiranih razmaka. Ne treba ručno računati poziciju svake tipke.
- Postojeće `CustomDisplay_EnableStdPages_*` zastavice OSTAJU `Y` (nepromijenjene) — nova stranica je DODATNA kartica, ne zamjena; stare kartice ostaju dostupne za kombinacije (general/divisional pistoni), koje ovaj plan ne pokriva.

**Tech Stack:** Isti kao ostatak projekta — Python 3 stdlib, `unittest`, postojeći `src/codm/model.py`/`writer.py`/`full_organ.py`.

**Spec:** Korisnikov zahtjev u razgovoru ("generički izgled iz Hauptwerkove biblioteke", "sve na jednoj stranici, pa ćemo podijeliti ako bude prenatrpano") + istraživanje ugrađeno u ovaj plan (Global Constraints).

## Global Constraints

### Odabrani stilovi (iz `ExampleCustomOrgan2.CustomOrgan_Hauptwerk_xml`, lokalno instalirano, paket 1 "Hauptwerk Standard Components")

Sve slike dolaze iz `HauptwerkStandardImages/` unutar paketa 1, koji je već u `REQUIRED_PACKAGES` svake divizije.

**Control style (registar/kupler/tremulant) — JEDAN stil za sve:**
- `Stop07-Drawknob-Wood-Small-{Off,On}.bmp` + `-Mask.bmp`, 65×65px klikabilno područje, ugrađen bijeli Verdana 8px tekst (bounding box 2,1–61,61) — ime registra se automatski renderira NA knobu, ne treba zasebna labela.
- Ovo je `ControlStyleID=10` u `ExampleCustomOrgan2` — u našoj datoteci bit će `ControlStyleID=1` (jedini stil koji definiramo).

**Keyboard style — DVA stila (manual, pedal):**
- Manual: `Man07IvorySm` (= `ExampleCustomOrgan2` `KeyboardStyleID=4`) — `KeyImageSet007`, razmak naravnih tipki 12px, visina klikabilnog područja 32px. U našoj datoteci `KeyboardStyleID=1`.
- Pedal: `Ped06OldSm` (= `ExampleCustomOrgan2` `KeyboardStyleID=7`) — `KeyImageSet006`, uniformni razmak 12-24px (prirodna tipka 24px, sve ostalo 12px), visina 70px. U našoj datoteci `KeyboardStyleID=2`.
- Oba stila repliciraju TOČNO polja i slikovne datoteke iz `ExampleCustomOrgan2` (kopiraj-zalijepi, kako vodič i preporučuje: "copy and paste those two tables... and use immediately").

**Stranica:**
- Jedna `CustomDisplayPage` (`DisplayPageID=1`, `Name="Console"`), pozadina `HauptwerkStandardImages/SeamlessBackgrounds-WoodPanelling-DarkCherry.png` (paket 1) — ista pozadina koju `ExampleCustomOrgan4` koristi.
- `_general.CustomDisplay_DefaultDisplayPageID=1` (otvara se na ovoj stranici prvoj).
- `_general.CustomDisplay_ConsoleWidthPixels`/`_ConsoleHeightPixels` — izračunati iz stvarnog rasporeda (Task Step 3 ispisuje točne vrijednosti; okvirna procjena: ~1000×1400px, provjeriti nakon implementacije).

### Raspored (moja odluka — sve na jednoj stranici, grupirano po diviziji, korisnik može tražiti promjenu kasnije)

Odozgo prema dolje:
1. Redovi knobova, jedan blok po diviziji: **Pedal (9), Oberwerk (13), Hauptwerk (13), Brustwerk (9)** — unutar bloka, registri u izvornom redoslijedu iz spec-a; zamatanje u redove od ~12 knobova (70px razmak uključujući margin) po redu.
2. Red kuplera (6) i red tremulanata (2), nakon 4 divizijska bloka.
3. Tipkovnice, odozgo prema dolje: **Oberwerk, Hauptwerk, Brustwerk, Pedal** (moja odluka — nema univerzalne konvencije za 3-manualni raspored, pedal uvijek zadnji/dolje jer se svira nogama).

Širina tipkovnice po diviziji (broj naravnih tipki × razmak stila, aproksimacija dovoljna za sprječavanje preklapanja, ne treba biti piksel-precizna):
- Hauptwerk/Oberwerk (Görlitz, 58 tipki, MIDI 36-93): ≈34 naravne tipke × 12px ≈ 408px
- Brustwerk (Zöblitz, 56 tipki, MIDI 36-91): ≈33 naravne tipke × 12px ≈ 396px
- Pedal (Görlitz, 32 tipke, MIDI 36-67): ≈19 naravnih tipki × 24px ≈ 456px

### Model/writer polja koja nedostaju (treba dodati)

`Stop`, `Coupler`, `Tremulant` dataklase u `model.py` TRENUTNO nemaju polja pozicije/stila (`writer.py` ih već renderira hardkodirano na `None`/`0` za `CustomDisplay1_DisplayPageID`/`_Text`/`_ControlStyleID`/`_PosPixels_X`/`_Y`). `Division` VEĆ ima ta polja renderirana u `_division_display_block`, ali hardkodirana na `None`/`0` — treba ih učiniti postavljivima iz `Division` dataklase (koja trenutno nema `keyboard_*` polja).

Potrebna nova polja (sve s default vrijednostima da postojeći pozivi ne puknu):
- `Stop`/`Coupler`/`Tremulant`: `display_page_id: int | None = None`, `control_style_id: int | None = None`, `pos_x: int = 0`, `pos_y: int = 0` (tekst na knobu = postojeće `display_name`, ne treba novo polje).
- `Division`: `keyboard_display_page_id: int | None = None`, `keyboard_style_id: int | None = None`, `keyboard_pos_x: int = 0`, `keyboard_pos_y: int = 0`.

Potrebne nove `model.py` dataklase: `ControlStyle`, `KeyboardStyle`, `DisplayPage` (polja prema gornjim stilovima — vidi Review Focus za točan popis polja iz `ExampleCustomOrgan2`).

`render_custom_organ` mora primiti i renderirati `control_styles`, `keyboard_styles`, `display_pages` liste (trenutno `_empty_object_list` za `customdisplaycontrolstyle`/`customdisplaykeyboardstyle`/`customdisplaypage`).

## Review Focus

- **Izmišljena vrijednost stila umjesto kopirane**: svako polje `ControlStyle`/`KeyboardStyle` MORA biti prepisano izravno iz `ExampleCustomOrgan2.CustomOrgan_Hauptwerk_xml` (ControlStyleID 10, KeyboardStyleID 4 i 7) — ne izmišljati nijednu vrijednost (slikovne datoteke, razmake, boje, font). Test mora uspoređivati generirani XML s točnim nizovima iz izvornika.
- **Preklapanje elemenata na stranici** (52 knoba + 4 tipkovnice na jednoj stranici): test mora provjeriti da se nijedan knob/tipkovnica ne preklapa (bounding-box provjera), ne samo da su "negdje" postavljeni.
- **Console canvas manji od stvarnog sadržaja**: `CustomDisplay_ConsoleWidthPixels`/`_HeightPixels` moraju biti ≥ najdesnijeg/najdonjeg elementa + njegove širine/visine, inače se dio konzole odreže. Test mora provjeriti ovu nejednakost za svaki element.
- **Pogrešan `DisplayPageID` na nekom elementu** (npr. zaboravljen na 1 od 52+4 elementa) ostavio bi taj element nevidljivim na našoj stranici bez vidljive greške pri učitavanju. Test mora provjeriti da SVI elementi (44 registra + 6 kuplera + 2 tremulanta + 4 tipkovnice) imaju `CustomDisplay1_DisplayPageID=1`.
- **Zaboravljen `ControlStyleID`/`KeyboardStyleID` na nekom elementu** — isti tihi rizik kao gore, zaseban test.

---

### Task 1: Prilagođena grafička konzola — stilovi, stranica, raspored, ožičenje

**Files:**
- Modify: `src/codm/model.py` (nove dataklase `ControlStyle`/`KeyboardStyle`/`DisplayPage`; nova polja na `Stop`/`Coupler`/`Tremulant`/`Division`)
- Modify: `src/codm/writer.py` (renderirati nove tablice i polja umjesto hardkodiranih praznih)
- Create: `src/codm/console_layout.py` (generator rasporeda — računa pozicije za 52 kontrole + 4 sidra tipkovnice)
- Modify: `src/codm/full_organ.py` (pozvati `console_layout`, dodati stilove/stranicu, postaviti polja na postojeće stopove/kuplere/tremulante/divizije)
- Test: `tests/test_model.py`, `tests/test_writer.py`, `tests/test_console_layout.py`, `tests/test_full_organ.py`

**Interfaces:**
- Consumes: postojeći `Stop`/`Coupler`/`Tremulant`/`Division` iz `model.py`; postojeći `build_full_organ()` sklop iz `full_organ.py`.
- Produces: `console_layout.layout_controls(stops, couplers, tremulants) -> dict[str, tuple[int,int]]` (mapira `"stop:<code>"`/`"coupler:<code>"`/`"tremulant:<code>"` na (x,y)); `console_layout.layout_keyboard_anchors() -> dict[int, tuple[int,int]]` (mapira `division_code` na (x,y) sidro tipkovnice); `console_layout.console_size(...) -> tuple[int,int]`.

- [ ] **Step 1: Napiši padajući test koji provjerava da `ControlStyle`/`KeyboardStyle`/`DisplayPage` dataklase postoje s ispravnim poljima, i da `render_custom_organ` renderira njihove tablice umjesto prazne**

- [ ] **Step 2: Pokreni test, FAIL**

- [ ] **Step 3: Dodaj dataklase u `model.py` (polja kopirana iz `ExampleCustomOrgan2`'s `ControlStyleID=10` i `KeyboardStyleID=4,7` zapisa — vidi Global Constraints), dodaj nova polja na `Stop`/`Coupler`/`Tremulant`/`Division`, proširi `writer.py`'s `_stop_fields`/`_coupler_fields`/`_tremulant_fields`/`_division_fields` da čitaju iz njih umjesto hardkodiranih `None`/`0`, dodaj `_control_style_fields`/`_keyboard_style_fields`/`_display_page_fields`, proširi `render_custom_organ` potpis s `control_styles=()`, `keyboard_styles=()`, `display_pages=()`, i proširi `_general_fields`/`render_custom_organ` da prima `console_width`, `console_height`, `default_display_page_id` umjesto hardkodiranih `0`/`None` za `CustomDisplay_ConsoleWidthPixels`/`_ConsoleHeightPixels`/`_DefaultDisplayPageID`**

- [ ] **Step 4: Pokreni test, PASS; pokreni cijeli suite**

- [ ] **Step 5: Napiši padajući test za `console_layout.py` koji provjerava: svih 52 kontrola ima jedinstvenu, nepreklapajuću (x,y) poziciju (bounding-box provjera s 65×65 veličinom knoba + margin), 4 sidra tipkovnice ne preklapaju ni međusobno ni s redovima knobova iznad njih, i da `console_size(...)` vraća dimenzije ≥ svaki element + njegova veličina**

- [ ] **Step 6: Pokreni test, FAIL**

- [ ] **Step 7: Implementiraj `console_layout.py` — raspored po diviziji (Pedal/Oberwerk/Hauptwerk/Brustwerk redom, zamatanje u redove od ~12 knobova), red kuplera, red tremulanata, zatim 4 sidra tipkovnice (Oberwerk/Hauptwerk/Brustwerk/Pedal odozgo nadolje) prema Global Constraints rasporedu**

- [ ] **Step 8: Pokreni test, PASS**

- [ ] **Step 9: Napiši padajući test na `build_full_organ()` razini koji provjerava: svih 44+6+2=52 kontrola i sve 4 divizije imaju `CustomDisplay1_DisplayPageID=1`, odgovarajući `ControlStyleID`/`KeyboardStyleID`, i da je `CustomDisplay_ConsoleWidthPixels`/`_HeightPixels` dosljedan s `console_layout.console_size(...)`**

- [ ] **Step 10: Pokreni test, FAIL**

- [ ] **Step 11: Ožičiti `full_organ.py` — pozvati `console_layout`, postaviti nova polja na sve stopove/kuplere/tremulante (mutacija postojećih objekata, isti pattern kao `_wire_oberwerk_tremulant`)/divizije, dodati `ControlStyle`/`KeyboardStyle`/`DisplayPage` instance, postaviti `_general` dimenzije i `CustomDisplay_DefaultDisplayPageID=1` (potrebno: provjeriti postoji li već `_general`-level parametar u `render_custom_organ` za console width/height/default page — ako ne, dodati)**

- [ ] **Step 12: Pokreni test, PASS; pokreni cijeli suite; regeneriraj `FreibergHybrid.CustomOrgan_Hauptwerk_xml`**

- [ ] **Step 13: Commit**

```bash
git add src/codm/model.py src/codm/writer.py src/codm/console_layout.py src/codm/full_organ.py tests/
git commit -m "feat: add generic graphical console (Hauptwerk standard image library)"
```
