"""Stichprobe ziehen, Datenqualitaet pruefen, pseudonymisieren.

Aufruf: python src/prepare.py <pfad/train.parquet> data/sample_5000.csv
"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from privacy import mask

N = 5000
df = pd.read_parquet(sys.argv[1])
df["review_id"] = df.index  # Zeilennummer im Originaldatensatz = stabile ID
s = df.head(N).copy()       # Vorgabe Lehrperson: die ersten 5'000 Saetze

log = []
log.append(("Fehlende Werte", int(s.isna().sum().sum()), "keine Aktion"))
d = s.duplicated(["text"], keep="first")
log.append(("Doppelter Text", int(d.sum()), "entfernt (erste behalten)"))
s = s[~d]
bad = ~s[["overall","cleanliness","value","location","rooms","sleep_quality"]].isin([1,2,3,4,5]).all(axis=1)
log.append(("Note ausserhalb 1-5", int(bad.sum()), "entfernt"))
s = s[~bad]
short = s["text"].str.len() < 50
log.append(("Text < 50 Zeichen", int(short.sum()), "behalten, markiert"))
s["text_short"] = short

s["title_masked"] = s["title"].map(mask)
s["text_masked"] = s["text"].map(mask)
s["masked_changes"] = (s["text_masked"] != s["text"]) | (s["title_masked"] != s["title"])
log.append(("Texte mit maskierten Namen/Kontakten", int(s.masked_changes.sum()), "maskiert vor Versand"))

keep = ["review_id","overall","cleanliness","value","location","rooms","sleep_quality",
        "post_date","char","text_short","masked_changes","title_masked","text_masked"]
s[keep].to_csv(sys.argv[2], index=False)   # user_id und hotel_id werden NICHT gespeichert
pd.DataFrame(log, columns=["Problem","Anzahl Zeilen","Entscheid"]).to_csv(
    os.path.join(os.path.dirname(sys.argv[2]), "bereinigungsprotokoll.csv"), index=False)
print(pd.DataFrame(log)); print(len(s), "Zeilen gespeichert")
