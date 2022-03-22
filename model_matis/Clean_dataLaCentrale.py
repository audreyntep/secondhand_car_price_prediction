import pandas as pd
import re

df = pd.read_csv('model_anouar/dataLaCentrale.csv', sep=',')
df["Kilométrage"] = df["Kilométrage"].replace(r"\D", "", regex=True)
df["Prix"] = df["Prix"].replace(r"\W", "", regex=True)
print(df)