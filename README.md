# KTH-kod — Canvas-material, automatiskt sorterat

Det här repot hämtar filer (föreläsningar, tentor, litteratur, övningar) från
Canvas automatiskt, sorterar dem med en lokal AI, och gör dem tillgängliga
här på GitHub — både för nedladdning via `git pull` och som en webbsida via
GitHub Pages.

**Mappstruktur:**
```
KTH-kod/
├── canvas_download.py          <- hämtar filer från Canvas
├── organize_and_build_site.py  <- sorterar filer + bygger webbsidan
├── KTH_KOD/                    <- dina kurser, en mapp per kurs
│   ├── EL1000/
│   │   ├── exam/
│   │   ├── lecture/
│   │   ├── exercise/
│   │   ├── literature/
│   │   └── index.html
│   └── ...
└── canvas_downloads/           <- tillfällig arbetsmapp (committas ALDRIG)
```

---

## 1. Engångsinstallation (görs en gång per dator)

### 1.1 Installera Python
- Ladda ner från **python.org/downloads**, kör installationen.
- **Windows:** kryssa i "Add python.exe to PATH" under installationen.
- Kontrollera i en terminal:
  ```
  python3 --version
  ```

### 1.2 Installera Git
- Ladda ner från **git-scm.com/downloads**, installera med standardval.
- Kontrollera:
  ```
  git --version
  ```

### 1.3 Installera Ollama (lokal AI, bara på huvuddatorn)
- Ladda ner från **ollama.com/download**, installera.
- Hämta en modell:
  ```
  ollama pull llama3.2
  ```
- Ollama körs automatiskt i bakgrunden efter installation.

**OBS:** Ollama behövs bara på datorn där du kör `organize_and_build_site.py`.
På din andra dator, där du bara hämtar färdiga filer, behövs varken Python,
Ollama eller skripten — bara Git.

### 1.4 Klona repot
```
git clone https://github.com/Pykarn/KTH-kod.git
cd KTH-kod
```

### 1.5 Installera Python-paketet som behövs
```
pip install requests
```

---

## 2. Canvas-token

1. Logga in på **canvas.kth.se** → profilbild → **Settings**.
2. Scrolla till **Approved Integrations** → **+ New Access Token**.
3. Ge den ett namn, generera, **kopiera direkt** (visas bara en gång).

**Spara ALDRIG token direkt i filen `canvas_download.py`.** Sätt den istället
som miljövariabel varje gång du öppnar en ny terminal:

```powershell
$env:CANVAS_TOKEN = "ditt-token-här"
```

Om token någonsin hamnar i en fil, chatt, eller committas till Git —
återkalla den direkt i Canvas (samma meny, papperskorg-ikonen) och skapa en ny.

---

## 3. Lägg till/ändra kurser

Öppna `canvas_download.py` och redigera:

```python
COURSE_IDS = {
    "EL1000": 64209,
    "DD1385": 63900,
    "SF1930": 65047,
}
```

- Namnet till vänster = mappnamnet i `KTH_KOD/` (du väljer själv).
- Numret till höger = kurs-ID, hittas i webbadressen när du öppnar kursen i
  Canvas: `canvas.kth.se/courses/64209` → ID är `64209`.

---

## 4. Köra en synk (huvuddatorn)

```powershell
$env:CANVAS_TOKEN = "ditt-token-här"
python3 canvas_download.py
python3 organize_and_build_site.py
```

Det här:
1. Hämtar filer från Canvas Files-fliken OM den är påslagen.
2. Söker samtidigt igenom startsidan, moduler, sidor, uppgifter, anslag och
   kursplan efter fler filer och GitHub-länkar (laddar ner hela repon om de
   hittas).
3. Sorterar allt med den lokala AI:n i `exam/`, `lecture/`, `exercise/`,
   `literature/` eller `other/` inuti `KTH_KOD/<kurs>/`.
4. Bygger `index.html`-sidor så materialet går att bläddra/ladda ner via
   webbläsare.

---

## 5. Kontrollera innan du pushar (VIKTIGT)

Ibland fastnar konstiga filer utan riktiga filnamn (bara siffror, eller
`download`/`preview`) — dessa är skräp från länksökningen, inte riktigt
kursmaterial, och kan ibland innehålla känslig data. Kör alltid:

```powershell
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' }
```

Om listan inte är tom, ta bort dem:
```powershell
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' } | Remove-Item
```

---

## 6. Pusha till GitHub

```powershell
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```

Om GitHub blockerar pushen p.g.a. "secrets" (t.ex. AWS-nycklar i någon fil):
se **Felsökning** längst ner.

---

## 7. Använda på en annan dator

**Engångsinstallation** (bara Git behövs, inget annat):
```
git clone https://github.com/Pykarn/KTH-kod.git
cd KTH-kod
```

**Varje gång du vill ha senaste materialet:**
```
git pull
```

Du behöver **inte** installera Python, Ollama eller köra några skript på den
andra datorn — den hämtar redan färdigsorterat material.

Alternativt: öppna GitHub Pages-länken i webbläsaren och ladda ner enskilda
filer därifrån (se avsnitt 8).

---

## 8. GitHub Pages (webbsida med nedladdningslänkar)

1. Gå till **github.com/Pykarn/KTH-kod** → **Settings** → **Pages**.
2. Under "Build and deployment": välj **Deploy from a branch**.
3. Branch: `main`, mapp: `/KTH_KOD`.
4. Spara. Efter ~1 minut visas länken, t.ex.:
   ```
   https://pykarn.github.io/KTH-kod/
   ```

**Notera:** Om repot är privat är Pages-sidan ändå nåbar av alla som har
exakt länken. Dela den inte offentligt om materialet är upphovsrättsskyddat.

---

## 9. Regelbunden uppdatering (rutin)

Kör detta på huvuddatorn när du vill uppdatera:

```powershell
$env:CANVAS_TOKEN = "ditt-token-här"
python3 canvas_download.py
python3 organize_and_build_site.py
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' }
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```

Kör sedan `git pull` på din andra dator.

---

## Felsökning

### "403 Forbidden" när skriptet hämtar filer
Files-fliken är troligen avstängd av läraren för den kursen. Inget fel hos
dig — skriptet letar automatiskt på andra ställen (startsida, moduler,
sidor) istället.

### Terminalen ber om användarnamn/lösenord vid `git push`
Välj **"Sign in with your browser"** när alternativen dyker upp, följ
instruktionerna i webbläsaren. Behövs bara en gång per dator.

### GitHub blockerar push p.g.a. "secrets" (t.ex. AWS-nycklar)
```powershell
git reset --soft origin/main
git reset
Remove-Item -Recurse -Force .\canvas_downloads -ErrorAction SilentlyContinue
Get-ChildItem -Path .\KTH_KOD -Recurse -File | Where-Object { $_.Name -match '^\d+$' -or $_.Name -eq 'download' -or $_.Name -eq 'preview' } | Remove-Item
git add .
git commit -m "Uppdaterar kursmaterial"
git push
```
Kör sedan `python3 canvas_download.py` och `organize_and_build_site.py` igen
för att fylla på med rena filer.

### Jag råkade klistra in mitt Canvas-token någonstans synligt
Återkalla det direkt: Canvas → Settings → Approved Integrations →
ta bort tokenet → skapa ett nytt.

---

## Säkerhet & upphovsrätt

- Håll repot **privat** (Settings → Danger Zone → Change visibility).
  Tentor, föreläsningsanteckningar och kurslitteratur är oftast
  upphovsrättsskyddat och ska inte spridas offentligt.
- Dela aldrig ditt Canvas-token med någon, och spara det aldrig i en fil som
  committas till Git.
