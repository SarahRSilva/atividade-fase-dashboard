# 🥔 AgroSmart — Inspeção Inteligente de Batatas

Projeto desenvolvido para o curso de Engenharia de Software (FIAP — Turma 4ESOA) que aplica **visão computacional** e **análise de dados** ao agronegócio, com foco no controle de qualidade de batatas.

O sistema é dividido em duas fases complementares:

- **Fase 1 — Classificação por Imagem**: modelo de IA (TensorFlow/Keras com MobileNetV2 + fine-tuning) que classifica imagens de batatas como **Saudáveis** ou **Doentes**, gerando relatórios em CSV.
- **Fase 2 — Dashboard Analítico**: painel interativo em Streamlit que consome os relatórios da Fase 1, enriquece com metadados de campo (localidade, talhão, data) e apresenta visualizações para apoio à tomada de decisão do agricultor.

---

## 📁 Estrutura do Projeto

```
atividade-fase-dashboard/
│
├── 🧠 FASE 1 — Modelo de Visão Computacional
│   ├── treinamento_com_finetuning.py    # Treina o modelo (transfer learning + fine-tuning)
│   ├── classificacao_exporte.py         # Classifica imagens em lote e exporta CSV
│   ├── modelo_batatas_finetuned.keras   # Modelo treinado pronto para uso
│   └── metricas_avaliacao.ipynb         # Notebook com métricas de avaliação
│
├── 📊 FASE 2 — Dashboard Analítico
│   ├── dashboard.py                     # Aplicação Streamlit (dashboard interativo)
│   ├── enriquecer_csv.py                # Enriquece CSV da Fase 1 com metadados
│   ├── dados/
│   │   └── inspecoes.csv                # Base de dados consumida pelo dashboard
│   └── relatorio_inspecao_batatas_v2.csv # Exemplo de relatório gerado pela Fase 1
│
├── 📦 Configuração
│   ├── requirements_fase2.txt           # Dependências do dashboard
│   └── README.md
│
└── 🗂️ Pastas locais (não versionadas)
    ├── dataset/                         # Imagens de treino (Doente / Saudavel)
    └── imagens_teste/                   # Imagens para classificação em lote
```

---

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.12**
- pip atualizado

### 1. Instalar dependências

Para a **Fase 1** (treino e classificação):
```bash
pip install tensorflow streamlit opencv-python pillow numpy
```

Para a **Fase 2** (dashboard):
```bash
pip install -r requirements_fase2.txt
```

### 2. Executar o Dashboard (Fase 2)

```bash
streamlit run dashboard.py
```

O dashboard abre automaticamente em `http://localhost:8501`.

### 3. Gerar novos dados a partir de imagens (Fase 1)

```bash
# 1. Coloque imagens em imagens_teste/
# 2. Execute a classificação em lote
python classificacao_exporte.py

# 3. Enriqueça o CSV gerado com metadados de campo
python enriquecer_csv.py

# 4. O dashboard já está pronto para consumir os novos dados
```

---

## 📊 Fase 2 — Dashboard Analítico

### Funcionalidades

O dashboard transforma os relatórios técnicos da Fase 1 em informação acionável para o agricultor:

| Visualização | O que mostra |
|---|---|
| 🖼️ **KPIs principais** | Total de imagens analisadas, % de saudáveis, % de doentes, confiança média do modelo |
| 🥧 **Distribuição geral** | Gráfico de pizza com proporção saudável vs. doente |
| 📊 **Tipos de doença** | Frequência de cada doença detectada |
| 📈 **Tendência temporal** | Evolução das inspeções nos últimos 90 dias |
| 🗺️ **Heatmap por localidade** | Taxa de doença cruzando localidade × talhão |
| 💡 **Alertas automáticos** | Recomendações geradas com base em limiares críticos |

### Filtros interativos

A barra lateral permite refinar a análise por:
- **Localidade** (multi-seleção)
- **Talhão** (multi-seleção)
- **Confiança mínima do modelo** (slider 0-100%)

### Atualização de dados

O dashboard suporta duas fontes:

1. **Padrão**: lê o arquivo `dados/inspecoes.csv`
2. **Upload**: o agricultor pode subir um novo CSV pelo painel lateral, permitindo análise instantânea de novas inspeções vindas da Fase 1

### Formato esperado do CSV

O arquivo deve usar **`;`** como separador e conter as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `ID_Imagem` | string | Nome do arquivo de imagem |
| `Status_Inspecao` | `Doente` ou `Saudavel` | Resultado da classificação |
| `Grau_de_Confianca_Pct` | float (0-100) | Confiança do modelo |
| `Data_Inspecao` | datetime | Data e hora da inspeção |
| `Localidade` | string | Fazenda / propriedade |
| `Talhao` | string | Identificador do talhão |
| `Tipo_Doenca` | string | Doença detectada (ou `N/A` se saudável) |
| `Lote` | string | Identificador do lote de produção |

---

## 🧠 Fase 1 — Modelo de Visão Computacional

### Arquitetura

- **Backbone**: MobileNetV2 (pré-treinado em ImageNet)
- **Estratégia**: Transfer Learning + Fine-tuning em duas etapas
- **Classes**: `Doente`, `Saudavel`
- **Output**: probabilidade por classe (softmax)

### Treinar o modelo

```bash
# 1. Organize o dataset:
#    dataset/Doente/      (imagens de batatas doentes)
#    dataset/Saudavel/    (imagens de batatas saudáveis)

# 2. Execute o treinamento:
python treinamento_com_finetuning.py
```

O fluxo:
- **Etapa 1**: 5 épocas treinando apenas as camadas finais (head)
- **Etapa 2**: até 15 épocas com fine-tuning das camadas finais do MobileNetV2
- **Callbacks**: `EarlyStopping` + `ReduceLROnPlateau`
- **Saída**: `modelo_batatas_finetuned.keras`

### Classificação em lote

```bash
python classificacao_exporte.py
```

Lê todas as imagens em `imagens_teste/` (jpg/jpeg/png), classifica cada uma e gera um CSV de relatório com `ID_Imagem`, `Status_Inspecao` e `Grau_de_Confianca_Pct`.

> ⚠️ Este script usa `tkinter` para escolher onde salvar o CSV. Não funciona em ambientes headless (servidores sem GUI).

### Dataset utilizado

[Fruit and Vegetable Disease (Healthy vs Rotten) — Kaggle](https://www.kaggle.com/datasets/muhammad0subhan/fruit-and-vegetable-disease-healthy-vs-rotten)

---

## 🎬 Vídeo Explicativo

📺 **Assista à demonstração completa**: [LINK DO VÍDEO AQUI]

O vídeo (2-4 min) cobre:
- Apresentação do projeto AgroSmart
- Demonstração ao vivo do dashboard
- Insights acionáveis para o agricultor (ex: priorização de talhões para tratamento, identificação de surtos de doença)
- Fluxo Fase 1 → Fase 2 (do modelo ao dashboard)

---

## 🔧 Personalização

### Adicionar novas classes ao modelo
1. Crie subpastas adicionais em `dataset/`
2. Altere a última camada Dense em `treinamento_com_finetuning.py`:
   ```python
   Dense(N, activation='softmax')  # N = número de classes
   ```
3. Atualize a lista `class_names` nos scripts

### Trocar o backbone
Substitua `MobileNetV2` por outro modelo (ResNet50, EfficientNetB0, etc.) e ajuste o pré-processamento conforme necessário.

### Ajustar hiperparâmetros
- **Épocas**: parâmetro `epochs` em `model.fit()`
- **Learning rate**: parâmetro de `Adam(learning_rate=...)`
- **Data augmentation**: edite a sequência `data_augmentation`

---

## 👥 Equipe

| Nome | RM | Turma |
|---|---|---|
| Gabriel Genaro Dalaqua | 551986 | 4ESOA |
| Alairton Rocha Scabelli | 551454 | 4ESOA |
| Carolina Nascimento Amorim | 97930 | 4ESOA |
| Eduardo Marins | 551892 | 4ESOA |
| Sarah Ribeiro da Silva | 97747 | 4ESOA |

---

## 📚 Tecnologias

**Fase 1**: Python • TensorFlow • Keras • OpenCV • Pillow • NumPy

**Fase 2**: Python • Streamlit • Pandas • Plotly

---

**Projeto desenvolvido para a disciplina de PBL — FIAP 2026**
