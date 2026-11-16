# Reflexion: Was hat sich gegenüber dem Konzept geändert, und warum?

*Entwurf. Bitte mit euren eigenen Erfahrungen ergänzen, besonders nach eurer Handkontrolle.*

| Konzept | Umsetzung | Warum |
|---|---|---|
| `hotel_id` für die Weiterleitung an Hotels nutzen | nicht möglich | `hotel_id` ist pro Bewertung eindeutig (201'295 verschiedene Werte). Erst beim Prüfen der Datenqualität entdeckt. |
| Unsicher, ob «die ersten 5'000» verzerrt sind | Sternverteilung verglichen, praktisch identisch | Die Vorgabe der Lehrperson ist vertretbar, mit Beleg. |
| Themen klar getrennt | Themen überschneiden sich (Klima ↔ Zustand, Rechnung ↔ Preis) | Viele «Fehler» von JEV sind eigentlich Unschärfen im Codebuch. Nächstes Mal pro Thema festhalten, was **nicht** dazugehört (JEV-Doku: strukturierte Kriterien). |
| «Irgendeine Beschwerde» als Kriterium für die Weiterleitung | ungeeignet | Auch 35 % der 5-Sterne-Texte enthalten Kritik. Besser Thema + Sterne oder eine Score-Frage zum Schweregrad. |
| Kontrollstichprobe von Menschen codiert | zuerst von einem KI-Werkzeug (Claude) codiert | Aus Zeitgründen. Muss durch eine menschliche Codierung von ≥ 30 Bewertungen bestätigt werden (Notebook, Kapitel 9). |
| Pseudonymisierung | funktioniert nur teilweise | Vornamen ohne Anrede werden nicht erkannt. Darum keine Zitate ohne Kontrolle von Hand. |

**Was wir gelernt haben:** Eine KI liefert schnell Zahlen, aber erst die Prüfung (Kontrollstichprobe, Plausibilität mit den Teilnoten, zweiter Durchlauf) macht daraus Zahlen, denen man glauben kann.
