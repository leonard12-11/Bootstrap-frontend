"""Schickt jede Bewertung mit allen Codebuch-Fragen an JEV und speichert die Antworten.

Aufruf:  TYPESAFE_API_KEY=... python src/run_jev.py data/sample_5000.csv data/jev_results.csv
Bereits beantwortete Bewertungen werden uebersprungen (Cache), ein Abbruch ist also kein Problem.
"""
import asyncio, csv, os, sys, time
import pandas as pd
from typesafe_sdk import AsyncTypeSafeClient, Noul

sys.path.insert(0, os.path.dirname(__file__))
from codebook import THEMES

CONCURRENCY = 16


def questions():
    return {k: Noul(instructions=v[2]) for k, v in THEMES.items()}


async def main(src, dst, id_col="review_id"):
    df = pd.read_csv(src)
    done = set(pd.read_csv(dst)[id_col]) if os.path.exists(dst) else set()
    todo = df[~df[id_col].isin(done)]
    print(f"{len(done)} schon fertig, {len(todo)} offen", flush=True)
    cols = [id_col, "model", "input_tokens"] + list(THEMES)
    new = not os.path.exists(dst)
    f = open(dst, "a", newline="")
    w = csv.writer(f)
    if new:
        w.writerow(cols)
    sem = asyncio.Semaphore(CONCURRENCY)
    n = 0
    t0 = time.time()
    async with AsyncTypeSafeClient(model="jev-latest") as client:
        async def one(row):
            nonlocal n
            async with sem:
                state = {"title": row.title_masked, "review": row.text_masked}
                r = await client.system_one(state=state, questions=questions())
            w.writerow([row[id_col], r.model, r.usage.input_tokens] + [round(r.nouls[k].noul, 4) for k in THEMES])
            n += 1
            if n % 250 == 0:
                f.flush()
                print(f"{n}/{len(todo)}  {time.time()-t0:.0f}s", flush=True)
        await asyncio.gather(*(one(r) for _, r in todo.iterrows()))
    f.close()
    print("fertig", n, flush=True)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
