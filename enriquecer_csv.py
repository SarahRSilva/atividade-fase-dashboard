import pandas as pd
import random
from datetime import datetime, timedelta

# Lê o CSV exportado pelo classificacao_exporte.py (separador ;)
df = pd.read_csv("relatorio_inspecao_batatas_v2.csv", sep=";")

localidades = ["Fazenda São João - Vacaria/RS", "Sítio Boa Vista - Ibiraiaras/RS",
               "Fazenda Santa Clara - Guarapuava/PR", "Sítio Três Pinheiros - Irati/PR"]
talhoes = ["T-01", "T-02", "T-03", "T-04", "T-05"]
tipos_doenca = ["Podridão mole", "Requeima", "Pinta preta", "Sarna comum"]

df["Data_Inspecao"] = [datetime.now() - timedelta(days=random.randint(0,90)) for _ in range(len(df))]
df["Localidade"] = [random.choice(localidades) for _ in range(len(df))]
df["Talhao"] = [random.choice(talhoes) for _ in range(len(df))]
df["Tipo_Doenca"] = df["Status_Inspecao"].apply(
    lambda s: random.choice(tipos_doenca) if s == "Doente" else "N/A"
)
df["Lote"] = [f"L{random.randint(1000,9999)}" for _ in range(len(df))]

df.to_csv("dados/inspecoes.csv", sep=";", index=False)
print(f"✅ {len(df)} inspeções enriquecidas e salvas")