from pathlib import Path
import json
import tensorflow as tf

BASE_DIR = Path(__file__).resolve().parent

# Dataset location shown in your VS Code screenshot
DATASET_DIR = (
    BASE_DIR
    / "agriculture"
    / "archive"
    / "PlantVillage"
)

MODEL_DIR = BASE_DIR / "agriculture" / "ml_models"

MODEL_PATH = MODEL_DIR / "disease_model.h5"
LABELS_PATH = MODEL_DIR / "disease_labels.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10


def main():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset folder not found: {DATASET_DIR}"
        )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading PlantVillage dataset...")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
    )

    class_names = train_ds.class_names

    print("Classes:", class_names)

    with open(LABELS_PATH, "w", encoding="utf-8") as file:
        json.dump(class_names, file, indent=4)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Rescaling(1.0 / 255),

        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(64, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(128, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(
            len(class_names),
            activation="softmax"
        ),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=3,
                restore_best_weights=True,
            )
        ],
    )

    model.save(MODEL_PATH)

    print("\nTraining completed!")
    print("Model saved:", MODEL_PATH)
    print("Labels saved:", LABELS_PATH)


if __name__ == "__main__":
    main()