import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, RandomFlip, RandomRotation, RandomZoom, Input, Dropout, Rescaling
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# 1. Configurações Iniciais
pasta_dataset = 'dataset' 
tamanho_imagem = (224, 224)
batch_size = 32

print("Carregando datasets...")
train_dataset = image_dataset_from_directory(
    pasta_dataset, validation_split=0.2, subset="training", seed=42,
    image_size=tamanho_imagem, batch_size=batch_size
)
validation_dataset = image_dataset_from_directory(
    pasta_dataset, validation_split=0.2, subset="validation", seed=42,
    image_size=tamanho_imagem, batch_size=batch_size
)

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.cache().prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)

# 2. Data Augmentation
data_augmentation = tf.keras.Sequential([
  RandomFlip('horizontal_and_vertical'),
  RandomRotation(0.2),
  RandomZoom(0.2),
])

# 3. Construindo a Arquitetura Base
inputs = Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = Rescaling(scale=1./127.5, offset=-1)(x)

base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False # Começamos com ele congelado

x = base_model(x, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(2, activation='softmax')(x) 

model = Model(inputs, outputs)

# ---------------------------------------------------------
# FASE 1: Aquecimento (Treinar apenas a nossa camada final)
# ---------------------------------------------------------
print("\n--- INICIANDO FASE 1: AQUECIMENTO ---")
model.compile(optimizer=Adam(learning_rate=0.001), 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])


model.fit(train_dataset, validation_data=validation_dataset, epochs=5)

# ---------------------------------------------------------
# FASE 2: Fine-Tuning
# ---------------------------------------------------------
print("\n--- INICIANDO FASE 2: FINE-TUNING ---")
base_model.trainable = True

# O MobileNetV2 tem 154 camadas. Vamos deixar as 100 primeiras congeladas
# e permitir que as 54 camadas finais aprendam a textura da batata.
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=0.0001), 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

# Callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=1, min_lr=1e-6)

history_fine = model.fit(
    train_dataset, 
    validation_data=validation_dataset, 
    epochs=15, # Para sozinho se começar a piorar
    callbacks=[early_stop, reduce_lr]
)

# Salvar o modelo supremo
model.save('modelo_batatas_finetuned.keras')
print("\nModelo Fine-Tuned salvo com sucesso como 'modelo_batatas_finetuned.keras'!")