# AI Smart Agriculture Platform (Django)

## Included modules
- User registration, login, logout
- Dashboard with current user's saved analyses
- Crop image upload and optional TensorFlow model loader
- Educational NPK review (not a dosage calculator)
- Crop yield estimation (demo baseline until a trained model is installed)
- Live city weather using OpenWeather API key
- Rule-based farmer assistant
- Django admin and SQLite database

## Run on Windows (VS Code terminal)
```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations agriculture
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations agriculture
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Live weather
Get an API key from OpenWeather and set it in your terminal before running the server.

PowerShell:
```powershell
$env:OPENWEATHER_API_KEY="YOUR_API_KEY"
python manage.py runserver
```
macOS/Linux:
```bash
export OPENWEATHER_API_KEY="YOUR_API_KEY"
python manage.py runserver
```

## Machine-learning model files
The repository does not include fabricated trained models. Read `agriculture/ml_models/README.md`.
For yield model training, prepare a CSV with columns:
`nitrogen,phosphorus,potassium,temperature,rainfall,yield_t_ha`
then run:
```bash
python train_yield_model.py path/to/your_crop_yield.csv
```
The generated model is saved to `agriculture/ml_models/yield_model.pkl`.

For disease detection, provide a genuinely trained Keras model at
`agriculture/ml_models/disease_model.h5` and configure class labels to match the model. The app explicitly reports when the model is missing.

## Notes
- SQLite is configured by default so the app starts without MySQL setup.
- For production, set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, configure allowed hosts, HTTPS, and a production database.
- This project is an educational starter. Verify all agricultural decisions with soil tests and local agricultural experts.
