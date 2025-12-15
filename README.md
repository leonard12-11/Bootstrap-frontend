<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart Dashboard & Bewerbung</title>

<!-- Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<!-- jQuery -->
<script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>

<!-- Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Google Font -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

<style>
body {
  background: linear-gradient(135deg,#020617,#0f172a);
  font-family: 'Poppins', sans-serif;
  color: #f8fafc;
}
h1,h2,h3 {
  font-weight: 700;
  text-shadow: 0 0 20px rgba(56,189,248,.35);
}
.glass {
  background: rgba(255,255,255,.08);
  backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid rgba(255,255,255,.15);
  box-shadow: 0 25px 60px rgba(0,0,0,.45);
  transition: .3s;
}
.glass:hover { transform: translateY(-6px); }
.btn { border-radius: 999px; }
.list-group-item {
  background: rgba(255,255,255,.06);
  color: white;
  border: none;
  cursor: pointer;
}
.list-group-item:hover {
  background: rgba(56,189,248,.3);
}
#map {
  height: 350px;
  border-radius: 16px;
}
.form-control, .form-select {
  background: rgba(255,255,255,.08);
  color: white;
  border: 1px solid rgba(255,255,255,.25);
}
.form-control:focus, .form-select:focus {
  border-color: #38bdf8;
  box-shadow: 0 0 12px rgba(56,189,248,.6);
}
.fade-in {
  animation: fade .6s ease;
}
@keyframes fade {
  from {opacity:0; transform: translateY(10px);}
  to {opacity:1; transform: translateY(0);}
}
</style>
</head>

<body>
<div class="container py-5">

<h1 class="text-center mb-5">⚡ Smart Dashboard</h1>

<!-- DASHBOARD -->
<div class="row g-4">

<div class="col-md-4">
<div class="glass text-center">
<h5>🐱 Zufällige Katze</h5>
<button id="btnCat" class="btn btn-outline-info mt-2">Laden</button>
<div id="cat" class="mt-3"></div>
</div>
</div>

<div class="col-md-4">
<div class="glass text-center">
<h5>₿ Bitcoin Preis</h5>
<button id="btnBTC" class="btn btn-outline-warning mt-2">Anzeigen</button>
<div id="btc" class="mt-3 fs-5"></div>
</div>
</div>

<div class="col-md-4">
<div class="glass text-center">
<h5>🌤 Wetter Zürich</h5>
<button id="btnWeather" class="btn btn-outline-primary mt-2">Laden</button>
<div id="weather" class="mt-3"></div>
</div>
</div>

<div class="col-md-6">
<div class="glass">
<h5>⚡ Strom-Tankstellen Winterthur</h5>
<button id="btnCharge" class="btn btn-outline-success mt-2">Laden</button>
<ul id="charges" class="list-group mt-3"></ul>
</div>
</div>

<div class="col-md-6">
<div class="glass">
<h5>🗺 Karte – Winterthur</h5>
<div id="map"></div>
</div>
</div>

</div>

<hr class="my-5">

<!-- FORMULAR -->
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
<input class="form-control" required>
</div>

<div class="col-md-5">
<label class="form-label">Nachname</label>
<input class="form-control" required>
</div>

<div class="col-12">
<label class="form-label">Strasse & Nr.</label>
<input class="form-control" required>
</div>

<div class="col-md-4">
<label class="form-label">PLZ</label>
<input class="form-control" pattern="\d{4}" required>
</div>

<div class="col-md-8">
<label class="form-label">Ort</label>
<input class="form-control" required>
</div>

<h5>Kontakt</h5>

<div class="col-md-6">
<label class="form-label">E-Mail</label>
<input type="email" class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Handy</label>
<input type="tel" class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Kontaktart</label>
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
<label class="form-label">Portfolio URL</label>
<input type="url" class="form-control" required>
</div>

<div class="col-12">
<a href="https://www.edoeb.admin.ch" target="_blank">Datenschutzbestimmungen</a>
</div>

<div class="col-12 form-check">
<input class="form-check-input" type="checkbox" required>
<label class="form-check-label">Datenschutz akzeptieren</label>
</div>

<div class="col-12 text-end">
<button class="btn btn-primary px-4">📧 Bewerbung senden</button>
</div>

</form>

<div id="success" class="text-center mt-4 d-none fade-in">
<h4>✅ Erfolgreich gesendet</h4>
</div>

</div>

</div>

<script>
// ===== KONSTANTEN =====
const LAT = 47.3769, LON = 8.5417;
const WINT_LAT = 47.4988, WINT_LON = 8.7237;

// ===== MAP =====
const map = L.map('map').setView([WINT_LAT, WINT_LON], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let marker = L.marker([WINT_LAT, WINT_LON]).addTo(map);

// ===== APIs =====
$("#btnCat").click(()=>{
$.get("https://api.thecatapi.com/v1/images/search",d=>{
$("#cat").html(`<img src="${d[0].url}" class="img-fluid rounded fade-in">`);
});
});

$("#btnBTC").click(()=>{
$.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,chf",d=>{
$("#btc").html(`USD ${d.bitcoin.usd}<br>CHF ${d.bitcoin.chf}`);
});
});

$("#btnWeather").click(()=>{
$.get(`https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&forecast_days=1&timezone=Europe/Zurich`,d=>{
$("#weather").html(`
Max: ${d.daily.temperature_2m_max[0]}°C<br>
Min: ${d.daily.temperature_2m_min[0]}°C<br>
Regen: ${d.daily.precipitation_sum[0]} mm
`);
});
});

$("#btnCharge").click(()=>{
$("#charges").empty();
$.get("https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json",d=>{
d.features.slice(0,5).forEach(s=>{
const c = s.geometry.coordinates;
$(`<li class="list-group-item fade-in">${s.properties.name || "Ladestation"}</li>`)
.click(()=>{map.setView([c[1],c[0]],16);marker.setLatLng([c[1],c[0]]);})
.appendTo("#charges");
});
});
});

// ===== FORMULAR + WEBHOOK =====
$("#form").on("submit",function(e){
e.preventDefault();
if(!this.checkValidity()){
this.classList.add("was-validated");
return;
}
$.post("PASTE_DEIN_WEBHOOK_HIER",$(this).serialize(),()=>{
$("#success").removeClass("d-none");
this.reset();
});
});
</script>

</body>
</html>
