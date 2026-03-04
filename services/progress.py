LEVELS = ["Onthouden", "Begrijpen", "Toepassen", "Analyseren"]

def score_pct(row):
    return round(((row["kennen"] + row["kunnen"] + row["confidence"]) / 3) * 100)


def kleurklasse(pct):
    if pct < 40:
        return "bad"
    if pct < 70:
        return "warn"
    return "good"