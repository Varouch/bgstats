"""Převede export z BG Stats na kompaktní data.js pro web (index.html).

Použití: python build.py [cesta_k_exportu.json]
Bez argumentu vezme nejnovější BGStatsExport-*.json ve složce.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def latest_export():
    files = sorted(glob.glob(os.path.join(HERE, "BGStatsExport-*.json")), key=os.path.getmtime)
    if not files:
        sys.exit("Nenalezen žádný BGStatsExport-*.json")
    return files[-1]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else latest_export()
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    games = {
        g["id"]: {
            "n": g["name"],
            "t": g.get("urlThumb") or "",
            "c": bool(g.get("cooperative")),
            "x": bool(g.get("isExpansion")),
            "y": g.get("bggYear") or 0,
            "b": g.get("bggId") or 0,
        }
        for g in d["games"]
    }
    players = {p["id"]: p["name"] for p in d["players"]}
    locations = {l["id"]: l["name"] for l in d["locations"]}

    plays = []
    for p in d["plays"]:
        if p.get("ignored"):
            continue
        plays.append([
            p["playDate"][:16],
            p["gameRefId"],
            p.get("locationRefId") or 0,
            p.get("durationMin") or 0,
            # [hráč, vítěz, nový hráč]
            [[s["playerRefId"], 1 if s.get("winner") else 0, 1 if s.get("newPlayer") else 0]
             for s in p["playerScores"] if s.get("playerRefId")],
            [e["gameRefId"] for e in p.get("expansionPlays") or []],
        ])
    plays.sort(key=lambda r: r[0])

    out = {
        "me": d["userInfo"].get("meRefId", 1),
        "exportDate": d["userInfo"].get("exportDate", ""),
        "games": games,
        "players": players,
        "locations": locations,
        "plays": plays,
    }
    js = "window.BG = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
    with open(os.path.join(HERE, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)
    print(f"{os.path.basename(path)} -> data.js ({len(plays)} partií, {len(js) // 1024} kB)")


if __name__ == "__main__":
    main()
