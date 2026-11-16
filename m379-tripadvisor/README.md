# M379 · Tripadvisor-Auswertung für die Quartiera AG

Auswertung von 5'000 Hotelbewertungen mit dem KI-Werkzeug **JEV** (TypeSafe) für drei Entscheide der Geschäftsleitung.

## Abgaben

| Abgabe | Datei |
|---|---|
| 1 Konzept | [`01_Konzept.md`](01_Konzept.md) |
| 2 Notebook **eigenständig** (eine Datei, direkt in Jupyter) | [`notebook/M379_Tripadvisor_Standalone.ipynb`](notebook/M379_Tripadvisor_Standalone.ipynb) |
| 2 Notebook (Variante mit `src/`-Modulen) | [`notebook/M379_Tripadvisor_Auswertung.ipynb`](notebook/M379_Tripadvisor_Auswertung.ipynb) |
| 3 Management Summary + 3 Grafiken | [`02_Management_Summary.md`](02_Management_Summary.md), [`output/`](output/) |
| 3 Präsentation (Ablauf 10 Min.) | [`03_Praesentation.md`](03_Praesentation.md) |
| Reflexion | [`04_Reflexion.md`](04_Reflexion.md) |

## Ergebnisse in drei Sätzen

1. **Budget:** Zwei von drei unzufriedenen Gästen stört **Personal & Service** (66 %, Bandbreite 54–73 %). Dahinter folgen der Zustand der Zimmer (62 %) und die Sauberkeit (51 %).
2. **Teilnoten:** Service wird heute nicht abgefragt, kostet aber 0.38 Sterne über die 5 Teilnoten hinaus. Empfehlung: Teilnote «Personal & Service» einführen.
3. **KI:** JEV erreicht F1 = 0.86 gegenüber 0.64 mit Stichwörtern und ist stabil (6 von 3'400 Entscheiden kippen). Empfehlung: Pilot mit Weiterleitung nach Thema und Sternen und regelmässiger Kontrolle.

## Ordner

```
data/      sample_5000.csv          erste 5'000 Bewertungen, bereinigt + pseudonymisiert (ohne user_id/hotel_id)
           bereinigungsprotokoll.csv
           jev_results.csv          JEV-Antworten (Wahrscheinlichkeit 0–1 pro Thema)
           jev_rerun_200.csv        zweiter Durchlauf (Stabilitätstest)
           gold_sample_100_texts.csv  Kontrollstichprobe (Texte)
           gold_100_claude.csv      Referenz-Codierung (KI-Werkzeug Claude, von euch zu prüfen)
           gold_100_eure_kontrolle.csv  ← HIER codiert ihr selbst (1/0 pro Thema)
src/       codebook.py   Themen + JEV-Fragen
           privacy.py    Namen/E-Mail/Telefon maskieren
           prepare.py    Stichprobe + Datenqualität
           run_jev.py    JEV-Aufruf (mit Cache)
           analysis.py   alle Kennzahlen + Grafiken
           build_notebook.py
output/    3 Grafiken (PNG) + Ergebnistabellen (CSV)
```

## Selbst ausführen

```bash
pip install typesafe-sdk pandas pyarrow matplotlib statsmodels jupyter
```

```bash
cd notebook && jupyter notebook M379_Tripadvisor_Auswertung.ipynb
```

JEV neu befragen (optional, ca. 20 Rappen): `TYPESAFE_API_KEY` als Umgebungsvariable setzen und im Notebook `RUN_JEV = True` wählen. Den Key **nie** ins Notebook oder ins Repo schreiben.

Rohdaten neu erzeugen: Parquet von `huggingface.co/datasets/jniimi/tripadvisor-review-rating` laden, dann:

```bash
python src/prepare.py <pfad/zu/train.parquet> data/sample_5000.csv
```

## ⚠️ Vor der Abgabe von Hand erledigen

- [ ] Mindestens 30 Bewertungen in `data/gold_100_eure_kontrolle.csv` selbst codieren und Kapitel 9 im Notebook laufen lassen. Die Referenz stammt bisher von einer KI.
- [ ] Die Reflexion mit euren eigenen Erfahrungen ergänzen.
- [ ] Den TypeSafe-API-Key am Ende des Moduls in der Konsole neu erstellen. Der alte stand im Chat.
