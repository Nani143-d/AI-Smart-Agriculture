# Machine-learning model files

The project intentionally does not ship fabricated `.h5` or `.pkl` files.

- `disease_model.h5`: add a genuinely trained TensorFlow/Keras model. The example loader expects RGB images resized to 224x224 and normalized to [0, 1]. Configure class labels in `agriculture/utils/disease_detection.py` to match your training order.
- `yield_model.pkl`: create this with `python train_yield_model.py` after installing dependencies and preparing a CSV dataset.

Model quality depends on the dataset, training procedure, and validation. Do not use demo outputs as agronomic advice.
