import pandas as pd
import re

df = pd.read_csv("model_anouar/MarqueFR-automatique.csv", sep=',')
#Supprime tout ce qui n'est pas alpha Numerique'
df["Prix"] = df["Prix"].replace(r"\W", "", regex=True)
#Supprime tout ce qui n'est pas un chiffre'
df["Kilométrage"] = df["Kilométrage"].replace(r"\D", "", regex=True)
print(df)