# Projeto de Inspeção de Batatas com Visão Computacional

Este projeto utiliza inteligência artificial e visão computacional para classificar batatas como **"Saudáveis"** ou **"Doentes"** com base em imagens. Ele é construído com TensorFlow/Keras usando transfer learning (MobileNetV2 pré-treinado) e inclui: treinamento com fine-tuning, classificação em lote com exportação CSV e uma interface web simples em Streamlit.

---

## ✅ Estrutura Atual do Projeto

- `treinamento_com_finetuning.py`: treina o modelo (transfer learning + fine-tuning) e salva `modelo_batatas_finetuned.keras`
- `classificacao_exporte.py`: classifica imagens em `imagens_teste/` e exporta relatório CSV (usa `tkinter` para escolher destino)
- `app.py`: interface web Streamlit para classificar uma imagem por vez
- `modelo_batatas_finetuned.keras`: modelo treinado existente (pode ser substituído ao treinar novamente)
- `dataset/`: (não comitado) pasta com imagens de treino divididas em classes
- `imagens_teste/`: (não comitado) pasta com imagens para classificação em lote
- `old/`: histórico de modelos e relatórios antigos

---

## 🧰 Requisitos / Dependências

### Requisitos mínimos
- Python 3.12

### Dependências Python

```bash
pip install tensorflow streamlit opencv-python pillow numpy
```

> ⚠️ O script `classificacao_exporte.py` usa `tkinter` (incluído no Python padrão em Windows/macOS/Linux). Em ambientes headless (servidores sem GUI) ele não funcionará.

---

## 🧠 Como Treinar o Modelo (Fine-Tuning)

1. Prepare o dataset conforme a seção **Dataset** abaixo.
2. Execute:

```bash
python treinamento_com_finetuning.py
```

O fluxo do script:
- **Fase 1**: treina apenas as camadas finais (cabeça) por 5 épocas
- **Fase 2**: descongela parte do MobileNetV2 para fine-tuning (até 15 épocas) com callbacks de `EarlyStopping` e `ReduceLROnPlateau`
- O modelo final é salvo como `modelo_batatas_finetuned.keras`

---

## 🗂️ Classificação em Lote (Relatório CSV)

Para classificar todas as imagens na pasta `imagens_teste/` e gerar um relatório:

```bash
python classificacao_exporte.py
```

O que o script faz:
- Carrega `modelo_batatas_finetuned.keras`
- Lê todas as imagens em `imagens_teste/` (jpg/jpeg/png)
- Classifica cada imagem e gera um relatório com:
  - **ID_Imagem** (nome do arquivo)
  - **Status_Inspecao** (Doente/Saudavel)
  - **Grau_de_Confianca_Pct**
- Pede para você escolher onde salvar o arquivo CSV (interface gráfica via `tkinter`)
- O CSV usa `;` como separador

---

## 🖥️ Aplicação Web (Streamlit)

Para rodar a interface web:

```bash
streamlit run app.py
```

O app oferece:
- Upload de imagem (JPG/JPEG/PNG)
- Exibição da imagem carregada
- Classificação em tempo real (Doente / Saudável)
- Exibição do grau de confiança em % com barra de progresso

> Observação: o app não gera relatório CSV, apenas mostra o resultado na tela.

---

## 🧩 Dataset (Organização)

Crie a estrutura abaixo para treinar o modelo (não incluído no repositório):

```
dataset/
├── Doente/     # imagens de batatas doentes
└── Saudavel/   # imagens de batatas saudáveis
```

Para testes de classificação em lote, coloque imagens em:

```
imagens_teste/
```

---

## 🧪 Classes e Nomes Usados

O projeto utiliza estas classes (mapeadas pelo índice de saída do modelo):

- `Doente`
- `Saudavel`

### Se quiser adicionar classes
- Edite as pastas em `dataset/`
- Altere a última camada Dense: `Dense(2, activation='softmax')` → `Dense(N, activation='softmax')`
- Atualize a lista `class_names` nos scripts para refletir as novas classes

---

## 🔧 Ajustes / Personalizações comuns

### Ajustar hiperparâmetros
- **Épocas**: modifique `epochs` em `model.fit()` (ambos os blocos)
- **Learning rate**: altere `Adam(learning_rate=...)`
- **Data augmentation**: edite a sequência em `data_augmentation` (flip/rotation/zoom)

### Trocar o backbone do modelo
Substitua `MobileNetV2` por outro modelo (ResNet50, EfficientNet, etc.) e ajuste pré-processamento conforme necessário.

---

## Dataset Kaggle

https://www.kaggle.com/datasets/muhammad0subhan/fruit-and-vegetable-disease-healthy-vs-rotten

## 🗂️ Estrutura Recomendada (Resumo)

```
ProjetoFase1Batatas/
├── app.py
├── treinamento_com_finetuning.py
├── classificacao_exporte.py
├── modelo_batatas_finetuned.keras
├── dataset/         # Não comitado (contém dados de treino)
└── imagens_teste/   # Não comitado (contém imagens para relatório)

```

---

## 👥 Contato

### Time

<table>
  <tr>
    <th>Nome</th>
    <th>RM</th>
    <th>Turma</th>
  </tr>
  <tr>
    <td>Gabriel Genaro Dalaqua</td>
    <td>551986</td>
    <td>4ESOA</td>
  </tr>
  <tr>
    <td>Alairton Rocha Scabelli </td>
    <td>551454</td>
    <td>4ESOA</td>
  </tr>
  <tr>
    <td>Carolina Nascimento Amorim</td>
    <td>97930</td>
    <td>4ESOA</td>
  </tr>
  <tr>
    <td>Eduardo Marins</td>
    <td>551892</td>
    <td>4ESOA</td>
  </tr>
  <tr>
    <td>Sarah Ribeiro da Silva</td>
    <td>97747</td>
    <td>4ESOA</td>
  </tr>
</table>
