import cv2
import tensorflow as tf
import numpy as np
import os
import csv
from tensorflow.keras.models import load_model
from tkinter import Tk, filedialog


# 1. Configurações
modelo_path = 'modelo_batatas_finetuned.keras'
pasta_teste = 'imagens_teste'
arquivo_csv_padrao = 'relatorio_inspecao_batatas_v2.csv'
class_names = ['Doente', 'Saudavel'] 

print("Carregando o sistema V3...")
model = load_model(modelo_path)

dados_exportacao = [['ID_Imagem', 'Status_Inspecao', 'Grau_de_Confianca_Pct']]

print("Iniciando inspeção...")
for nome_imagem in os.listdir(pasta_teste):
    caminho_imagem = os.path.join(pasta_teste, nome_imagem)
    
    if not nome_imagem.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Leitura e conversão de cores
    imagem = cv2.imread(caminho_imagem)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB) 
    imagem_resized = cv2.resize(imagem, (224, 224))
    
    # Formatação
    imagem_array = np.expand_dims(imagem_resized, axis=0)

    # Predição
    prediction = model.predict(imagem_array, verbose=0)
    index = np.argmax(prediction)
    classe_detectada = class_names[index]
    acuracia = prediction[0][index] * 100

    dados_exportacao.append([nome_imagem, classe_detectada, f"{acuracia:.2f}"])
    print(f"[{nome_imagem}] -> {classe_detectada} ({acuracia:.1f}%)")

# Função para escolher local de salvamento
def escolher_local_salvamento():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    root.attributes('-topmost', True)  # Mantém a janela de diálogo no topo
    
    arquivo_csv = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        title="Salvar Relatório de Inspeção",
        initialfile=arquivo_csv_padrao
    )
    
    root.destroy()
    return arquivo_csv

# Escolher local de salvamento
print("\nEscolhendo local para salvar o relatório...")
arquivo_csv = escolher_local_salvamento()

if arquivo_csv:  # Só salva se o usuário não cancelou
    with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(dados_exportacao)
    
    print(f"\nRelatório salvo com sucesso: {arquivo_csv}")
else:
    print("\nSalvamento cancelado pelo usuário.")