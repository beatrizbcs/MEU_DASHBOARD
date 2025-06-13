import pandas as pd
import numpy as np
from pathlib import Path
import random
random.seed(42)
np.random.seed(42)

n = 300

anos   = np.random.randint(2005, 2025, n)
tipos  = np.random.choice(
    ["Homicídio", "Roubo", "Estupro", "Fraude", "Lesão corporal"], n)
exames = np.random.choice(
    ["Identificação dental", "Marca de mordida", "Estimativa de idade", "DNA dentário"], n)

idades = np.random.randint(5, 90, n)
ferim  = np.random.poisson(2, n)
resolv = np.random.choice([0, 1], n, p=[0.4, 0.6])  # 60 % resolvidos

df = pd.DataFrame({
    "id": range(1, n+1),
    "ano": anos,
    "tipo": tipos,
    "exame_odontologico": exames,
    "idade_vitima": idades,
    "qtd_ferimentos": ferim,
    "resolvido": resolv
})

Path("data").mkdir(exist_ok=True)
df.to_csv("data/crimes.csv", index=False)

print("✨ Arquivo data/crimes.csv criado com", len(df), "linhas!")