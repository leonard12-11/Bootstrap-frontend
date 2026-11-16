# Konzept: Kundenbewertungen auswerten (Quartiera AG)

Modul 379 · Data-Team · Abgabe 1 von 3

## 1. Fragestellung

Die Geschäftsleitung muss drei Entscheide treffen. Für jeden übersetzen wir den Entscheid in eine Frage, die sich mit Daten beantworten lässt, und eine Kennzahl (Trichter «Entscheid → Argumente → Resultate → Methode → Daten → Frage», B.10.I).

| Entscheid | Frage an die Daten | Kennzahl | Woraus |
|---|---|---|---|
| **E1** CHF 500'000 Coaching: wohin? | Welche Themen nennen unzufriedene Gäste (1–2 Sterne) am häufigsten? | Anteil der Unzufriedenen pro Thema, mit Bandbreite; Faktor unzufrieden/zufrieden | Text |
| **E2** Richtige Teilnoten? | Welche Themen kosten Sterne, obwohl die 5 Teilnoten sie nicht zeigen? | Zusätzlicher Sterne-Abzug pro Thema bei gleichen Teilnoten (Regression), Häufigkeit | Text und Noten |
| **E3** Automatische Auswertung? | Wie oft erkennt das KI-Werkzeug eine Beschwerde richtig, und wo irrt es? | Trefferquote, Präzision, F1, Stabilität, Anteil «unsicher» | Text und Kontrollstichprobe |

## 2. Die Daten (HZ 1)

- **Quantitativ (ordinal 1–5):** `overall`, `cleanliness`, `value`, `location`, `rooms`, `sleep_quality`. Damit lässt sich sagen, *dass* und *wie stark* etwas schlecht war.
- **Qualitativ:** `title`, `text`. Nur hier steht, *warum*. Beispiel: Ein Gast gibt 1 Stern, aber keine Teilnote erfasst «Valet machte eine Spritztour mit meinem Auto».
- **Kennungen und Metadaten:** `user_id` (Pseudonym), `hotel_id`, `post_date`, `char`, `lang`.
- **Stichprobe:** gemäss Vorgabe die ersten 5'000 von 201'295 Zeilen. Vorher prüfen wir, ob diese Auswahl verzerrt ist (Vergleich der Sternverteilung mit dem Gesamtdatensatz).

## 3. Datenqualität (HZ 2)

| Prüfung | Vorgehen | Entscheid |
|---|---|---|
| Fehlende Werte | `isna()` pro Spalte | protokollieren, keine Imputation |
| Duplikate | gleicher Text | entfernen, erste Zeile behalten |
| Unmögliche Werte | Noten ausserhalb 1–5 | entfernen |
| Ausreisser | sehr kurze (< 50 Zeichen) und sehr lange Texte | behalten, markieren |
| Schiefe Verteilung | 76 % geben 4–5 Sterne | Unzufriedene separat auswerten, nicht nur den Durchschnitt |
| Kennungen | ist `hotel_id` wirklich ein Hotel? | prüfen (`nunique`) |

Alle Annahmen und Entscheide kommen in ein **Bereinigungsprotokoll** (Problem, Anzahl Zeilen, Entscheid, Begründung).

## 4. Vom Text zur Zahl (HZ 1 + 2)

- **Methode:** Das KI-Werkzeug **JEV** (TypeSafe). Pro Bewertung stellen wir in *einer* Anfrage 17 Ja/Nein-Fragen (Noul): «irgendeine Beschwerde» und 16 Themen aus einem Codebuch, z.B. Personal & Service, Sauberkeit, Zustand, Lärm, Preis, Check-in, Frühstück, WLAN, Parkieren.
- **Codebuch:** Wir lesen zuerst 20 Bewertungen von Hand und leiten daraus die Themen ab. Jedes Thema bekommt eine eng formulierte Frage und den Vermerk, welche Teilnote es heute abdeckt.
- **Rollen:** JEV beurteilt nur. Zählen, Prozente, Intervalle und Tests rechnet unser Python-Code («Code rechnet, KI interpretiert, wir prüfen beides»).
- **Schwellen:** ≥ 0.7 ja, ≤ 0.3 nein, dazwischen unsicher (Empfehlung der JEV-Doku).
- **Vergleich:** eine einfache Stichwort-Methode (Regex) als Baseline.

## 5. Überprüfung (HZ 3)

1. **Kontrollstichprobe:** 100 Bewertungen, geschichtet (50 × 1–2, 25 × 3, 25 × 4–5 Sterne), unabhängig codiert, *bevor* wir die JEV-Resultate anschauen. Daraus berechnen wir eine Confusion-Matrix, Präzision und Trefferquote pro Thema.
2. **Plausibilität:** Wenn JEV «Sauberkeit» meldet, muss die Sauberkeits-Note tiefer sein.
3. **Stabilität:** 200 Bewertungen zweimal abfragen und zählen, wie viele Entscheide kippen.
4. **Ehrliche Bandbreiten:** 95 %-Wilson-Intervalle, kombiniert mit der KI-Unsicherheit (nur sichere Ja bis alles ausser sichere Nein).

## 6. Ethik und Recht (HZ 4)

- **Personendaten:** `user_id` (pseudonymisiert, aber personenbezogen) und Namen von Mitarbeitenden in Texten. ➜ `user_id` löschen, Namen, E-Mails und Telefonnummern maskieren, *bevor* Daten den Computer verlassen. Keine Namen im Report.
- **Externer Dienst:** JEV läuft bei TypeSafe (USA). Laut Doku gibt es einen Auftragsverarbeitungsvertrag (DPA) und kein Training auf Kundendaten, Zero-Data-Retention nur für Enterprise. Für Übungsdaten (öffentlich, pseudonymisiert) vertretbar. Für echte Quartiera-Daten braucht es einen DPA und eine Prüfung nach nDSG.
- **Herkunft und Lizenz:** Hugging Face `jniimi/tripadvisor-review-rating` (Apache-2.0), ursprünglich Li et al. (2013, CMU), Inhalte von Tripadvisor. Für den Unterricht in Ordnung. Für kommerzielle Nutzung müssten die Tripadvisor-Nutzungsbedingungen geklärt werden.
- **API-Key** nur als Umgebungsvariable, nie im Code oder Repo.

## 7. Der Report (HZ 5)

| Grafik | Zeigt | Entscheid |
|---|---|---|
| 1 Balken: «Was stört unzufriedene Gäste?» | Anteil pro Thema + Bandbreite, Farbe = abgefragt ja/nein | E1 (+ E2) |
| 2 Balken: «Was die Teilnoten übersehen» | Sterne-Abzug pro Thema bei gleichen Teilnoten | E2 |
| 3 Gestapelte Balken: «Wie zuverlässig ist die KI?» | erkannt / übersehen / Fehlalarm pro Thema | E3 |

Unsicherheit kommunizieren wir in Worten: «zwei von drei (zwischen 54 und 73 %)» statt «66.26 %».

## 8. Plan

| Schritt | Werkzeug | Ergebnis |
|---|---|---|
| 1 Daten laden, Stichprobe, Qualität | Python/pandas | `sample_5000.csv`, Protokoll |
| 2 Pseudonymisieren | Python/Regex | maskierte Texte |
| 3 Codebuch + 20 Texte lesen | Excel/Notebook | 16 Themen |
| 4 Kontrollstichprobe codieren | Excel | `gold_100_*.csv` |
| 5 JEV-Lauf | typesafe-sdk | `jev_results.csv` |
| 6 Prüfen (Kap. 5) | Python/statsmodels | Kennzahlen E3 |
| 7 Auswerten E1/E2 | Python | Tabellen + Grafiken |
| 8 Summary, Präsentation, Reflexion | Markdown/PowerPoint | Abgabe 3 |
