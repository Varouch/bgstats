# Deskovky – statistiky

Statický web se statistikami odehraných deskových her z aplikace [BG Stats](https://www.bgstatsapp.com/), celkově i podle lokalit.

## Aktualizace dat

1. V BG Stats exportujte data (JSON) a uložte `BGStatsExport-*.json` do této složky.
2. Spusťte `python build.py` – vygeneruje `data.js` (bez e-mailu a dalších údajů z exportu).
3. Commitněte a pushněte `data.js`; GitHub Pages se aktualizuje samo.

Surové exporty jsou v `.gitignore` a do repozitáře se nedostanou.
