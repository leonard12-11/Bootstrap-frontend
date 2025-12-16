body{
  font-family:'Inter',sans-serif;
  background:
    radial-gradient(circle at top,#1e293b,#020617),
    linear-gradient(180deg,#020617,#0f172a);
  color:#e5e7eb;
  overflow-x:hidden;
}

/* ❄️ SNOW OVERLAY */
body::before{
  content:"";
  position:fixed;
  inset:0;
  background-image:
    radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,.8) 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 70% 80%, rgba(255,255,255,.6) 50%, transparent 51%),
    radial-gradient(1px 1px at 40% 60%, rgba(255,255,255,.5) 50%, transparent 51%);
  animation:snow 20s linear infinite;
  pointer-events:none;
  opacity:.25;
}

@keyframes snow{
  from{transform:translateY(-100px)}
  to{transform:translateY(800px)}
}

/* ❄️ GLASS = ICE */
.card-glass{
  background:linear-gradient(
    180deg,
    rgba(255,255,255,.18),
    rgba(255,255,255,.06)
  );
  backdrop-filter:blur(22px);
  border-radius:26px;
  padding:30px;
  border:1px solid rgba(255,255,255,.25);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.4),
    0 30px 90px rgba(0,0,0,.7);
  transition:.4s;
}
.card-glass:hover{
  transform:translateY(-8px);
  box-shadow:0 40px 120px rgba(186,230,253,.35);
}

/* ❄️ HEADINGS */
h1,h2,h3,h5{
  font-weight:900;
  background:linear-gradient(90deg,#bae6fd,#e0f2fe);
  -webkit-background-clip:text;
  color:transparent;
  text-shadow:0 0 25px rgba(186,230,253,.35);
}

/* ❄️ BUTTON */
.btn-glow{
  background:linear-gradient(135deg,#38bdf8,#7dd3fc);
  border:none;
  border-radius:999px;
  color:#020617;
  font-weight:600;
  box-shadow:0 0 30px rgba(186,230,253,.6);
}
.btn-glow:hover{
  box-shadow:0 0 50px rgba(186,230,253,.9);
  transform:scale(1.05);
}

/* ❄️ FORM */
.form-control,.form-select{
  background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.3);
  color:white;
}
.form-control::placeholder{
  color:#cbd5f5;
}
.form-control:focus,.form-select:focus{
  box-shadow:0 0 0 2px rgba(186,230,253,.8);
  border-color:#bae6fd;
}

/* ❄️ MAP */
#map{
  height:350px;
  border-radius:22px;
  border:1px solid rgba(255,255,255,.3);
}
