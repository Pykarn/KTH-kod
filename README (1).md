# KTH-kod — Canvas-material, automatiskt sorterat

Det här repot hämtar filer (föreläsningar, tentor, övningar, litteratur) från
Canvas, sorterar dem med en lokal AI (Ollama) och gör dem tillgängliga på
GitHub — både via `git pull` och som en webbsida via GitHub Pages.

## Innehåll

1. [Översikt: hur det hänger ihop](#1-översikt-hur-det-hänger-ihop)
2. [Vilken terminal ska jag använda?](#2-vilken-terminal-ska-jag-använda)
3. [Engångsinstallation](#3-engångsinstallation)
4. [Canvas-token](#4-canvas-token)
5. [Vad ändrar jag i vilken fil? (snabbguide)](#5-vad-ändrar-jag-i-vilken-fil-snabbguide)
6. [Steg för steg: lägga till en ny kurs](#6-steg-för-steg-lägga-till-en-ny-kurs)
7. [Steg för steg: köra en synk](#7-steg-för-steg-köra-en-synk)
8. [Ändra sorteringen (kategorier och AI-modell)](#8-ändra-sorteringen-kategorier-och-ai-modell)
9. [Kontrollera innan du pushar](#9-kontrollera-innan-du-pushar)
10. [Pusha till GitHub](#10-pusha-till-github)
11. [GitHub Pages (webbsida)](#11-github-pages-webbsida)
12. [Använda materialet på en annan dator](#12-använda-materialet-på-en-annan-dator)
13. [Felsökning](#13-felsökning)
14. [Säkerhet och upphovsrätt](#14-säkerhet-och-upphovsrätt)

---

## 1. Översikt: hur det hänger ihop

```
KTH-kod/
├── canvas_download.py          <- steg 1: hämtar filer från Canvas
├── organize_and_build_site.py  <- steg 2: sorterar filer + bygger webbsidan
├── .gitignore                  <- talar om för Git vad som INTE ska med
├── canvas_downloads/           <- tillfällig arbetsmapp (committas ALDRIG)
│   └── EL1000/ ...             <- allt "rått" och osorterat från Canvas
└── KTH_KOD/                    <- färdigt resultat, det som pushas
    ├── index.html              <- startsida med länkar till alla kurser
    └── EL1000/
        ├── index.html          <- kursens egen sida
        ├── exam/
        ├── lecture/
        ├── exercise/
        ├── literature/
        └── other/
```

Flödet är alltid:

```
Canvas  --canvas_download.py-->  canvas_downloads/  --organize_and_build_site.py-->  KTH_KOD/  --git push-->  GitHub
```

- **`canvas_download.py`** loggar in mot Canvas med ditt token och sparar allt
  den hittar i `canvas_downloads/<kurs>/`. Den tittar på Files-fliken, och
  söker dessutom igenom startsida, moduler, sidor, uppgifter, anslag och
  kursplan efter filer och GitHub-länkar. Hittas ett GitHub-repo laddas hela
  repot ner. Ingen AI används här.
- **`organize_and_build_site.py`** går igenom `canvas_downloads/`, ber Ollama
  avgöra om varje fil är `exam`, `lecture`, `exercise`, `literature` eller
  `other`, kopierar filen till rätt mapp i `KTH_KOD/` och bygger
  `index.html`-sidor.

Båda skripten är **säkra att köra om**: `canvas_download.py` hoppar över filer
du redan har, och `organize_and_build_site.py` bygger om kursmapparna.

---

## 2. Vilken terminal ska jag använda?

Alla kommandon i den här guiden skrivs i en **terminal**. Vilken du använder
beror på ditt operativsystem:

| System  | Terminal                                                        | Hur du öppnar den |
|---------|-----------------------------------------------------------------|-------------------|
| Windows | **PowerShell** (rekommenderas) eller *Terminal* i Windows 11    | Tryck Windows-tangenten, skriv `PowerShell`, Enter |
| macOS   | **Terminal**                                                    | Cmd + Mellanslag, skriv `Terminal`, Enter |
| Linux   | Valfri terminal (Bash)                                          | Ctrl + Alt + T |

**Tips (alla system):** Öppna repomappen i **VS Code** (gratis, code.visualstudio.com)
och använd dess inbyggda terminal via menyn *Terminal → New Terminal*. Då
startar terminalen automatiskt i rätt mapp, och du kan redigera
Python-filerna i samma fönster.

> **Viktigt:** Alla kommandon nedan ska köras **inifrån repomappen** `KTH-kod`.
> Skripten använder relativa sökvägar (`canvas_downloads`, `KTH_KOD`), så
> körs de från fel mapp skapas filerna på fel ställe.

Gå till repomappen så här (justera sökvägen efter var du klonade repot):

```powershell
# Windows (PowerShell)
cd C:\Users\DittNamn\KTH-kod
```
```bash
# macOS / Linux
cd ~/KTH-kod
```

Kontrollera att du är rätt med `ls` (macOS/Linux) eller `dir` (Windows) — du
ska se `canvas_download.py` i listan.

### `python` eller `python3`?

- **Windows:** använd oftast `python`.
- **macOS/Linux:** använd oftast `python3`.

Fungerar inte det ena, prova det andra. Resten av guiden skriver `python`;
byt till `python3` om du sitter på Mac/Linux.

---

## 3. Engångsinstallation

Görs en gång per dator.

### 3.1 Installera Python
1. Ladda ner från **python.org/downloads** och kör installationen.
2. **Windows:** kryssa i **"Add python.exe to PATH"** på första skärmen.
3. Öppna en *ny* terminal och kontrollera:
   ```
   python --version
   ```
   (eller `python3 --version` på Mac/Linux). Du ska se t.ex. `Python 3.12.x`.

### 3.2 Installera Git
1. Ladda ner från **git-scm.com/downloads**, installera med standardval.
2. Kontrollera i en ny terminal:
   ```
   git --version
   ```

### 3.3 Installera Ollama (lokal AI)
Behövs bara på datorn där du kör `organize_and_build_site.py`.

1. Ladda ner från **ollama.com/download** och installera.
2. Hämta en modell i terminalen:
   ```
   ollama pull llama3.2
   ```
3. Kontrollera att modellen finns:
   ```
   ollama list
   ```
   Ollama körs automatiskt i bakgrunden efter installation. Om inte, kör
   `ollama serve` i en separat terminal och låt den vara öppen.

> `llama3.2` är en liten modell och sorterar ibland fel. För bättre
> träffsäkerhet, se [kapitel 8](#8-ändra-sorteringen-kategorier-och-ai-modell).

### 3.4 Klona repot
```
git clone https://github.com/Pykarn/KTH-kod.git
cd KTH-kod
```

### 3.5 Installera Python-paketen
```
pip install requests pypdf
```

- `requests` krävs (pratar med Canvas och Ollama).
- `pypdf` är valfritt men **rekommenderat**: då läser skriptet första sidan i
  varje PDF och ger texten till AI:n, vilket gör sorteringen mycket
  träffsäkrare (filnamnet `EL1000_F4_AF.pdf` säger lite, men första sidan
  "Lecture 4: Bode Plot" avslöjar direkt att det är en föreläsning).

Om `pip` inte hittas, prova:
```
python -m pip install requests pypdf
```

### 3.6 Skapa en `.gitignore` (så att råfiler och token aldrig pushas)

Skapa en fil som heter exakt `.gitignore` (med punkt, utan filändelse) i
repomappen med detta innehåll:

```
canvas_downloads/
__pycache__/
*.pyc
```

Kontrollera att den fungerar: efter att du kört `canvas_download.py` ska
`git status` **inte** lista `canvas_downloads/`.

---

## 4. Canvas-token

Tokenet är ditt lösenord mot Canvas. Det ger åtkomst till ditt konto.

### 4.1 Skapa token
1. Logga in på **canvas.kth.se** → klicka på din profilbild → **Settings**.
2. Scrolla till **Approved Integrations** → **+ New Access Token**.
3. Ge det ett namn (t.ex. `kth-kod`), lämna utgångsdatum tomt eller sätt ett,
   klicka **Generate Token**.
4. **Kopiera tokenet direkt** — det visas bara en gång.

### 4.2 Använd token (miljövariabel, ALDRIG i filen)
Sätt det som en miljövariabel i terminalen **varje gång du öppnar en ny
terminal** (variabeln försvinner när terminalen stängs, vilket är meningen):

```powershell
# Windows (PowerShell)
$env:CANVAS_TOKEN = "ditt-token-här"
```
```bash
# macOS / Linux
export CANVAS_TOKEN="ditt-token-här"
```

Skriv **inte** in tokenet i `canvas_download.py`. Då riskerar du att det
hamnar på GitHub.

### 4.3 Om tokenet läckt
Hamnar tokenet i en fil, en chatt eller en commit: gå till Canvas → Settings →
Approved Integrations, klicka på papperskorgen vid tokenet och skapa ett nytt.

---

## 5. Vad ändrar jag i vilken fil? (snabbguide)

| Jag vill...                                  | Fil                          | Vad jag ändrar |
|----------------------------------------------|------------------------------|----------------|
| Hämta en ny kurs från Canvas                 | `canvas_download.py`         | Lägg till en rad i `COURSE_IDS` |
| Sortera/bygga en ny kurs                     | `organize_and_build_site.py` | Lägg till kurskoden i listan `COURSES` |
| Sluta hantera en kurs                        | båda                         | Ta bort raden/kurskoden i båda filerna |
| Byta AI-modell                               | `organize_and_build_site.py` | `OLLAMA_MODEL` |
| Ändra eller lägga till kategorier            | `organize_and_build_site.py` | Ordlistan `CATEGORIES` |
| Förbättra hur AI:n tolkar en kategori        | `organize_and_build_site.py` | Beskrivningen i `CATEGORIES` |
| Ändra var den färdiga sidan hamnar           | `organize_and_build_site.py` | `SITE_DIR` |
| Använda ett annat Canvas (inte KTH)          | `canvas_download.py`         | `CANVAS_URL` (eller miljövariabeln `CANVAS_URL`) |
| Behålla gamla/manuellt flyttade filer        | `organize_and_build_site.py` | `CLEAN_OLD_OUTPUT = False` |
| Stänga av PDF-läsningen                      | `organize_and_build_site.py` | `USE_PDF_PREVIEW = False` |

**Så redigerar du filerna:** högerklicka på filen → öppna med VS Code
(rekommenderas) eller Anteckningar/TextEdit. Spara med Ctrl+S (Cmd+S på Mac).
Python är känsligt för **indrag** (mellanslag i början av raden) — behåll
indragen precis som de är och ändra bara texten och siffrorna.

---

## 6. Steg för steg: lägga till en ny kurs

Exempel: du vill lägga till kursen `SF1626` med Canvas-ID `65123`.

### Steg 1 — Hitta kurs-ID:t
Öppna kursen i Canvas i webbläsaren och titta på adressen:
```
https://canvas.kth.se/courses/65123
                                ^^^^^ det här är kurs-ID:t
```

### Steg 2 — Lägg till kursen i `canvas_download.py`
Hitta `COURSE_IDS` (nära toppen) och lägg till en rad. **Glöm inte kommatecknet
i slutet av raden.**

```python
COURSE_IDS = {
    "DD1385": 63900,
    "SF1930": 65047,
    "EL1000": 64209,
    "SF1626": 65123,      # <- ny rad
}
```

- Texten till vänster (`"SF1626"`) är **mappnamnet**. Du väljer det själv, men
  använd kurskoden så blir det konsekvent.
- Numret till höger är kurs-ID:t från steg 1.

### Steg 3 — Lägg till kursen i `organize_and_build_site.py`
Hitta `COURSES` högst upp bland inställningarna:

```python
COURSES = ["EL1000", "SF1930", "DD1385", "SF1626"]
```

> **Namnen måste vara exakt likadana** i båda filerna (stora/små bokstäver
> spelar roll). `"SF1626"` i `COURSE_IDS` ↔ `"SF1626"` i `COURSES`. Annars
> hittar sorteringsskriptet inte mappen och hoppar över kursen med
> meddelandet `[skip] canvas_downloads/... not found`.

### Steg 4 — Kör
Följ [kapitel 7](#7-steg-för-steg-köra-en-synk).

### Köra bara en eller några kurser
Du behöver inte ta bort kurser permanent. Vill du bara synka en kurs just nu:
- I `canvas_download.py`: kommentera bort de andra raderna med `#` framför:
  ```python
  COURSE_IDS = {
      # "DD1385": 63900,
      # "SF1930": 65047,
      "EL1000": 64209,
  }
  ```
- I `organize_and_build_site.py`: ändra listan till `COURSES = ["EL1000"]`.

> **OBS:** startsidan `KTH_KOD/index.html` byggs om vid varje körning och
> listar bara kurserna i `COURSES`. Kör du med bara en kurs försvinner de
> andra från **startsidans länklista** (deras mappar och filer ligger kvar).
> Kör med alla kurser innan du pushar om du vill ha en komplett startsida.

---

## 7. Steg för steg: köra en synk

Görs på huvuddatorn (den med Python + Ollama).

**1. Öppna en terminal i repomappen** (se [kapitel 2](#2-vilken-terminal-ska-jag-använda)).

**2. Kontrollera att Ollama kör:**
```
ollama list
```
Visas en lista med modeller är allt OK. Får du ett felmeddelande, starta
Ollama (öppna appen, eller kör `ollama serve` i en annan terminal).

**3. Sätt token** (för just den här terminalen):
```powershell
$env:CANVAS_TOKEN = "ditt-token-här"          # Windows
```
```bash
export CANVAS_TOKEN="ditt-token-här"          # macOS / Linux
```

**4. Hämta filer från Canvas:**
```
python canvas_download.py
```
Du ser vilka filer som laddas ner. Meddelandet `403 Forbidden`, eller att ett
ställe inte hittar något, är normalt (se [felsökning](#13-felsökning)). Filer
sparas i `canvas_downloads/<kurs>/`.

**5. Sortera och bygg sidan:**
```
python organize_and_build_site.py
```
Skriptet skriver en rad per fil, t.ex.:
```
Organizing EL1000...
  EL1000_F4_AF.pdf  ->  lecture
  tenta_2022.pdf    ->  exam
```
Om Ollama inte kan nås skriver skriptet det **en gång i början** och sorterar
då alla filer med enkla nyckelord i filnamnet i stället. Det blir sämre
sortering — starta Ollama och kör om.

**6. Kontrollera resultatet** i `KTH_KOD/` (se [kapitel 9](#9-kontrollera-innan-du-pushar)),
och pusha sedan ([kapitel 10](#10-pusha-till-github)).

### Hela rutinen i ett block

```powershell
# Windows (PowerShell), i repomappen
$env:CANVAS_TOKEN = "ditt-token-här"
python canvas_download.py
python organize_and_build_site.py
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```
```bash
# macOS / Linux, i repomappen
export CANVAS_TOKEN="ditt-token-här"
python3 canvas_download.py
python3 organize_and_build_site.py
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```
(Gör kontrollen i kapitel 9 innan `git add .`.)

---

## 8. Ändra sorteringen (kategorier och AI-modell)

Allt du behöver ändra finns i blocket `SETTINGS` högst upp i
`organize_and_build_site.py`.

### 8.1 Byta AI-modell
Större modeller sorterar bättre men är långsammare och kräver mer minne.

1. Hämta modellen:
   ```
   ollama pull llama3.1:8b
   ```
2. Ändra i `organize_and_build_site.py`:
   ```python
   OLLAMA_MODEL = "llama3.1:8b"
   ```
Andra bra alternativ: `qwen2.5:7b`. Namnet måste matcha det som står i
`ollama list`.

### 8.2 Ändra kategorier
`CATEGORIES` styr **både** mapparna som skapas, rubrikerna på webbsidan och
vad AI:n får veta om varje kategori:

```python
CATEGORIES = {
    "exam": "old exams, exam solutions, tentamen, re-exams, practice exams",
    "lecture": "lecture slides, lecture notes, presentations, 'Lecture N' / 'Föreläsning N'",
    "exercise": "exercise sheets, problem sets, labs, assignments, homework, tutorials and their solutions",
    "literature": "textbooks, book chapters, compendiums, reference sheets, formula sheets, articles",
    "other": "anything that clearly fits none of the above (syllabus, schedules, admin info)",
}
```

- **Byta namn på en mapp** (t.ex. `lecture` → `slides`): ändra nyckeln
  (texten till vänster). Skriptet skapar då mappen `slides/` nästa gång.
  Kom ihåg att den gamla `lecture/`-mappen finns kvar i git tills du tagit
  bort den (med `CLEAN_OLD_OUTPUT = True` rensas bara mappar som finns i
  `CATEGORIES`, så ta bort gamla `lecture/`-mappar för hand).
- **Lägga till en kategori** (t.ex. `solutions`): lägg till en ny rad med
  beskrivning på engelska — modellen presterar bäst på engelska
  beskrivningar. Behåll `"other"` som sista rad.
- **Förbättra träffsäkerheten**: om AI:n ofta hamnar fel för en viss typ av
  fil, lägg till ord som beskriver den i kategorins beskrivning. Exempel:
  sorteras laborationsinstruktioner fel, lägg till `lab instructions` under
  `exercise`.

> Håll kategorinamnen enkla: små bokstäver, inga mellanslag eller
> specialtecken (de blir mappnamn och webbadresser).

### 8.3 Övriga inställningar

```python
SOURCE_DIR = "canvas_downloads"   # var canvas_download.py sparar filer
SITE_DIR = "KTH_KOD"              # var det färdiga resultatet hamnar
CLEAN_OLD_OUTPUT = True           # rensa kursens kategorimappar innan ombyggnad
USE_PDF_PREVIEW = True            # låt AI:n läsa första sidan i PDF-filer
```

**`CLEAN_OLD_OUTPUT`:** med `True` tas kursens kategorimappar
(`exam/`, `lecture/` ...) och `index.html` bort innan de byggs om. Det är det
som fixar filer som hamnat fel i en tidigare körning. Det är säkert eftersom
råfilerna finns kvar i `canvas_downloads/`. Sätt `False` om du lagt in egna
filer direkt i `KTH_KOD/` som du vill behålla.

### 8.4 En fil hamnade i fel mapp — vad gör jag?
1. Kolla att Ollama faktiskt kördes (stod det `Ollama is not reachable` i början?).
2. Installera `pypdf` (`pip install pypdf`) om du inte gjort det.
3. Byt till en större modell (kapitel 8.1).
4. Förtydliga kategoribeskrivningen (kapitel 8.2) och kör om
   `python organize_and_build_site.py`.
5. Som sista utväg: flytta filen för hand till rätt mapp. Kör du skriptet igen
   med `CLEAN_OLD_OUTPUT = True` skrivs din ändring över, så sätt det till
   `False` först eller flytta filen igen efteråt.

---

## 9. Kontrollera innan du pushar

### 9.1 Ta bort skräpfiler
Länksökningen i `canvas_download.py` kan ibland ge filer utan riktiga
filnamn (bara siffror, eller `download` / `preview`). Det är inte riktigt
kursmaterial och kan innehålla känslig data. Leta efter dem:

```powershell
# Windows (PowerShell)
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' }
```
```bash
# macOS / Linux
find KTH_KOD -type f \( -regex '.*/[0-9]+' -o -name download -o -name preview \)
```

Är listan inte tom, ta bort filerna:

```powershell
# Windows (PowerShell)
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' } | Remove-Item
```
```bash
# macOS / Linux
find KTH_KOD -type f \( -regex '.*/[0-9]+' -o -name download -o -name preview \) -delete
```

### 9.2 Titta igenom resultatet
- Öppna `KTH_KOD/<kurs>/` och kolla att tentor ligger i `exam/`, föreläsningar
  i `lecture/` osv.
- Dubbelklicka på `KTH_KOD/index.html` för att förhandsgranska webbsidan lokalt.
- Kör `git status` för att se exakt vad som kommer med i nästa commit.

---

## 10. Pusha till GitHub

```
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```

Första gången du pushar från en dator kan en webbläsare öppnas för
inloggning — välj **"Sign in with your browser"**.

Blockerar GitHub pushen på grund av "secrets" (t.ex. hittade
AWS-nycklar i någon fil), se [felsökning](#13-felsökning).

---

## 11. GitHub Pages (webbsida)

> **Observera:** GitHub Pages kan med "Deploy from a branch" bara publicera
> från rotmappen (`/`) eller en mapp som heter `/docs`. Mappen `/KTH_KOD`
> går **inte** att välja. Det finns två sätt att lösa det:

### Alternativ A (rekommenderas): GitHub Actions publicerar `KTH_KOD/`

1. Skapa filen `.github/workflows/pages.yml` i repot (skapa mapparna
   `.github` och `workflows` om de saknas) med detta innehåll:

   ```yaml
   name: Deploy Pages
   on:
     push:
       branches: [main]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: pages
     cancel-in-progress: true

   jobs:
     deploy:
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/checkout@v4
         - uses: actions/configure-pages@v5
         - uses: actions/upload-pages-artifact@v3
           with:
             path: KTH_KOD
         - id: deployment
           uses: actions/deploy-pages@v4
   ```
2. Gå till **github.com/Pykarn/KTH-kod → Settings → Pages**.
3. Under **Build and deployment → Source**, välj **GitHub Actions**.
4. Pusha. Under fliken **Actions** kan du följa publiceringen. Efter ca 1
   minut finns sidan på t.ex. `https://pykarn.github.io/KTH-kod/`.

### Alternativ B: byt mappnamn till `docs`
1. Ändra i `organize_and_build_site.py`: `SITE_DIR = "docs"`.
2. Flytta/byt namn på den befintliga mappen `KTH_KOD` till `docs`.
3. Settings → Pages → **Deploy from a branch** → Branch `main`, mapp `/docs` → Save.

(Då heter mappen `docs/` i stället för `KTH_KOD/` överallt i guiden.)

**Notera:** Pages från ett *privat* repo kräver ett betalt GitHub-konto, och
sidan kan vara nåbar för alla som har länken. Dela inte länken om materialet
är upphovsrättsskyddat.

---

## 12. Använda materialet på en annan dator

Här behövs **bara Git** — inte Python, Ollama eller skripten.

**Engångsinstallation:**
```
git clone https://github.com/Pykarn/KTH-kod.git
cd KTH-kod
```

**Varje gång du vill ha senaste materialet:**
```
cd KTH-kod
git pull
```

Alternativt öppnar du GitHub Pages-länken i webbläsaren och laddar ner
enskilda filer därifrån.

---

## 13. Felsökning

### `python` / `python3` / `pip` hittas inte
- Windows: installera om Python och kryssa i **Add python.exe to PATH**,
  öppna sedan en ny terminal.
- Prova det andra kommandot (`python3` i stället för `python` eller tvärtom).
- För pip: `python -m pip install requests pypdf`.

### "Set CANVAS_TOKEN first"
Du har inte satt token i den här terminalen. Kör kommandot från
[kapitel 4.2](#42-använd-token-miljövariabel-aldrig-i-filen) igen. Variabeln
gäller bara i terminalen där du satte den.

### `401 Unauthorized` från Canvas
Tokenet är fel, utgånget eller borttaget. Skapa ett nytt (kapitel 4.1).

### `403 Forbidden` när skriptet hämtar filer
Files-fliken är troligen avstängd av läraren för kursen. Det är inget fel hos
dig — skriptet letar automatiskt på andra ställen (startsida, moduler, sidor,
uppgifter, anslag).

### "Nothing downloadable found anywhere for this course"
Kontrollera att kurs-ID:t i `COURSE_IDS` stämmer med adressen i Canvas och att
du är anmäld till kursen. Läraren kan också ha lagt allt som länkar till andra
sajter, vilka skriptet inte kan hämta.

### Skriptet hämtar inte om en fil jag raderat/ändrat
`canvas_download.py` hoppar över filer som redan finns i `canvas_downloads/`.
Vill du hämta allt på nytt, ta bort kursens mapp i `canvas_downloads/` (eller
hela mappen) och kör skriptet igen.

### `Ollama is not reachable ...`
Ollama körs inte. Starta Ollama-appen, eller kör `ollama serve` i en
separat terminal och försök igen. Under tiden sorteras filerna med enkla
nyckelord (sämre träffsäkerhet).

### `Model 'llama3.2' not found`
Du har inte hämtat modellen. Kör `ollama pull llama3.2` (eller den modell du
satt i `OLLAMA_MODEL`).

### Sorteringen går mycket långsamt
Första filen tar längst tid eftersom modellen laddas in i minnet. Är det
fortfarande långsamt: använd en mindre modell (`llama3.2`) eller stäng
`USE_PDF_PREVIEW`.

### `[skip] canvas_downloads/XXXX not found`
Kursen står i `COURSES` men det finns ingen mapp med det namnet i
`canvas_downloads/`. Kontrollera stavningen (samma i båda filerna) och att
`canvas_download.py` har körts för kursen.

### Terminalen ber om användarnamn/lösenord vid `git push`
Välj **"Sign in with your browser"** och följ instruktionerna. Behövs bara en
gång per dator.

### GitHub blockerar push p.g.a. "secrets" (t.ex. AWS-nycklar)
Någon nedladdad fil (ofta från ett GitHub-repo som en lärare länkat) innehåller
något som ser ut som en hemlig nyckel. Städa historiken:

```powershell
# Windows (PowerShell)
git reset --soft origin/main
git reset
Remove-Item -Recurse -Force .\canvas_downloads -ErrorAction SilentlyContinue
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' } | Remove-Item
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```
```bash
# macOS / Linux
git reset --soft origin/main
git reset
rm -rf canvas_downloads
find KTH_KOD -type f \( -regex '.*/[0-9]+' -o -name download -o -name preview \) -delete
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```
Kör sedan `canvas_download.py` och `organize_and_build_site.py` igen för att
fylla på. Om GitHub fortfarande klagar pekar felmeddelandet ut exakt vilken
fil som innehåller nyckeln — ta bort just den filen.

### Jag har klistrat in mitt Canvas-token någonstans synligt
Återkalla det direkt: Canvas → Settings → Approved Integrations → papperskorgen
→ skapa ett nytt.

---

## 14. Säkerhet och upphovsrätt

- Håll repot **privat** (Settings → Danger Zone → Change visibility).
  Tentor, föreläsningsanteckningar och kurslitteratur är oftast
  upphovsrättsskyddat och ska inte spridas offentligt.
- Dela aldrig ditt Canvas-token och spara det aldrig i en fil som
  committas till Git.
- Se till att `canvas_downloads/` står i `.gitignore` (kapitel 3.6).
- Kontrollera alltid vad som följer med (`git status`) innan du pushar.
