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

<!-- Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">

<!-- Font -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

<style>
body {
  background: linear-gradient(270deg,#020617,#0f172a,#020617);
  background-size: 600% 600%;
  animation: bg 20s ease infinite;
  font-family: 'Poppins', sans-serif;
  color: #f8fafc;
}
@keyframes bg {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

h1,h2 {
  font-weight: 700;
  text-shadow: 0 0 25px rgba(56,189,248,.4);
}

.navbar {
  backdrop-filter: blur(14px);
  background: rgba(2,6,23,.6);
}

.glass {
  background: rgba(255,255,255,.08);
  backdrop-filter: blur(18px);
  border-radius: 22px;
  padding: 26px;
  border: 1px solid rgba(255,255,255,.15);
  box-shadow: 0 30px 70px rgba(0,0,0,.5);
  transition: .4s;
}
.glass:hover {
  transform: translateY(-8px) scale(1.01);
  box-shadow: 0 35px 80px rgba(56,189,248,.25);
}

.btn {
  border-radius: 999px;
  position: relative;
  overflow: hidden;
}
.btn::after {
  content:"";
  position:absolute;
  inset:0;
  background: radial-gradient(circle at top,rgba(255,255,255,.35),transparent);
  opacity:.2;
}

.list-group-item {
  background: rgba(255,255,255,.06);
  color: white;
  border: none;
  cursor: pointer;
}
.list-group-item:hover {
  background: rgba(56,189,248,.35);
}

#map {
  height: 360px;
  border-radius: 18px;
}

.form-control, .form-select {
  background: rgba(255,255,255,.08);
  color: white;
  border: 1px solid rgba(255,255,255,.25);
}
.form-control:focus, .form-select:focus {
  border-color: #38bdf8;
  box-shadow: 0 0 14px rgba(56,189,248,.6);
}

.fade-in {
  animation: fade .6s ease;
}
@keyframes fade {
  from {opacity:0; transform: translateY(12px);}
  to {opacity:1; transform: translateY(0);}
}

.badge {
  background: rgba(56,189,248,.2);
  border: 1px solid rgba(56,189,248,.4);
}

.spinner {
  display:none;
}
</style>
</head>

<body>

<!-- NAVBAR -->
<nav class="navbar navbar-dark fixed-top">
  <div class="container">
    <span class="navbar-brand">⚡ Smart Dashboard</span>
    <span id="clock" class="badge"></span>
  </div>
</nav>

<div class="container py-5 mt-5">

<h1 class="text-center mb-5">🚀 Live API Dashboard</h1>

<div class="row g-4">

<div class="col-md-4">
<div class="glass text-center">
<h5>🐱 Katze <span class="badge ms-2">API</span></h5>
<button id="btnCat" class="btn btn-outline-info mt-2">Laden</button>
<div class="spinner spinner-border text-info mt-3"></div>
<div id="cat" class="mt-3"></div>
</div>
</div>

<div class="col-md-4">
<div class="glass text-center">
<h5>₿ Bitcoin <span class="badge ms-2">Live</span></h5>
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
<h5>⚡ Ladestationen Winterthur</h5>
<button id="btnCharge" class="btn btn-outline-success mt-2">Laden</button>
<ul id="charges" class="list-group mt-3"></ul>
</div>
</div>

<div class="col-md-6">
<div class="glass">
<h5>🗺 Karte</h5>
<div id="map"></div>
</div>
</div>

</div>

<hr class="my-5">

<h2 class="text-center mb-4">📄 Bewerbungsformular</h2>

<div class="glass">
<form id="form" class="row g-3 needs-validation" novalidate>

<div class="col-md-6">
<label class="form-label">Vorname</label>
<input class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Nachname</label>
<input class="form-control" required>
</div>

<div class="col-12">
<label class="form-label">E-Mail</label>
<input type="email" class="form-control" required>
</div>

<div class="col-12">
<label class="form-label">Motivation</label>
<textarea class="form-control" rows="4" required></textarea>
</div>

<div class="col-12 text-end">
<button class="btn btn-primary px-5">🚀 Absenden</button>
</div>

</form>

<div id="success" class="text-center mt-4 d-none fade-in">
<h4>✅ Erfolgreich gesendet</h4>
</div>
</div>

</div>

<script>
// ===== CLOCK =====
setInterval(()=>{
const d=new Date();
$("#clock").text(d.toLocaleTimeString());
},1000);

// ===== MAP =====
const map=L.map('map').setView([47.4988,8.7237],14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let marker=L.marker([47.4988,8.7237]).addTo(map);

// ===== APIs =====
$("#btnCat").click(()=>{
$(".spinner").show();
$.get("https://api.thecatapi.com/v1/images/search",d=>{
$("#cat").html(`<img src="${d[0].url}" class="img-fluid rounded fade-in">`);
$(".spinner").hide();
});
});

$("#btnBTC").click(()=>{
$.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,chf",
d=>$("#btc").html(`USD ${d.bitcoin.usd}<br>CHF ${d.bitcoin.chf}`));
});

$("#btnWeather").click(()=>{
$.get("https://api.open-meteo.com/v1/forecast?latitude=47.3769&longitude=8.5417&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Europe/Zurich",
d=>$("#weather").html(`Max ${d.daily.temperature_2m_max[0]}°C<br>Min ${d.daily.temperature_2m_min[0]}°C`));
});

$("#btnCharge").click(()=>{
$("#charges").empty();
$.get("https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json",d=>{
d.features.slice(0,5).forEach(s=>{
const c=s.geometry.coordinates;
$(`<li class="list-group-item fade-in">${s.properties.name||"Ladestation"}</li>`)
.click(()=>{map.flyTo([c[1],c[0]],16);marker.setLatLng([c[1],c[0]]);})
.appendTo("#charges");
});
});
});

// ===== FORM =====
$("#form").on("submit",function(e){
e.preventDefault();
if(!this.checkValidity()){this.classList.add("was-validated");return;}
$.post("PASTE_DEIN_WEBHOOK_HIER",$(this).serialize(),()=>{
$("#success").removeClass("d-none");
this.reset();
});
});
</script>

</body>
</html>
