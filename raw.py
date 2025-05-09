import os
import json
from datetime import datetime
from fetch import magmalevelonly

def load_and_save_raw(output_dir="raw_data"):
    
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    data = magmalevelonly()
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"raw_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[✓] Raw data saved to {filepath}")

def main():
    load_and_save_raw()

if __name__ == "__main__":
    main()
