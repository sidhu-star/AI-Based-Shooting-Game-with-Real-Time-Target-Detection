import csv
from pathlib import Path
from datetime import datetime

class Leaderboard:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("player,score,level,hits,misses,accuracy,date\n", encoding="utf-8")

    def add(self, player, score, level, hits, misses, accuracy):
        rows = self.rows()
        rows.append({
            "player": player,
            "score": str(score),
            "level": str(level),
            "hits": str(hits),
            "misses": str(misses),
            "accuracy": f"{accuracy:.1f}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        rows.sort(key=lambda r: int(r["score"]), reverse=True)
        rows = rows[:10]
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def rows(self):
        with self.path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
