"""Auswertung: alle Kennzahlen und Grafiken fuer die drei Entscheide.

Grundsatz aus dem Unterricht: Code rechnet, KI interpretiert, wir pruefen beides.
JEV hat pro Bewertung und Thema nur eine Wahrscheinlichkeit geliefert (0-1).
Alles Zaehlen, Prozente, Bandbreiten und Tests passiert hier im Code.
"""
import os, re, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint

sys.path.insert(0, os.path.dirname(__file__))
from codebook import THEMES, TOPICS, LABEL, SUBSCORE, YES, NO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")
SUBS = ["cleanliness", "value", "location", "rooms", "sleep_quality"]
SUB_DE = {"cleanliness": "Sauberkeit", "value": "Preis-Leistung", "location": "Lage",
          "rooms": "Zimmer", "sleep_quality": "Schlaf"}

# Farben (validierte Referenzpalette, Light-Mode)
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#b5b3ad"
INK, INK2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"


# ---------------------------------------------------------------- Daten laden
def load():
    s = pd.read_csv(os.path.join(DATA, "sample_5000.csv"))
    s = s.rename(columns={c: "note_" + c for c in SUBS})  # Teilnoten: note_cleanliness etc.
    r = pd.read_csv(os.path.join(DATA, "jev_results.csv")).drop(columns=["model", "input_tokens"])
    df = s.merge(r, on="review_id", how="inner")
    df["group"] = pd.cut(df.overall, [0, 2, 3, 5], labels=["unzufrieden (1-2)", "mittel (3)", "zufrieden (4-5)"])
    return df


def share_with_range(p, n_thr=0.5):
    """Anteil 'ja' (p>=0.5) plus ehrliche Bandbreite.

    Bandbreite = untere Grenze: nur sichere Ja (p>=0.7), 95%-Wilson-Intervall unten
                 obere Grenze:  alles ausser sichere Nein (p>0.3), 95%-Wilson-Intervall oben
    So stecken Stichprobenzufall UND KI-Unsicherheit in der Bandbreite.
    """
    n = len(p)
    k = int((p >= n_thr).sum())
    lo = proportion_confint(int((p >= YES).sum()), n, method="wilson")[0]
    hi = proportion_confint(int((p > NO).sum()), n, method="wilson")[1]
    return k / n, lo, hi, k, n


# ---------------------------------------------------------------- Entscheid 1
def decision1(df):
    unhappy = df[df.overall <= 2]
    happy = df[df.overall >= 4]
    rows = []
    for t in TOPICS:
        sh, lo, hi, k, n = share_with_range(unhappy[t])
        sh_h = (happy[t] >= 0.5).mean()
        rows.append(dict(thema=t, Thema=LABEL[t], Teilnote=SUB_DE.get(SUBSCORE[t], "- (nicht abgefragt)"),
                         anteil_unzufrieden=sh, von=lo, bis=hi, anzahl=k, n=n,
                         anteil_zufrieden=sh_h, faktor=sh / sh_h if sh_h else np.nan))
    return pd.DataFrame(rows).sort_values("anteil_unzufrieden", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------- Entscheid 2
def decision2(df):
    """Erklaeren die Themen die Gesamtnote ueber die 5 Teilnoten hinaus?

    Modell A: overall ~ 5 Teilnoten
    Modell B: overall ~ 5 Teilnoten + alle Themen (0/1)
    Koeffizient eines Themas in B = zusaetzlicher Sterne-Abzug, den die Teilnoten NICHT erklaeren.
    """
    d = df.copy()
    for t in TOPICS:
        d[t + "_j"] = (d[t] >= 0.5).astype(int)
    fa = "overall ~ " + " + ".join("note_" + c for c in SUBS)
    fb = fa + " + " + " + ".join(t + "_j" for t in TOPICS)
    ma = smf.ols(fa, d).fit()
    mb = smf.ols(fb, d).fit(cov_type="HC3")
    ci = mb.conf_int()
    rows = []
    for t in TOPICS:
        c = t + "_j"
        rows.append(dict(thema=t, Thema=LABEL[t], Teilnote=SUB_DE.get(SUBSCORE[t], "- (nicht abgefragt)"),
                         abgefragt=SUBSCORE[t] is not None, sterne_effekt=mb.params[c],
                         von=ci.loc[c, 0], bis=ci.loc[c, 1], p_wert=mb.pvalues[c],
                         anteil_alle=d[c].mean()))
    res = pd.DataFrame(rows).sort_values("sterne_effekt").reset_index(drop=True)
    return res, dict(r2_a=ma.rsquared, r2_b=mb.rsquared, n=int(mb.nobs))


def convergent_validity(df):
    """Plausibilitaet: Wenn JEV 'Sauberkeit-Beschwerde' meldet, ist dann die Sauberkeits-Note tiefer?"""
    rows = []
    for t in TOPICS:
        sub = SUBSCORE[t]
        if sub is None:
            continue
        yes = df[df[t] >= 0.5]["note_" + sub]
        no = df[df[t] < 0.5]["note_" + sub]
        rows.append(dict(Thema=LABEL[t], Teilnote=SUB_DE[sub], note_mit_beschwerde=yes.mean(),
                         note_ohne_beschwerde=no.mean(), n_mit=len(yes)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Entscheid 3
KEYWORDS = {  # einfache Stichwort-Methode als Vergleich ("Baseline")
    "complaint": r"\b(but|however|unfortunately|disappoint|dirty|rude|noisy|broken|poor|terrible|worst|not worth|complain)",
    "staff_service": r"\b(rude|unfriendly|unhelpful|staff (was|were) (not|un)|poor service|bad service|attitude)",
    "checkin_booking": r"\b(check[- ]?in took|reservation|booked .* (but|got)|overbook|not ready|charged|billing|wrong room)",
    "cleanliness": r"\b(dirty|filthy|stain|smell|smelly|musty|mold|mould|dust|hair|not clean|unclean|grime)",
    "pests": r"\b(bed ?bugs?|cockroach|roach|mice|mouse|ants|pests?)\b",
    "room_condition": r"\b(old|outdated|dated|worn|run[- ]?down|shabby|tired|broken|didn't work|did not work|needs? (an )?(update|renovat))",
    "room_size": r"\b(tiny|small room|cramped|too small|shoebox)",
    "bathroom_plumbing": r"\b(shower|water pressure|hot water|toilet|drain|plumbing)",
    "ac_heating": r"\b(a/?c|air ?con\w*|heater|heating|too hot|too cold|freezing)",
    "noise": r"\b(noise|noisy|loud|thin walls|could hear)",
    "bed_comfort": r"\b(uncomfortable bed|hard bed|mattress|pillows?)\b",
    "price_value": r"\b(overpriced|over priced|expensive|not worth|fees?|pricey|resort fee)",
    "food_breakfast": r"\b(breakfast|restaurant|food|bar)\b",
    "wifi": r"\b(wi-?fi|internet)\b",
    "parking": r"\b(parking|valet)\b",
    "location_safety": r"\b(unsafe|sketchy|dangerous|far from|homeless|bad area|bad neighbo)",
    "facilities": r"\b(pool|gym|fitness|elevators?|lifts?|lobby|spa)\b",
}


def keyword_codes(df):
    import warnings
    warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")
    txt = (df.title_masked.fillna("") + " " + df.text_masked.fillna("")).str.lower()
    return pd.DataFrame({t: txt.str.contains(rx, regex=True).astype(int) for t, rx in KEYWORDS.items()},
                        index=df.index)


def metrics(y, pred):
    y, pred = np.asarray(y), np.asarray(pred)
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else np.nan
    rec = tp / (tp + fn) if tp + fn else np.nan
    f1 = 2 * prec * rec / (prec + rec) if prec and rec else np.nan
    return dict(TP=tp, FP=fp, FN=fn, TN=tn, genauigkeit=(tp + tn) / len(y),
                praezision=prec, trefferquote=rec, f1=f1)


def decision3(df):
    gold = pd.read_csv(os.path.join(DATA, "gold_100_claude.csv"))
    m = gold.merge(df, on="review_id", suffixes=("_ref", ""))
    kw = keyword_codes(m)
    rows = []
    for t in THEMES:
        j = metrics(m[t + "_ref"], (m[t] >= 0.5).astype(int))
        k = metrics(m[t + "_ref"], kw[t])
        rows.append(dict(thema=t, Thema=LABEL[t], ref_ja=int(m[t + "_ref"].sum()),
                         **{"jev_" + a: b for a, b in j.items()},
                         kw_praezision=k["praezision"], kw_trefferquote=k["trefferquote"], kw_f1=k["f1"],
                         unsicher=((m[t] > NO) & (m[t] < YES)).mean()))
    res = pd.DataFrame(rows)
    # Stabilitaet: zweiter Durchlauf auf 200 Bewertungen
    a = pd.read_csv(os.path.join(DATA, "jev_results.csv"))
    b = pd.read_csv(os.path.join(DATA, "jev_rerun_200.csv"))
    ab = a.merge(b, on="review_id", suffixes=("_1", "_2"))
    flips = sum(int(((ab[t + "_1"] >= .5) != (ab[t + "_2"] >= .5)).sum()) for t in THEMES)
    maxdiff = max(float((ab[t + "_1"] - ab[t + "_2"]).abs().max()) for t in THEMES)
    stab = dict(entscheide=len(ab) * len(THEMES), gekippt=flips, max_abweichung=maxdiff)
    # Gesamtwerte ueber alle Themen (ohne 'complaint')
    tot = {}
    for who, cols in [("JEV", None), ("Stichwoerter", None)]:
        y = np.concatenate([m[t + "_ref"].values for t in TOPICS])
        if who == "JEV":
            p = np.concatenate([(m[t] >= .5).astype(int).values for t in TOPICS])
        else:
            p = np.concatenate([kw[t].values for t in TOPICS])
        tot[who] = metrics(y, p)
    return res, stab, tot, m


def complaint_by_stars(df):
    g = df.groupby("overall")["complaint"]
    return pd.DataFrame({"n": g.size(), "anteil_beschwerde": g.apply(lambda p: (p >= .5).mean()),
                         "anteil_unsicher": g.apply(lambda p: ((p > NO) & (p < YES)).mean())})


# ---------------------------------------------------------------- Grafiken
def _style(ax):
    ax.set_facecolor(SURFACE)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.tick_params(colors=INK2, length=0)
    ax.xaxis.grid(True, color="#e6e4df", linewidth=0.8)
    ax.set_axisbelow(True)


def fig1(d1, path):
    """Was stoert unzufriedene Gaeste? Anteil + Bandbreite, Farbe = abgefragt ja/nein."""
    d = d1.head(12).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 6), dpi=200, facecolor=SURFACE)
    _style(ax)
    col = [ORANGE if t == "- (nicht abgefragt)" else BLUE for t in d.Teilnote]
    y = np.arange(len(d))
    ax.barh(y, d.anteil_unzufrieden * 100, color=col, height=0.62)
    ax.errorbar(d.anteil_unzufrieden * 100, y,
                xerr=[(d.anteil_unzufrieden - d.von) * 100, (d.bis - d.anteil_unzufrieden) * 100],
                fmt="none", ecolor=INK2, elinewidth=1.2, capsize=3)
    for yi, (v, hi) in enumerate(zip(d.anteil_unzufrieden, d.bis)):
        ax.text(hi * 100 + 1, yi, f"{v*100:.0f}%", va="center", color=INK, fontsize=9)
    ax.set_yticks(y, d.Thema, color=INK, fontsize=10)
    ax.set_xlabel("Anteil der unzufriedenen Gäste (1–2 Sterne), die das Thema nennen", color=INK2)
    ax.set_xlim(0, max(d.bis) * 100 + 10)
    n = int(d1.n.iloc[0])
    fig.suptitle("Was stört unzufriedene Gäste am meisten?", x=0.02, ha="left", fontsize=14, color=INK, weight="bold")
    ax.set_title(f"{n} Bewertungen mit 1–2 Sternen · Strich = ehrliche Bandbreite", loc="left", color=INK2, fontsize=10)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label="heute NICHT als Teilnote abgefragt"),
                       Patch(color=BLUE, label="über eine Teilnote abgefragt")],
              loc="lower right", frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def fig2(d2, path):
    """Sterne-Abzug, den die 5 Teilnoten nicht erklaeren."""
    d = d2.sort_values("sterne_effekt", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 6), dpi=200, facecolor=SURFACE)
    _style(ax)
    y = np.arange(len(d))
    col = [ORANGE if not a else BLUE for a in d.abgefragt]
    ax.barh(y, -d.sterne_effekt, color=col, height=0.62)
    ax.errorbar(-d.sterne_effekt, y, xerr=[(d.bis - d.sterne_effekt), (d.sterne_effekt - d.von)],
                fmt="none", ecolor=INK2, elinewidth=1.2, capsize=3)
    for yi, (v, lo) in enumerate(zip(d.sterne_effekt, d.von)):
        ax.text(max(-lo, 0) + 0.01, yi, f"{-v:.2f} Sterne weniger" if v < 0 else f"{v:.2f} Sterne mehr",
                va="center", color=INK, fontsize=8.5)
    ax.set_yticks(y, d.Thema, color=INK, fontsize=10)
    ax.axvline(0, color=GREY, lw=1)
    ax.set_xlim(-0.25, 0.85)
    ax.set_xlabel("Sterne-Abzug in der Gesamtnote, wenn das Thema vorkommt – bei gleichen Teilnoten", color=INK2)
    fig.suptitle("Was die fünf Teilnoten übersehen", x=0.02, ha="left", fontsize=14, color=INK, weight="bold")
    ax.set_title("Grosser Balken = Gäste ziehen Sterne ab, obwohl die Teilnoten es nicht zeigen",
                 loc="left", color=INK2, fontsize=10)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label="heute NICHT abgefragt"),
                       Patch(color=BLUE, label="über eine Teilnote abgefragt")],
              loc="lower right", frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def fig3(d3, path):
    """Wie gut erkennt JEV Beschwerden? Pro Thema: erkannt / uebersehen / Fehlalarm (von 100 geprueften)."""
    d = d3[(d3.ref_ja >= 7) & (d3.thema != "complaint")].copy()
    d = d.sort_values("jev_f1").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9, 6.4), dpi=200, facecolor=SURFACE)
    _style(ax)
    y = np.arange(len(d))
    ax.barh(y, d.jev_TP, color=BLUE, height=0.62, label="richtig erkannt")
    ax.barh(y, d.jev_FN, left=d.jev_TP + 0.4, color=GREY, height=0.62, label="übersehen")
    ax.barh(y, d.jev_FP, left=d.jev_TP + d.jev_FN + 0.8, color=ORANGE, height=0.62, label="Fehlalarm")
    for yi, r in d.iterrows():
        ax.text(r.jev_TP + r.jev_FN + r.jev_FP + 1.6, yi,
                f"{r.jev_trefferquote*100:.0f}% erkannt · {r.jev_praezision*100:.0f}% Meldungen stimmen",
                va="center", color=INK2, fontsize=8.5)
    ax.set_yticks(y, d.Thema, color=INK, fontsize=10)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Anzahl Bewertungen in der Kontrollstichprobe (100 Bewertungen)", color=INK2)
    fig.suptitle("Wie zuverlässig erkennt das KI-Werkzeug Beschwerden?", x=0.02, ha="left", fontsize=14, color=INK, weight="bold")
    ax.set_title("JEV im Vergleich mit einer unabhängigen Codierung derselben 100 Bewertungen",
                 loc="left", color=INK2, fontsize=10)
    ax.legend(loc="lower right", frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def run_all(save=True):
    df = load()
    d1 = decision1(df)
    d2, fit = decision2(df)
    d3, stab, tot, _ = decision3(df)
    if save:
        os.makedirs(OUT, exist_ok=True)
        fig1(d1, os.path.join(OUT, "grafik1_themen_unzufriedene.png"))
        fig2(d2, os.path.join(OUT, "grafik2_teilnoten_luecken.png"))
        fig3(d3, os.path.join(OUT, "grafik3_ki_zuverlaessigkeit.png"))
        d1.to_csv(os.path.join(OUT, "entscheid1_themen.csv"), index=False)
        d2.to_csv(os.path.join(OUT, "entscheid2_regression.csv"), index=False)
        d3.to_csv(os.path.join(OUT, "entscheid3_ki_pruefung.csv"), index=False)
    return df, d1, d2, fit, d3, stab, tot


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    df, d1, d2, fit, d3, stab, tot = run_all()
    print(d1.round(3).to_string())
    print(d2.round(3).to_string()); print(fit)
    print(convergent_validity(df).round(2).to_string())
    print(d3[["Thema", "ref_ja", "jev_genauigkeit", "jev_praezision", "jev_trefferquote", "jev_f1", "kw_praezision", "kw_trefferquote", "kw_f1", "unsicher"]].round(2).to_string())
    print(stab); print(tot)
    print(complaint_by_stars(df).round(3))
