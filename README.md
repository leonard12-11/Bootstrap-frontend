<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>❄️ Winter Smart Dashboard</title>

<!-- Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<!-- jQuery -->
<script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>

<!-- Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Font -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">

<style>
/* ===== WINTER BACKGROUND ===== */
body{
  background:
    radial-gradient(circle at top,#bae6fd,#020617),
    linear-gradient(135deg,#064e3b,#7c2d12);
  color:#f8fafc;
  font-family:'Poppins',sans-serif;
  overflow-x:hidden;
}

/* ===== GLASS / ICE CARDS ===== */
.glass{
  background:linear-gradient(135deg,rgba(255,255,255,.35),rgba(255,255,255,.08));
  backdrop-filter:blur(22px);
  border-radius:22px;
  padding:25px;
  border:2px solid rgba(255,255,255,.4);
  box-shadow:0 0 45px rgba(186,230,253,.6);
  transition:.3s;
}
.glass:hover{ transform:translateY(-6px) }

/* ===== HEADINGS ===== */
h1,h2,h5{
  font-weight:900;
  background:linear-gradient(90deg,#fef3c7,#fca5a5,#86efac);
  -webkit-background-clip:text;
  color:transparent;
  text-shadow:0 0 25px rgba(255,255,255,.8);
}

/* ===== BUTTONS ===== */
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

/* ===== INPUTS ===== */
.form-control,.form-select{
  background:rgba(255,255,255,.2);
  color:white;
  border:1px solid rgba(255,255,255,.5);
}
.form-control:focus,.form-select:focus{
  box-shadow:0 0 15px rgba(186,230,253,1);
  border-color:#bae6fd;
}

/* ===== LIST ===== */
.list-group-item{
  background:rgba(255,255,255,.2);
  color:white;
  border:none;
}

/* ===== MAP ===== */
#map{
  height:350px;
  border-radius:18px;
  box-shadow:0 0 40px rgba(186,230,253,.8);
}
</style>
</head>

<body>

<!-- ❄️ SNOWFALL -->
<script>
for(let i=0;i<60;i++){
  const snow=document.createElement("div");
  snow.textContent="❄";
  snow.style.position="fixed";
  snow.style.top="-20px";
  snow.style.left=Math.random()*100+"vw";
  snow.style.fontSize=10+Math.random()*25+"px";
  snow.style.opacity=Math.random();
  snow.style.pointerEvents="none";
  snow.style.animation=`fall ${6+Math.random()*10}s linear infinite`;
  document.body.appendChild(snow);
}
const s=document.createElement("style");
s.innerHTML=`@keyframes fall{to{transform:translateY(110vh) rotate(360deg)}}`;
document.head.appendChild(s);
</script>

<div class="container py-5">

<h1 class="text-center mb-5">🎄 Winter Smart Dashboard</h1>

<!-- DASHBOARD -->
<div class="row g-4">

<div class="col-md-4">
<div class="glass text-center">
<h5>🐱 Zufällige Katze</h5>
<button id="btnCat" class="btn mt-2">Laden</button>
<div id="cat" class="mt-3"></div>
</div>
</div>

<div class="col-md-4">
<div class="glass text-center">
<h5>₿ Bitcoin</h5>
<button id="btnBTC" class="btn mt-2">Anzeigen</button>
<div id="btc" class="mt-3 fs-5"></div>
</div>
</div>

<div class="col-md-4">
<div class="glass text-center">
<h5>🌤 Wetter Zürich</h5>
<button id="btnWeather" class="btn mt-2">Laden</button>
<div id="weather" class="mt-3"></div>
</div>
</div>

<div class="col-md-6">
<div class="glass">
<h5>⚡ Strom-Tankstellen Winterthur</h5>
<button id="btnCharge" class="btn mt-2">Laden</button>
<ul id="charges" class="list-group mt-3"></ul>
</div>
</div>

<div class="col-md-6">
<div class="glass">
<h5>🗺 Karte Winterthur</h5>
<div id="map"></div>
</div>
</div>

</div>

<hr class="my-5">

<!-- FORM -->
<h2 class="text-center mb-4">📄 Bewerbungsformular</h2>

<div class="glass">
<form id="form" class="row g-3 needs-validation" novalidate>

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

<div class="col-md-6">
<label class="form-label">E-Mail</label>
<input type="email" class="form-control" required>
</div>

<div class="col-md-6">
<label class="form-label">Handy</label>
<input type="tel" class="form-control" required>
</div>

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

<div class="col-12 form-check">
<input class="form-check-input" type="checkbox" required>
<label class="form-check-label">Datenschutz akzeptieren</label>
</div>

<div class="col-12 text-end">
<button class="btn px-4">📧 Senden</button>
</div>

</form>

<div id="success" class="text-center mt-4 d-none">
<h4>✅ Erfolgreich gesendet</h4>
</div>
</div>

</div>

<script>
// ===== MAP =====
const map=L.map('map').setView([47.4988,8.7237],14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let marker=L.marker([47.4988,8.7237]).addTo(map);

// ===== APIS =====
$("#btnCat").click(()=>$.get("https://api.thecatapi.com/v1/images/search",d=>{
$("#cat").html(`<img src="${d[0].url}" class="img-fluid rounded">`);
}));

$("#btnBTC").click(()=>$.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,chf",d=>{
$("#btc").html(`USD ${d.bitcoin.usd}<br>CHF ${d.bitcoin.chf}`);
}));

$("#btnWeather").click(()=>$.get("https://api.open-meteo.com/v1/forecast?latitude=47.3769&longitude=8.5417&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&forecast_days=1&timezone=Europe/Zurich",d=>{
$("#weather").html(`Max ${d.daily.temperature_2m_max[0]}°C<br>Min ${d.daily.temperature_2m_min[0]}°C`);
}));

$("#btnCharge").click(()=>{
$("#charges").empty();
$.get("https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/ch.bfe.ladestellen-elektromobilitaet.json",d=>{
d.features.slice(0,5).forEach(s=>{
const c=s.geometry.coordinates;
$(`<li class="list-group-item">${s.properties.name||"Ladestation"}</li>`)
.click(()=>{map.setView([c[1],c[0]],16);marker.setLatLng([c[1],c[0]]);})
.appendTo("#charges");
});
});
});

$("#form").on("submit",function(e){
e.preventDefault();
if(!this.checkValidity()){this.classList.add("was-validated");return;}
$("#success").removeClass("d-none");
this.reset();
});
</script>

</body>
</html>
