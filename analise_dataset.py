import pandas as pd

# Carregar os dados
data = pd.read_csv('data/Car_Insurance_Claim.csv')

# Visualizar as primeiras linhas e a informação sobre os tipos de dados e valores faltantes
print(data.head())
print(data.info())
