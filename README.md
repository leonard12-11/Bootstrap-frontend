SMART DASHBOARD & BEWERBUNGSFORMULAR
===================================

Dieses Projekt ist eine statische Website (HTML, CSS, JavaScript),
die mit Bootstrap, jQuery und Leaflet umgesetzt wurde.

-------------------------------------------------
DASHBOARD – API-FUNKTIONEN
-------------------------------------------------

1) Zufälliges Katzenbild
- API: https://api.thecatapi.com/v1/images/search
- Wird per Button-Klick geladen
- Bild wird dynamisch ins Dashboard gerendert

2) Bitcoin-Preis
- API: https://api.coingecko.com/api/v3/simple/price
- Anzeige in USD und CHF
- Aktualisierung per Button

3) Wetter Zürich
- API: https://api.open-meteo.com
- Koordinaten:
  LAT = 47.3769
  LON = 8.5417
- Anzeige:
  - Max-Temperatur
  - Min-Temperatur
  - Niederschlagsmenge

4) Strom-Tankstellen Winterthur
- JSON-Daten:
  https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json
- Koordinaten Winterthur:
  LAT = 47.4988
  LON = 8.7237
- Anzeige der 5 nächstgelegenen Tankstellen
- Klick auf eine Tankstelle zentriert die Karte

5) Karte (Leaflet)
- Bibliothek: Leaflet.js
- Zentriert auf:
  Pionierstrasse 28, Winterthur
- Marker bewegt sich bei Klick auf Tankstelle

-------------------------------------------------
BEWERBUNGSFORMULAR
-------------------------------------------------

Das Formular ist vollständig mit Bootstrap umgesetzt
und enthält browserseitige Validierung.

Felder:
- Geschlecht (Auswahl)
- Vorname
- Nachname
- Strasse und Nr.
- PLZ (4-stellig, validiert)
- Ort
- E-Mail (validiert)
- Handy-Nummer
- Bevorzugte Kontaktart
- Geburtsdatum
- Motivationsschreiben (Textarea)
- Lebenslauf (PDF Upload)
- Portfolio-Link (URL)
- Externer Datenschutz-Link
- Checkbox Datenschutz akzeptieren
- Senden-Button mit Icon

Validierung:
- Pflichtfelder mit required
- Pattern für PLZ
- Typvalidierung für E-Mail / URL
- Visuelle Rückmeldung mit Bootstrap

-------------------------------------------------
FORMULAR-VERARBEITUNG (WEBHOOK)
-------------------------------------------------

Die Formulardaten werden per HTTP POST
an einen Webhook-Endpoint gesendet.

Empfohlener Service:
https://webhook.site/

Ablauf:
1) Webhook-URL auf webhook.site generieren
2) URL im JavaScript eintragen
3) Formular absenden
4) Daten erscheinen im Webhook-Dashboard
5) Erfolgsnachricht wird angezeigt

Kein eigenes Backend notwendig.

-------------------------------------------------
SICHERHEIT – NEVER TRUST USER INPUT
-------------------------------------------------

- Browserseitige Validierung aktiv
- Erwartete Datentypen (email, url, date)
- Pflichtfelder definiert
- Vorbereitung für serverseitige Validierung

-------------------------------------------------
DEPLOYMENT
-------------------------------------------------

- Repository liegt auf GitHub
- Website wird über GitHub Pages ausgeliefert
- Jede Änderung (Commit + Push) triggert automatisches Re-Deployment
- Keine serverseitige Logik notwendig (statische Website)

-------------------------------------------------
TOOLS & TECHNOLOGIEN
-------------------------------------------------

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- jQuery
- Leaflet.js
- Open APIs (ohne API-Key)
- GitHub Pages

-------------------------------------------------
STATUS
-------------------------------------------------

✔ Alle Pflichtaufgaben umgesetzt  
✔ Erweiterte Aufgaben (Advanced) integriert  
✔ API-Anbindungen funktional  
✔ Formular validiert & angebunden  
✔ Deployment über GitHub Pages  

Projekt abgeschlossen 😎
