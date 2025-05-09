import os
import json
from datetime import datetime

def transform_merapi(raw_dir="raw_data", output_dir="clean_data", volcano="Merapi"):

    files = sorted(f for f in os.listdir(raw_dir)
                   if f.startswith("raw_") and f.endswith(".json"))
    if not files:
        raise FileNotFoundError(f"No raw files found in {raw_dir}")
    latest = files[-1]
    raw_path = os.path.join(raw_dir, latest)

    with open(raw_path, encoding="utf-8") as f:
        data = json.load(f)

    result = {}
    for level, volcanos in data.items():
        if volcano in volcanos:
            entry = volcanos[volcano]
            
            ts_str = latest.replace("raw_", "").replace(".json", "")
            timestamp = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M-%S").isoformat()

            result[volcano] = {
                "Status": level,
                "location": entry["location"],
                "link": entry["link"],
                "timestamp": timestamp
            }
            break

    if not result:
        raise ValueError(f"Volcano '{volcano}' not found in {raw_path}")

    os.makedirs(output_dir, exist_ok=True)
    clean_filename = f"{volcano.lower()}_{ts_str}.json"
    clean_path = os.path.join(output_dir, clean_filename)
    # with open(clean_path, "w", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False, indent=2)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[✓] Clean data for '{volcano}' saved to {clean_path}")
    return result

if __name__ == "__main__":
    clean = transform_merapi()
