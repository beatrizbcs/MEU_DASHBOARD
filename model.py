import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

df = pd.read_csv("data/crimes.csv")

X = df[["idade_vitima", "ano", "qtd_ferimentos"]]
y = df["resolvido"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

dump(rf, "modelo.joblib")
print("✅ Arquivo modelo.joblib criado com sucesso!")