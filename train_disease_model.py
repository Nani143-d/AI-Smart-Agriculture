from pathlib import Path
import json
import tensorflow as tf

# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

# Dataset contains disease-class folders inside "color"
DATASET_DIR = (
    BASE_DIR
    / "agriculture"
    / "ml_models"
    / "archive"
    / "PlantVillage"
    / "color"
)

MODEL_DIR = BASE_DIR / "agriculture" / "ml_models"

MODEL_PATH = MODEL_DIR / "disease_model.keras"
LABELS_PATH = MODEL_DIR / "disease_labels.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
SEED = 42

# =========================================================
# 2. DISPLAY PROJECT INFORMATION
# =========================================================

print("=" * 60)
print("       AI SMART AGRICULTURE")
print("       PLANT DISEASE MODEL TRAINING")
print("=" * 60)

print(f"\nDataset location:\n{DATASET_DIR}")

# =========================================================
# 3. CHECK DATASET
# =========================================================

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        "\nDataset folder not found!\n"
        f"Expected location: {DATASET_DIR}\n\n"
        "Please check the dataset folder location."
    )

# Find class folders
class_folders = sorted(
    folder
    for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
)

if len(class_folders) < 2:
    raise ValueError(
        "\nAt least two disease/healthy class folders are required.\n"
        f"Found {len(class_folders)} class folders in:\n"
        f"{DATASET_DIR}"
    )

# Check that the class folders contain image files
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

valid_classes = []

for folder in class_folders:
    image_count = sum(
        1
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in image_extensions
    )

    if image_count > 0:
        valid_classes.append(folder)
        print(f"{folder.name}: {image_count} images")

if len(valid_classes) < 2:
    raise ValueError(
        "Fewer than two class folders contain images. "
        "Please check your dataset."
    )

print("\nNumber of valid classes:", len(valid_classes))

# =========================================================
# 4. LOAD TRAINING AND VALIDATION DATA
# =========================================================

print("\nLoading training images...")

train_data = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    labels="inferred",
    label_mode="int",
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_names=[folder.name for folder in valid_classes]
)

print("\nLoading validation images...")

validation_data = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    labels="inferred",
    label_mode="int",
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_names=[folder.name for folder in valid_classes]
)

# Get class names in the exact order used by TensorFlow
class_names = train_data.class_names
number_of_classes = len(class_names)

print("\nClasses detected:", number_of_classes)

for index, name in enumerate(class_names):
    print(f"{index}: {name}")

# =========================================================
# 5. OPTIMIZE DATA LOADING
# =========================================================

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(
    buffer_size=AUTOTUNE
)

validation_data = validation_data.prefetch(
    buffer_size=AUTOTUNE
)

# =========================================================
# 6. BUILD CNN MODEL
# =========================================================

print("\nBuilding CNN model...")

model = tf.keras.Sequential([
    tf.keras.layers.Input(
        shape=(224, 224, 3)
    ),

    # Normalize pixel values from 0-255 to 0-1
    tf.keras.layers.Rescaling(1.0 / 255),

    # Convolution block 1
    tf.keras.layers.Conv2D(
        32,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),
    tf.keras.layers.MaxPooling2D(),

    # Convolution block 2
    tf.keras.layers.Conv2D(
        64,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),
    tf.keras.layers.MaxPooling2D(),

    # Convolution block 3
    tf.keras.layers.Conv2D(
        128,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),
    tf.keras.layers.MaxPooling2D(),

    # Feature extraction
    tf.keras.layers.GlobalAveragePooling2D(),

    # Classification layers
    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.3),

    # One output for each plant disease class
    tf.keras.layers.Dense(
        number_of_classes,
        activation="softmax"
    )
])

# =========================================================
# 7. COMPILE MODEL
# =========================================================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================================================
# 8. PREPARE MODEL OUTPUT DIRECTORY
# =========================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Save labels before training so the class order is available
# even if training is interrupted.
with open(
    LABELS_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        class_names,
        file,
        indent=4
    )

# =========================================================
# 9. TRAIN MODEL
# =========================================================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=str(MODEL_PATH),
    monitor="val_loss",
    save_best_only=True,
    verbose=1
)

print("\n" + "=" * 60)
print("STARTING MODEL TRAINING")
print("Please wait. Training may take some time.")
print("=" * 60 + "\n")

history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=EPOCHS,
    callbacks=[
        early_stopping,
        checkpoint
    ]
)

# =========================================================
# 10. EVALUATE MODEL
# =========================================================

print("\nEvaluating model...")

loss, accuracy = model.evaluate(
    validation_data,
    verbose=1
)

print(f"\nValidation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy * 100:.2f}%")

# =========================================================
# 11. SAVE FINAL MODEL
# =========================================================

# Save the final model with the restored best weights.
model.save(MODEL_PATH)

with open(
    LABELS_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        class_names,
        file,
        indent=4
    )

# =========================================================
# 12. TRAINING COMPLETED
# =========================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nModel saved at:")
print(MODEL_PATH)

print("\nDisease labels saved at:")
print(LABELS_PATH)

print("\nTotal classes:", number_of_classes)
print(f"Validation accuracy: {accuracy * 100:.2f}%")

print("\nYour plant disease model is ready for integration!")