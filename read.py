import pandas as pd

df = pd.read_excel("Liste_Kunden.xlsx", engine="openpyxl")

print(df.head())