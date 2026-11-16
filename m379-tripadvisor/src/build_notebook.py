"""Erzeugt notebook/M379_Tripadvisor_Auswertung.ipynb (danach mit nbconvert ausfuehren)."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s.strip()))
py = lambda s: C.append(nbf.v4.new_code_cell(s.strip()))

md("""
# Modul 379 · Quartiera AG: Was stört unsere Gäste wirklich?

**Ziel:** Mit 5'000 Tripadvisor-Bewertungen drei Entscheide der Geschäftsleitung beantworten.

| # | Entscheid | Frage an die Daten | Kennzahl |
|---|---|---|---|
| 1 | Wohin fliessen CHF 500'000 Coaching-Budget? | Welche Themen nennen unzufriedene Gäste (1–2 Sterne) am häufigsten? | Anteil der unzufriedenen Gäste pro Thema, mit Bandbreite |
| 2 | Fragen wir die richtigen Teilnoten ab? | Welche Themen kosten Sterne, obwohl die 5 Teilnoten sie nicht abbilden? | Zusätzlicher Sterne-Abzug pro Thema (Regression) |
| 3 | Texte automatisch auswerten? | Wie gut erkennt JEV Beschwerden, und wo irrt es sich? | Trefferquote, Präzision, Stabilität, Vergleich mit Stichwort-Methode |

**Vorgehen (hybride Pipeline aus dem Unterricht):** Code bereitet vor → KI (JEV) interpretiert → Code prüft und rechnet → Mensch entscheidet.

Das Notebook liest zwischengespeicherte JEV-Antworten (`data/jev_results.csv`). Den API-Aufruf startet ihr nur neu, wenn ihr `RUN_JEV = True` setzt.
""")

py("""
import sys, os
sys.path.insert(0, os.path.abspath("../src"))
import pandas as pd, numpy as np
from IPython.display import Image, display
pd.set_option("display.width", 160); pd.set_option("display.max_columns", 20)
import codebook, analysis
from analysis import *
""")

md("""
## 1 · Daten kennenlernen (HZ 1)

Quelle: *TripAdvisor Review Rating* (Hugging Face `jniimi/tripadvisor-review-rating`, Lizenz Apache-2.0, ursprünglich Li et al. 2013).
201'295 englische Hotelbewertungen aus dem Jahr 2012. Vorgabe: Wir nehmen die **ersten 5'000 Zeilen**.

| Spalte | Art | Bedeutung |
|---|---|---|
| `overall` | quantitativ, ordinal (1–5) | Gesamtnote in Sternen |
| `cleanliness`, `value`, `location`, `rooms`, `sleep_quality` | quantitativ, ordinal (1–5) | die 5 Teilnoten |
| `title`, `text` | **qualitativ** (Freitext) | Nur hier steht, *warum* ein Gast unzufrieden ist |
| `user_id` | Kennung (Pseudonym) | Personendatum → wird entfernt |
| `hotel_id` | Kennung | ⚠️ ist **pro Zeile eindeutig**, also keine echte Hotel-ID |
| `post_date`, `stay_year`, `char`, `lang`, `freq` | Metadaten | Datum, Jahr, Länge, Sprache |

Sterne und Teilnoten zeigen, **dass** etwas schlecht war, aber nur der Text sagt, **warum**.
""")

py("""
s = pd.read_csv("../data/sample_5000.csv")
print(s.shape)
s[["overall","cleanliness","value","location","rooms","sleep_quality","char"]].describe().round(2)
""")

md("""
**Ist die Stichprobe «die ersten 5'000» verzerrt?** Ein Vergleich mit dem Gesamtdatensatz (201'295 Zeilen) zeigt dieselbe Verteilung der Sterne:

| Sterne | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| alle 201'295 | 4.0 % | 5.4 % | 14.0 % | 33.6 % | 43.0 % |
| erste 5'000 | 4.1 % | 5.7 % | 13.8 % | 33.7 % | 42.7 % |

Der Datensatz ist nicht nach Hotel oder Note sortiert. Die ersten 5'000 sind deshalb für unsere Zwecke vertretbar.
""")

py("""
s.overall.value_counts(normalize=True).sort_index().round(3)
""")

md("""
## 2 · Datenqualität (HZ 2)

Geprüft mit `src/prepare.py`: fehlende Werte, Duplikate, unmögliche Werte, Ausreisser (sehr kurze Texte).
Das Protokoll hält fest, wie viele Zeilen betroffen sind und was wir entschieden haben.
""")

py("""
pd.read_csv("../data/bereinigungsprotokoll.csv")
""")

md("""
**Annahmen, die wir festhalten:**
- Im Gesamtdatensatz gibt es 40 doppelte Texte. In den ersten 5'000 Zeilen kommt keiner davon vor.
- Die Sternverteilung ist schief (76 % geben 4–5 Sterne). Das ist normal für Bewertungsportale. Darum werten wir die unzufriedenen Gäste **separat** aus und nicht im Durchschnitt aller Gäste.
- Sehr lange Texte (bis 22'000 Zeichen) behalten wir. JEV verarbeitet bis 32'000 Tokens pro Frage.
""")

md("""
## 3 · Datenschutz vor dem Versand (HZ 4)

- `user_id` und `hotel_id` werden **nicht** gespeichert und nicht verschickt.
- Namen nach Anrede oder «named …», E-Mail-Adressen und Telefonnummern werden maskiert (`src/privacy.py`).
- **Grenze:** Vornamen ohne Anrede (z.B. «thanks to Maria») erkennt die Regel nicht. Darum verwenden wir im Report **keine Zitate**, die nicht von Hand kontrolliert sind.
""")

py("""
from privacy import mask
beispiel = "The night manager Mr Smith was rude, call him at +1 312 555 0199 or smith@hotel.com"
print(mask(beispiel))
print("Bewertungen mit Maskierung:", int(s.masked_changes.sum()))
""")

md("""
## 4 · Vom Text zur Zahl: das Codebuch für JEV (HZ 1 + 2)

JEV (TypeSafe) beantwortet **Noul-Fragen**: Für jede Aussage liefert es eine Wahrscheinlichkeit von 0 bis 1, dass sie stimmt.
Pro Bewertung stellen wir 17 Fragen in **einer** Anfrage: 1× «irgendeine Beschwerde» und 16 Themen.

Regeln aus der JEV-Doku, die wir umsetzen:
- Fragen eng und wörtlich formulieren (JEV liest wörtlich).
- Zählen und Rechnen macht der Code, nicht JEV.
- Schwellen: ≥ 0.7 = ja, ≤ 0.3 = nein, dazwischen = **unsicher**. Für Zählungen verwenden wir 0.5 und zeigen die Unsicherheit als Bandbreite.

Spalte «Teilnote» = welche der 5 heutigen Teilnoten das Thema abdeckt (leer = wird heute nicht abgefragt).
""")

py("""
pd.DataFrame([(k, v[0], v[1] or "– nicht abgefragt –", v[2]) for k, v in codebook.THEMES.items()],
             columns=["Code", "Thema", "Teilnote", "Frage an JEV"])
""")

md("""
### JEV aufrufen (nur bei Bedarf)

Kosten des vollen Laufs: ca. 4.6 Mio. Tokens × $0.042 pro Mio. = **ca. 20 Rappen**. Dauer: ein paar Minuten.
Der API-Key kommt aus der Umgebungsvariable `TYPESAFE_API_KEY` und steht **nie** im Notebook.
""")

py("""
RUN_JEV = False   # auf True setzen, um JEV neu zu befragen
if RUN_JEV:
    assert os.environ.get("TYPESAFE_API_KEY"), "Bitte TYPESAFE_API_KEY setzen"
    !python ../src/run_jev.py ../data/sample_5000.csv ../data/jev_results.csv
df = load()
print(len(df), "Bewertungen mit JEV-Antworten")
df[["review_id","overall","title_masked","complaint","staff_service","cleanliness","noise"]].head(8)
""")

md("""
## 5 · Überprüfung: Stimmt die Methode? (HZ 3)

Bevor wir den Zahlen glauben, prüfen wir JEV auf vier Arten:

1. **Plausibilität mit den Teilnoten:** Wenn JEV «Sauberkeits-Beschwerde» meldet, muss die Sauberkeits-Note tiefer sein.
2. **Kontrollstichprobe:** 100 Bewertungen (50 mit 1–2, 25 mit 3, 25 mit 4–5 Sternen, zufällig, gemischt) wurden **unabhängig von JEV und vor dem Blick auf die JEV-Resultate** codiert. Diese Referenz hat das KI-Werkzeug Claude erstellt (siehe Grenzen). ➜ Vorlage `data/gold_100_eure_kontrolle.csv`: Prüft mindestens 30 davon selbst.
3. **Stabilität:** 200 Bewertungen ein zweites Mal an JEV geschickt.
4. **Vergleich mit einer einfachen Stichwort-Methode** (Regex), damit wir sehen, ob sich die KI lohnt.
""")

py("""
convergent_validity(df).round(2)
""")

md("""
➜ **Plausibel:** Bei jedem Thema ist die passende Teilnote deutlich tiefer, wenn JEV eine Beschwerde meldet.
Beispiel Sauberkeit: 2.3 statt 4.5 Sterne. JEV misst also, was es messen soll.
""")

py("""
d3, stab, tot, gold_merged = decision3(df)
cols = ["Thema","ref_ja","jev_TP","jev_FP","jev_FN","jev_praezision","jev_trefferquote","jev_f1","kw_f1","unsicher"]
d3[cols].round(2)
""")

py("""
print("Stabilität:", stab)
print(pd.DataFrame(tot).T[["praezision","trefferquote","f1","genauigkeit"]].round(2))
""")

md("""
**So liest man das:**
- *Trefferquote* = Von allen echten Beschwerden zu einem Thema: Wie viele findet JEV?
- *Präzision* = Von allen JEV-Meldungen: Wie viele stimmen?
- *F1* = Mittelwert aus beiden (1.0 = perfekt).

**Ergebnis:** Über alle 16 Themen erreicht JEV F1 = 0.86 (Präzision 81 %, Trefferquote 91 %). Die Stichwort-Methode schafft nur 0.64.
Im zweiten Durchlauf kippen nur 6 von 3'400 Entscheiden, und zwar alle nahe der 50 %-Grenze.

**Wo JEV sich irrt** (Fehler von Hand angeschaut):
- **Fehlalarme bei überlappenden Themen:** Eine defekte Klimaanlage zählt JEV auch als «Zustand defekt», Abrechnungsprobleme auch als «Preis», schlechte Reinigung auch als «Personal». Das ist oft eher eine Unschärfe im Codebuch als ein KI-Fehler.
- **Übersehen bei indirekten Aussagen:** «nicht viel in der Umgebung», «Polizei vor dem Haus» (Lage) oder «Nichtraucher-Zimmer versprochen, Raucherzimmer bekommen» (Reservation) erkennt JEV schlechter.
""")

py("""
complaint_by_stars(df).round(3)
""")

md("""
⚠️ **Wichtig für Entscheid 3:** «Irgendeine Beschwerde» steckt auch in 35 % der 5-Sterne-Bewertungen («super Hotel, nur das Frühstück war teuer»).
Wer *alles* weiterleitet, überflutet die Hotels. Weiterleiten sollte man nur nach **Thema + Sternen** (oder einem zusätzlichen Score für den Schweregrad).
""")

md("""
## 6 · Entscheid 1: Was stört unzufriedene Gäste am meisten?

Basis: alle 492 Bewertungen mit 1–2 Sternen. Die **Bandbreite** verbindet zwei Unsicherheiten:
- Stichprobenzufall (95 %-Wilson-Intervall)
- KI-Unsicherheit (untere Grenze: nur sichere Ja ≥ 0.7, obere Grenze: alles ausser sicheren Nein > 0.3)

«Faktor» = wie viel häufiger das Thema bei unzufriedenen als bei zufriedenen Gästen vorkommt.
""")

py("""
d1 = decision1(df)
d1[["Thema","Teilnote","anteil_unzufrieden","von","bis","anzahl","anteil_zufrieden","faktor"]].round(2)
""")

py("""
fig1(d1, "../output/grafik1_themen_unzufriedene.png")
display(Image("../output/grafik1_themen_unzufriedene.png", width=800))
""")

md("""
**Erkenntnis:** Zwei von drei unzufriedenen Gästen beklagen sich über **Personal & Service** (66 %, Bandbreite 54–73 %). Das ist das häufigste Thema, und es wird heute nicht abgefragt.
Danach folgen Zustand der Zimmer (62 %) und Sauberkeit (51 %). Coaching wirkt vor allem auf Verhalten und Abläufe (Service, Housekeeping, Beschwerdemanagement), weniger auf alte Bausubstanz.
""")

md("""
## 7 · Entscheid 2: Fragen wir die richtigen Teilnoten ab?

Regression: `overall ~ 5 Teilnoten (+ 16 Themen)`.
Die 5 Teilnoten allein erklären 78 % der Unterschiede in der Gesamtnote. Was übrig bleibt, zeigt, was die Teilnoten **übersehen**.
Der Koeffizient eines Themas sagt: So viele Sterne weniger gibt ein Gast, wenn er das Thema erwähnt, **bei gleichen Teilnoten**.
Robuste Standardfehler (HC3). Das ist ein Zusammenhang, keine bewiesene Ursache.
""")

py("""
d2, fit = decision2(df)
print({k: round(v, 3) if isinstance(v, float) else v for k, v in fit.items()})
d2[["Thema","Teilnote","sterne_effekt","von","bis","p_wert","anteil_alle"]].round(3)
""")

py("""
fig2(d2, "../output/grafik2_teilnoten_luecken.png")
display(Image("../output/grafik2_teilnoten_luecken.png", width=800))
""")

md("""
**Erkenntnis:** **Personal & Service** kostet zusätzlich 0.38 Sterne (Bandbreite 0.33–0.44, p < 0.001). Es kommt in 16 % aller Bewertungen vor und ist die grösste Lücke im heutigen Fragebogen.
Auch «Einrichtungen» zeigt einen klaren, aber kleinen Effekt (−0.11). Check-in, WLAN, Parkieren und Frühstück sind klein und statistisch nicht gesichert.
Ungeziefer hat zwar den grössten Effekt (−0.40), ist aber selten (0.9 %) und gehört bereits zur Sauberkeit.
""")

md("""
## 8 · Entscheid 3: Wie gut erkennt ein KI-Werkzeug Beschwerden?
""")

py("""
fig3(d3, "../output/grafik3_ki_zuverlaessigkeit.png")
display(Image("../output/grafik3_ki_zuverlaessigkeit.png", width=800))
""")

md("""
## 9 · Eure Handkontrolle (Pflicht vor der Präsentation)

Die Referenz für Kapitel 5 hat ein KI-Werkzeug (Claude) codiert. Für eine faire Prüfung muss **ein Mensch** mindestens 30 davon selbst codieren.
Öffnet `data/gold_100_eure_kontrolle.csv` (z.B. in Excel), tragt pro Thema 1/0 ein und lasst diese Zelle laufen.
""")

py("""
eure = pd.read_csv("../data/gold_100_eure_kontrolle.csv")
fertig = eure.dropna(subset=["complaint"])
print(len(fertig), "Bewertungen von euch codiert")
if len(fertig) >= 10:
    ref = pd.read_csv("../data/gold_100_claude.csv").set_index("review_id")
    j = df.set_index("review_id")
    rows = []
    for t in codebook.THEMES:
        y = fertig.set_index("review_id")[t].astype(int)
        rows.append(dict(Thema=codebook.LABEL[t],
                         uebereinstimmung_mit_Claude=(y == ref.loc[y.index, t]).mean(),
                         uebereinstimmung_mit_JEV=(y == (j.loc[y.index, t] >= .5).astype(int)).mean()))
    display(pd.DataFrame(rows).round(2))
""")

md("""
## 10 · Was die Daten NICHT beantworten können

- **Keine Hotel-Zuordnung:** `hotel_id` ist pro Bewertung eindeutig. Ob Beschwerden «beim richtigen Hotel landen», lässt sich mit diesen Daten nicht testen. Die Zuordnung muss über die Buchungs-ID erfolgen.
- **2012, USA, Englisch, Tripadvisor:** Die Gäste von Quartiera heute können anders sein. Die Ergebnisse sind ein Hinweis, kein Beweis für Partnerhotels.
- **Wer schreibt, ist nicht repräsentativ:** Sehr zufriedene und sehr unzufriedene Gäste schreiben häufiger.
- **Ursache vs. Zusammenhang:** Dass Service-Beschwerden mit tieferen Noten einhergehen, beweist nicht, dass ein Coaching die Note hebt. Das zeigt erst ein Pilot mit Vorher-Nachher-Messung.
- **Stichprobe:** 5'000 von 201'295 (492 unzufriedene). Seltene Themen (Ungeziefer: 46 Fälle) sind unsicher.
- **Referenz durch eine KI:** Die Kontrollstichprobe ist (noch) nicht von Menschen codiert, siehe Kapitel 9.
""")

nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "notebook/M379_Tripadvisor_Auswertung.ipynb")
print("ok")
