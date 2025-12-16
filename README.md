<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart Dashboard</title>

<!-- Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<!-- jQuery -->
<script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>

<!-- Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">

<!-- Font -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap" rel="stylesheet">

<style>
*{scroll-behavior:smooth}
body{
  font-family:'Inter',sans-serif;
  background:radial-gradient(circle at top,#0f172a,#020617);
  color:#e5e7eb;
}

/* HERO */
.hero{
  min-height:60vh;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  background:
    radial-gradient(circle at 20% 20%,rgba(56,189,248,.15),transparent 40%),
    radial-gradient(circle at 80% 80%,rgba(168,85,247,.15),transparent 40%);
}
.hero h1{
  font-size:3.5rem;
  font-weight:900;
  background:linear-gradient(90deg,#38bdf8,#a855f7);
  -webkit-background-clip:text;
  color:transparent;
}
.hero p{color:#cbd5f5}

/* CARDS */
.card-glass{
  background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.04));
  backdrop-filter:blur(20px);
  border-radius:24px;
  padding:28px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.2),
    0 30px 80px rgba(0,0,0,.6);
  transition:.4s;
}
.card-glass:hover{
  transform:translateY(-10px) scale(1.02);
  box-shadow:0 40px 120px rgba(56,189,248,.35);
}

/* ICONS */
.icon{
  font-size:2.2rem;
  background:linear-gradient(135deg,#38bdf8,#a855f7);
  -webkit-background-clip:text;
  color:transparent;
}

/* BUTTON */
.btn-glow{
  border:none;
  border-radius:999px;
  background:linear-gradient(135deg,#38bdf8,#a855f7);
  color:white;
  padding:.6rem 1.6rem;
  box-shadow:0 0 25px rgba(56,189,248,.5);
}
.btn-glow:hover{
  box-shadow:0 0 45px rgba(168,85,247,.8);
}

/* MAP */
#map{
  height:350px;
  border-radius:20px;
}

/* FORM */
.form-control, .form-select{
  background:rgba(255,255,255,.08);
  border:none;
  color:white;
}
.form-control:focus{
  box-shadow:0 0 0 2px rgba(56,189,248,.6);
}

/* FADE */
.fade-in{animation:fade .6s ease}
@keyframes fade{
  from{opacity:0;transform:translateY(15px)}
  to{opacity:1}
}
</style>
</head>

<body>

<!-- HERO -->
<section class="hero">
  <div>
    <h1>Smart Dashboard</h1>
    <p>APIs • Maps • Formulare • UX</p>
  </div>
</section>

<div class="container pb-5">

<!-- DASHBOARD -->
<div class="row g-4">

<div class="col-md-4">
<div class="card-glass text-center">
<div class="icon">🐱</div>
<h5>Zufällige Katze</h5>
<button id="btnCat" class="btn-glow mt-2">Laden</button>
<div id="cat" class="mt-3"></div>
</div>
</div>

<div class="col-md-4">
<div class="card-glass text-center">
<div class="icon">₿</div>
<h5>Bitcoin Preis</h5>
<button id="btnBTC" class="btn-glow mt-2">Anzeigen</button>
<div id="btc" class="mt-3 fs-5"></div>
</div>
</div>

<div class="col-md-4">
<div class="card-glass text-center">
<div class="icon">🌤</div>
<h5>Wetter Zürich</h5>
<button id="btnWeather" class="btn-glow mt-2">Laden</button>
<div id="weather" class="mt-3"></div>
</div>
</div>

<div class="col-md-6">
<div class="card-glass">
<h5>⚡ Ladestationen</h5>
<button id="btnCharge" class="btn-glow mt-2">Laden</button>
<ul id="charges" class="list-group mt-3"></ul>
</div>
</div>

<div class="col-md-6">
<div class="card-glass">
<h5>🗺 Karte Winterthur</h5>
<div id="map"></div>
</div>
</div>

</div>

<hr class="my-5">

<!-- FORM -->
<h2 class="text-center mb-4">Bewerbungsformular</h2>

<div class="card-glass">
<form id="form" class="row g-3 needs-validation" novalidate>

<div class="col-md-6">
<label>Vorname</label>
<input class="form-control" required>
</div>

<div class="col-md-6">
<label>Nachname</label>
<input class="form-control" required>
</div>

<div class="col-12">
<label>Email</label>
<input type="email" class="form-control" required>
</div>

<div class="col-12">
<label>Motivation</label>
<textarea class="form-control" rows="4" required></textarea>
</div>

<div class="col-12 text-end">
<button class="btn-glow">Absenden 🚀</button>
</div>

</form>

<div id="success" class="text-center mt-4 d-none fade-in">
<h4>✅ Erfolgreich gesendet</h4>
</div>
</div>

</div>

<script>
// MAP
const map=L.map('map').setView([47.4988,8.7237],14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let marker=L.marker([47.4988,8.7237]).addTo(map);

// CAT
$("#btnCat").click(()=>$.get("https://api.thecatapi.com/v1/images/search",d=>{
$("#cat").html(`<img src="${d[0].url}" class="img-fluid rounded fade-in">`);
}));

// BTC
$("#btnBTC").click(()=>$.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,chf",
d=>$("#btc").html(`USD ${d.bitcoin.usd}<br>CHF ${d.bitcoin.chf}`)));

// WEATHER
$("#btnWeather").click(()=>$.get("https://api.open-meteo.com/v1/forecast?latitude=47.3769&longitude=8.5417&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Europe/Zurich",
d=>$("#weather").html(`Max ${d.daily.temperature_2m_max[0]}°C<br>Min ${d.daily.temperature_2m_min[0]}°C`)));

// CHARGE
$("#btnCharge").click(()=>{
$("#charges").empty();
$.get("https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json",d=>{
d.features.slice(0,5).forEach(s=>{
const c=s.geometry.coordinates;
$(`<li class="list-group-item bg-transparent text-white">${s.properties.name||"Ladestation"}</li>`)
.click(()=>{map.flyTo([c[1],c[0]],16);marker.setLatLng([c[1],c[0]]);})
.appendTo("#charges");
});
});
});

// FORM
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
