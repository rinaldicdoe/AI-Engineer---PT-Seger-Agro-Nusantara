from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB = DATA / "retail_bi.db"

def main():
    con = sqlite3.connect(DB)
    for name in ["orders", "products", "channel_targets"]:
        df = pd.read_csv(DATA / f"{name}.csv")
        df.to_sql(name, con, if_exists="replace", index=False)
        print(f"loaded {name}: {len(df)} rows")
    con.close()
    print(f"Database created: {DB}")

if __name__ == "__main__":
    main()
