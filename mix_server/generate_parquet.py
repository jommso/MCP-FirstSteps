# generate_parquet.py

import pandas as pd

# CSV lesen
df = pd.read_csv("data/sample.csv")

# Als Parquet speichern
df.to_parquet("data/sample.parquet", index=False)

print("Parquet-Datei erfolgreich erstellt!")
