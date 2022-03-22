import re
import pandas as pd

df = pd.read_csv('model_anouar/dataAuto.csv', sep=',')
#Supprime tout ce qui n'est pas alpha Numerique'
df["Kilométrage"] = df["Kilométrage"].str.replace("\W", '', regex=True)
#Supprime tout ce qui n'est pas alpha Numerique'
df["Prix"] = df["Prix"].str.replace("\W", '', regex=True)
print(df)

