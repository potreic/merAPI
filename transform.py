import os
import json
from datetime import datetime
from fetch import magmalevelonly
import pytz

def transform_merapi(volcano="Merapi"):
    data = magmalevelonly()

    result = {}
    jakarta = pytz.timezone("Asia/Jakarta")
    timestamp = datetime.now(jakarta).strftime("%d-%m-%Y %H:%M")

    for level, volcanos in data.items():
        if volcano in volcanos:
            entry = volcanos[volcano]
            result[volcano] = {
                "Status": level,
                "location": entry["location"],
                "link": entry["link"],
                "timestamp": timestamp
            }
            break

    if not result:
        raise ValueError(f"Volcano '{volcano}' not found in fetched data")

    # Write ONLY data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[✓] Merapi data updated at {timestamp}")
    return result

if __name__ == "__main__":
    clean = transform_merapi()
