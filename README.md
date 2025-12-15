# ⚡ Smart Dashboard & Bewerbungsformular (Bootstrap Frontend)

Dieses Projekt ist ein **modernes Dashboard mit API-Anbindungen** sowie ein **vollständiges, valides Bewerbungsformular**.  
Die Umsetzung erfolgte mit **Bootstrap 5**, **jQuery**, **Leaflet** und **offenen APIs** (kein API-Key nötig 😎).

---

## 🚀 Dashboard-Funktionen

- 🐱 Zufälliges Katzenbild (TheCatAPI)
- ₿ Bitcoin-Preis in **USD & CHF** (CoinGecko)
- 🌤 Aktuelles Wetter für **Zürich** (Open-Meteo)
- ⚡ Anzeige der **5 nächstgelegenen Strom-Tankstellen**
- 🗺 Interaktive **Leaflet-Karte** (Winterthur)
- 📍 Klick auf Tankstelle zentriert die Karte (Advanced)

---

## 📄 Bewerbungsformular (vollständig)

Das Formular dient zur **Digitalisierung von Praktikums-Bewerbungen** und erfüllt alle Anforderungen der Aufgabenstellung.

### Enthaltene Formularfelder

**Persönliche Daten**
- Geschlecht (Auswahl)
- Vorname
- Nachname
- Strasse & Nr.
- PLZ (Validierung: 4-stellig)
- Ort

**Kontakt**
- E-Mail (Typ `email`)
- Handy-Nummer
- Bevorzugte Kontaktart (Auswahl)
- Geburtsdatum (Datumsauswahl)

**Bewerbung**
- Motivationsschreiben (Textarea)
- Lebenslauf (PDF-Upload)
- Portfolio-Link (URL)

**Datenschutz**
- Externer Link zu Datenschutzbestimmungen
- Checkbox zum Akzeptieren (Pflichtfeld)

**Abschluss**
- Senden-Button mit Mail-Icon
- Browser-seitige Validierung
- POST-Übermittlung an Webhook-Endpoint

---

## 🧠 Validierung & UX

- HTML5-Validierungen (`required`, `type`, `pattern`)
- Bootstrap-Feedback (`was-validated`)
- Subtile Hover- & Fokus-Effekte
- Glassmorphism-Design
- Benutzerfreundliche Struktur mit Überschriften

---

## 📦 Verwendete Technologien

- HTML5
- CSS3 (Glassmorphism)
- Bootstrap 5
- jQuery
- Leaflet
- Open APIs (ohne API-Key)
- Webhook.site (Formular-Endpoint)

---

## 📄 Vollständiger Beispiel-Code (index.html)

> ℹ️ **Hinweis:**  
> Dieser Code gehört in eine `index.html`.  
> Das README dient der Dokumentation des Projekts.


<!-- HIER BEGINNT DAS FORMULAR -->
<h2 class="text-center mb-4">📄 Bewerbungsformular</h2>

<div class="glass">
<form id="form" class="row g-3 needs-validation" novalidate>

<h5>Persönliche Daten</h5>

<div class="col-md-3">
<label class="form-label">Geschlecht</label>
<select class="form-select" required>
<option value="">Bitte wählen</option>
<option>Männlich</option>
<option>Weiblich</option>
<option>Divers</option>
</select>
</div>

<div class="col-md-4">
<label class="form-label">Vorname</label>
<input type="text" class="form-control" required>
</div>

<div class="col-md-5">
<label class="form-label">Nachname</label>
<input type="text" class="form-control" required>
</div>

<div class="col-12">
<label class="form-label">Strasse & Nr.</label>
<input type="text" class="form-control" required>
</div>

<div class="col-md-4">
<label class="form-label">PLZ</label>
<input type="text" class="form-control" pattern="\d{4}" required>
</div>

<div class="col-md-8">
<label class="form-label">Ort</label>
<input type="text" class="form-control" required>
</div>

<h5>Kontakt</h5>

<div class="col-md-6">
<label class="form-label">E-Mail</label>
<input type="email" class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Handy-Nummer</label>
<input type="tel" class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Bevorzugte Kontaktart</label>
<select class="form-select" required>
<option>Email</option>
<option>Telefon</option>
</select>
</div>

<div class="col-md-6">
<label class="form-label">Geburtsdatum</label>
<input type="date" class="form-control" required>
</div>

<h5>Bewerbung</h5>

<div class="col-12">
<label class="form-label">Motivationsschreiben</label>
<textarea class="form-control" rows="4" required></textarea>
</div>

<div class="col-md-6">
<label class="form-label">Lebenslauf (PDF)</label>
<input type="file" class="form-control" accept="application/pdf" required>
</div>

<div class="col-md-6">
<label class="form-label">Portfolio-URL</label>
<input type="url" class="form-control" required>
</div>

<div class="col-12">
<a href="https://www.edoeb.admin.ch" target="_blank">
Datenschutzbestimmungen
</a>
</div>

<div class="col-12 form-check">
<input class="form-check-input" type="checkbox" required>
<label class="form-check-label">
Ich akzeptiere die Datenschutzbestimmungen
</label>
</div>

<div class="col-12 text-end">
<button class="btn btn-primary">
📧 Bewerbung senden
</button>
</div>

</form>
</div>
<!-- HIER ENDET DAS FORMULAR -->
