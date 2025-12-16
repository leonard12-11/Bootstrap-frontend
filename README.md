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
/* 🎄 CHRISTMAS / WINTER THEME – SICHTBAR */
body{
  background:
    radial-gradient(circle at top, #0ea5e9, #020617),
    linear-gradient(120deg, #064e3b, #7c2d12);
  color:#f8fafc;
  font-family:'Poppins',system-ui;
}

/* ❄️ GLASS + FROST */
.glass{
  background:linear-gradient(
    135deg,
    rgba(255,255,255,.35),
    rgba(255,255,255,.05)
  );
  backdrop-filter:blur(22px);
  border-radius:22px;
  border:2px solid rgba(255,255,255,.4);
  box-shadow:
    0 0 40px rgba(186,230,253,.6),
    inset 0 0 30px rgba(255,255,255,.25);
  position:relative;
}

/* ✨ WEIHNACHTS-GLOW */
.glass::after{
  content:"";
  position:absolute;
  inset:-2px;
  border-radius:24px;
  box-shadow:0 0 35px rgba(34,197,94,.35);
  pointer-events:none;
}

/* 🎄 TITEL */
h1,h2,h5{
  font-weight:900;
  background:linear-gradient(90deg,#fef3c7,#fca5a5,#86efac);
  -webkit-background-clip:text;
  color:transparent;
  text-shadow:0 0 25px rgba(255,255,255,.8);
}

/* ❄️ INPUTS */
.form-control,.form-select{
  background:rgba(255,255,255,.2);
  color:white;
  border:1px solid rgba(255,255,255,.5);
}
.form-control:focus,.form-select:focus{
  box-shadow:0 0 15px rgba(186,230,253,1);
  border-color:#bae6fd;
}

/* 🎅 BUTTON */
.btn{
  border-radius:999px;
  font-weight:700;
  background:linear-gradient(135deg,#16a34a,#dc2626);
  border:none;
  color:white;
  box-shadow:0 0 30px rgba(34,197,94,.8);
}
.btn:hover{
  transform:scale(1.08);
  box-shadow:0 0 45px rgba(220,38,38,1);
}

/* ❄️ LISTEN */
.list-group-item{
  background:rgba(255,255,255,.2);
  color:white;
}

/* 🧊 MAP */
#map{
  border-radius:18px;
  box-shadow:0 0 40px rgba(186,230,253,.8);
}
</style>

<script>
for(let i=0;i<60;i++){
  const snow=document.createElement("div");
  snow.innerHTML="❄";
  snow.style.position="fixed";
  snow.style.top="-20px";
  snow.style.left=Math.random()*100+"vw";
  snow.style.fontSize=10+Math.random()*25+"px";
  snow.style.opacity=Math.random();
  snow.style.animation=`fall ${6+Math.random()*10}s linear infinite`;
  document.body.appendChild(snow);
}

const style=document.createElement("style");
style.innerHTML=`
@keyframes fall{
  to{
    transform:translateY(110vh) rotate(360deg);
  }
}`;
document.head.appendChild(style);
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
