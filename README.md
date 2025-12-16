<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>❄️ Winter Dashboard</title>

<!-- Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Leaflet -->
<link href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" rel="stylesheet">

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
/* 🌌 WINTER BACKGROUND */
body{
  background:radial-gradient(circle at top,#38bdf8,#020617);
  min-height:100vh;
  color:#e5e7eb;
  font-family:system-ui;
  overflow-x:hidden;
}

/* ❄️ SCHNEEFALL */
.snowflake{
  position:fixed;
  top:-10px;
  color:white;
  font-size:1em;
  animation:fall linear infinite;
  opacity:.8;
}
@keyframes fall{
  to{transform:translateY(110vh);}
}

/* 🧊 GLASS CARDS */
.card-glass{
  background:rgba(255,255,255,.15);
  backdrop-filter:blur(18px);
  border-radius:25px;
  border:1px solid rgba(255,255,255,.35);
  box-shadow:0 20px 60px rgba(0,0,0,.5);
  padding:25px;
  margin-bottom:30px;
}

/* ✨ TITEL */
h1,h2,h4{
  font-weight:900;
  background:linear-gradient(90deg,#e0f2fe,#bae6fd);
  -webkit-background-clip:text;
  color:transparent;
  text-shadow:0 0 25px rgba(255,255,255,.6);
}

/* ❄️ BUTTON */
.btn-winter{
  background:linear-gradient(135deg,#bae6fd,#38bdf8);
  border:none;
  border-radius:50px;
  color:#020617;
  font-weight:700;
  padding:10px 25px;
  box-shadow:0 0 30px rgba(186,230,253,.9);
}
.btn-winter:hover{
  transform:scale(1.07);
}

/* ❄️ FORM */
.form-control,.form-select{
  background:rgba(255,255,255,.18);
  border:1px solid rgba(255,255,255,.4);
  color:white;
}
.form-control::placeholder{color:#e0f2fe}

/* 🗺 MAP */
#map{
  height:350px;
  border-radius:20px;
}
</style>
</head>

<body>

<!-- ❄️ SCHNEEFLOCKEN -->
<script>
for(let i=0;i<40;i++){
  let s=document.createElement("div");
  s.className="snowflake";
  s.innerHTML="❄";
  s.style.left=Math.random()*100+"vw";
  s.style.animationDuration=5+Math.random()*10+"s";
  s.style.fontSize=10+Math.random()*20+"px";
  document.body.appendChild(s);
}
</script>

<div class="container py-5">

<h1 class="text-center mb-5">🎄 Winter Dashboard ❄️</h1>

<!-- 🐱 KATZE -->
<div class="card-glass text-center">
  <h4>🐱 Zufällige Katze</h4>
  <button class="btn btn-winter my-3" id="catBtn">Katze laden</button>
  <img id="catImg" class="img-fluid rounded">
</div>

<!-- 💰 BITCOIN -->
<div class="card-glass text-center">
  <h4>💰 Bitcoin Preis</h4>
  <button class="btn btn-winter my-3" id="btcBtn">Preis laden</button>
  <p id="btcResult"></p>
</div>

<!-- 🌦 WETTER -->
<div class="card-glass text-center">
  <h4>🌦 Wetter Zürich</h4>
  <button class="btn btn-winter my-3" id="weatherBtn">Wetter laden</button>
  <p id="weatherResult"></p>
</div>

<!-- ⚡ STROM -->
<div class="card-glass">
  <h4>⚡ Strom-Tankstellen (Winterthur)</h4>
  <button class="btn btn-winter my-3" id="chargeBtn">Laden</button>
  <ul id="chargeList"></ul>
</div>

<!-- 🗺 MAP -->
<div class="card-glass">
  <h4>🗺 Karte Winterthur</h4>
  <div id="map"></div>
</div>

<!-- 📋 FORMULAR -->
<div class="card-glass">
<h4>📋 Bewerbung</h4>

<div class="row g-3">
  <div class="col-md-4">
    <label>Geschlecht</label>
    <select class="form-select"><option>Bitte wählen</option></select>
  </div>
  <div class="col-md-4">
    <label>Vorname</label>
    <input class="form-control">
  </div>
  <div class="col-md-4">
    <label>Nachname</label>
    <input class="form-control">
  </div>

  <div class="col-12">
    <label>Strasse & Nr.</label>
    <input class="form-control">
  </div>

  <div class="col-md-4">
    <label>PLZ</label>
    <input class="form-control">
  </div>
  <div class="col-md-8">
    <label>Ort</label>
    <input class="form-control">
  </div>

  <div class="col-md-6">
    <label>E-Mail</label>
    <input class="form-control">
  </div>
  <div class="col-md-6">
    <label>Handy</label>
    <input class="form-control">
  </div>

  <div class="col-12">
    <label>Motivationsschreiben</label>
    <textarea class="form-control" rows="4"></textarea>
  </div>

  <div class="col-md-6">
    <label>Lebenslauf (PDF)</label>
    <input type="file" class="form-control">
  </div>
  <div class="col-md-6">
    <label>Portfolio URL</label>
    <input class="form-control">
  </div>

  <div class="col-12">
    <input type="checkbox"> Datenschutz akzeptieren
  </div>

  <div class="col-12 text-center">
    <button class="btn btn-winter">Senden ❄️</button>
  </div>
</div>
</div>

</div>

<script>
// 🐱 Katze
$("#catBtn").click(()=>$.get("https://api.thecatapi.com/v1/images/search",d=>$("#catImg").attr("src",d[0].url)));

// 💰 Bitcoin
$("#btcBtn").click(()=>$.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,chf",
d=>$("#btcResult").html(`USD: $${d.bitcoin.usd}<br>CHF: CHF ${d.bitcoin.chf}`)));

// 🌦 Wetter
$("#weatherBtn").click(()=>$.get("https://api.open-meteo.com/v1/forecast?latitude=47.3769&longitude=8.5417&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Europe/Zurich",
d=>$("#weatherResult").html(`Min: ${d.daily.temperature_2m_min[0]}°C<br>Max: ${d.daily.temperature_2m_max[0]}°C`)));

// ⚡ Strom
$("#chargeBtn").click(()=>$.get("https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json",
d=>{
$("#chargeList").empty();
d.features.slice(0,5).forEach(s=>$("#chargeList").append(`<li>${s.properties.Name}</li>`));
}));

// 🗺 Map
const map=L.map('map').setView([47.4988,8.7237],13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
</script>

</body>
</html>
