# Management Summary: Was stört unsere Gäste wirklich?

An die Geschäftsleitung der Quartiera AG · Data-Team · Basis: 5'000 Tripadvisor-Bewertungen (2012), davon 492 unzufriedene Gäste (1–2 Sterne)

## Zusammenfassung (5 Sätze)

1. Zwei von drei unzufriedenen Gästen beschweren sich über **Personal & Service** (66 %, ziemlich sicher zwischen 54 und 73 %). Damit ist es das häufigste Thema, noch vor dem Zustand der Zimmer (62 %) und der Sauberkeit (51 %).
2. Genau dieses Thema fragen wir heute **nicht** ab: Wer Service-Probleme erwähnt, gibt bei gleichen Teilnoten rund **0.4 Sterne weniger**.
3. Das KI-Werkzeug JEV erkennt Beschwerde-Themen deutlich besser als eine Stichwortsuche: 91 % der Beschwerden findet es, 81 % seiner Meldungen stimmen (Stichwörter: 67 % und 61 %). Es antwortet auch beim zweiten Mal fast immer gleich.
4. JEV irrt vor allem dort, wo sich Themen überschneiden (defekte Klimaanlage als «Zustand» **und** «Klima») und wo Kritik nur indirekt formuliert ist (Lage, Reservationsfehler).
5. Wir empfehlen: das Coaching-Budget auf Service und Beschwerdemanagement konzentrieren, eine Teilnote «Personal & Service» einführen und die automatische Auswertung in einem 3-monatigen Pilot mit monatlicher Stichprobenkontrolle starten.

## Empfehlungen

| Entscheid | Empfehlung | Begründung mit Zahlen | Sicherheit |
|---|---|---|---|
| **1 Qualitätsbudget** | Den Grossteil der CHF 500'000 in **Service- und Beschwerde-Coaching** stecken (Front Desk, Umgang mit Problemen), den Rest in **Housekeeping-Standards** | Service: 66 % der Unzufriedenen, aber nur 6 % der Zufriedenen (11× häufiger). Sauberkeit: 51 % (24× häufiger). Den Zustand der Zimmer (62 %) löst ein Coaching kaum, das ist ein Investitionsthema. | ziemlich sicher bei der Reihenfolge, die genaue Aufteilung ist eine Einschätzung |
| **2 Teilnoten** | Teilnote **«Personal & Service»** ergänzen. WLAN, Parkieren und Frühstück nicht zusätzlich abfragen. | Service kostet 0.38 Sterne (0.33–0.44) über die 5 Teilnoten hinaus und kommt in 16 % aller Bewertungen vor. WLAN, Parkieren und Frühstück: unter 0.06 Sterne, statistisch nicht gesichert. | sicher für Service, unsicher für kleine Themen |
| **3 Automatische Auswertung** | **Ja, als Pilot.** Weiterleiten nach Thema und Sternen (nicht jede «Beschwerde»), unsichere Fälle an einen Menschen. Zuordnung zum Hotel über die Buchungs-ID. | F1 = 0.86 (Stichwörter 0.64), 6 von 3'400 Entscheiden kippen beim zweiten Durchlauf, höchstens 13 % pro Thema «unsicher». Aber: 35 % der 5-Sterne-Bewertungen enthalten eine kleine Kritik. | mittel: Die Referenz ist noch nicht vollständig von Menschen codiert |

## Was die Daten nicht beantworten können

- Ob die Probleme in **unseren Partnerhotels** gleich verteilt sind: Die Daten stammen aus den USA, sind von 2012 und auf Englisch.
- **Welches Hotel** betroffen ist: Die Hotel-ID im Datensatz ist pro Bewertung eindeutig.
- Ob ein Coaching die Noten **tatsächlich verbessert**: Wir sehen einen Zusammenhang, keine Ursache. Das zeigt nur ein Pilot mit Vorher-Nachher-Messung.
- Was **stille Gäste** denken: Nur ein Teil der Gäste schreibt eine Bewertung, und das eher, wenn sie sehr zufrieden oder sehr unzufrieden sind.

## Datenschutz und Herkunft

Datensatz: Hugging Face `jniimi/tripadvisor-review-rating` (Apache-2.0, ursprünglich Li et al. 2013). Gäste-Kennungen wurden vor der Auswertung gelöscht, Namen, E-Mails und Telefonnummern maskiert. Im Report stehen keine Namen von Gästen oder Mitarbeitenden. JEV (TypeSafe, USA) trainiert gemäss eigener Erklärung nicht mit Kundendaten. Für echte Quartiera-Daten braucht es vorher einen Auftragsverarbeitungsvertrag und eine Prüfung nach nDSG.

## Grafiken

1. `output/grafik1_themen_unzufriedene.png`: Was stört unzufriedene Gäste?
2. `output/grafik2_teilnoten_luecken.png`: Was die Teilnoten übersehen
3. `output/grafik3_ki_zuverlaessigkeit.png`: Wie zuverlässig ist die KI?
