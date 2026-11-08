---
title: LuntiAI Crop Model
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/703d41ec-1ffa-4580-a6b0-b9825fe04780" />


# LuntiAI — Precision Agriculture for Tagum City

> AI-powered crop recommendation system for farmers in Tagum City, Davao del Norte.
> Built for the Technopreneurship Academic Festival 2026.

## Live Demo

🚀 **Try LuntiAI online (Hugging Face Spaces):**
- **Web App UI:** [https://owaruurawo-luntiai-crop-model.hf.space/app](https://owaruurawo-luntiai-crop-model.hf.space/app)
- **API Base URL:** [https://owaruurawo-luntiai-crop-model.hf.space](https://owaruurawo-luntiai-crop-model.hf.space)

### Public demo privacy

The public demo uses aliases and non-sensitive usernames instead of phone numbers.
Use a unique throwaway password—never submit real personal information or a password
used on another service. Demo account data is stored in ephemeral container storage
and may disappear whenever the Space restarts.

---

## What is LuntiAI?

**LuntiAI** (*Luntian* + AI) is a classroom crop-classification prototype for
Tagum City. It uses a Random Forest trained on synthetic crop profiles. Selecting
a barangay fills editable soil presets and weather inputs; the model ranks crop
classes and TreeSHAP explains its scores. Field suitability has not been validated.

**Start here:** [Dataset, inference, and XAI defense guide](docs/LUNTIAI_EXPLAINED.md).
The guide separates source claims, implemented behavior, and measured results.

### Key Features
- **Mobile-First UX/UI** — Touch-optimized interface with thumb-zone bottom sheets and responsive breakpoints
- **Demo tiers** — Economic extras and history use demo tiers; complete XAI remains visible to free users
- **23 Tagum Barangay Profiles** — Editable soil presets, not farm measurements
- **Live Weather Integration** — Real-time temperature, humidity via OpenWeatherMap
- **Random Forest ML Model** — 85.62% accuracy on a synthetic test split; 120,000 generated rows total
- **12 Philippine Crops** — Rice, Banana, Cacao, Coconut, Durian, Corn, Mango, Papaya, Cassava, Sweet Potato, Eggplant, Tomato
- **Explainable AI (SHAP)** — Understand *why* the AI chose a crop with positive/negative impact factors
- **UI Localization** — Supports English, Tagalog, and Bisaya
- **Illustrative economics** — Rule-based cost and return estimates; not validated yield or profit predictions
- **Confidence Scoring** — Top-5 crop predictions with probability chart

---

## Quick Start

### Prerequisites
- Python 3.11 (tested; saved model requires scikit-learn 1.8.0)
- pip

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset (Optional — already included)
```bash
python data/generate_dataset.py
```

### 3. Train Model (Optional — already included)
```bash
python train_model.py
```

### 4. Run the Server

From the repository root (activate your environment first):

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

On Windows, `./start-local.ps1` uses `.venv` or the existing sibling
`luntiai-test-env` and starts the same local demo. Copy `.env.example` to `.env`
only when configuring optional settings; never commit `.env`.

### 5. Open the App
- **Frontend:** http://localhost:8000/app
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Project Structure

### CS 24/L XAI study

The executed notebook is [`notebooks/LuntiAI_ML_and_XAI.ipynb`](notebooks/LuntiAI_ML_and_XAI.ipynb).
It retrains the existing Random Forest, compares a majority baseline and a shallow
decision tree, verifies parity with the saved model, and evaluates local and global
explanations. Run it with Python 3.11:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-notebook.txt
python -m ipykernel install --user --name luntiai-xai --display-name "Python (LuntiAI XAI)"
```

Open the notebook in a notebook editor, select **Python (LuntiAI XAI)**, and Run All.
Results and figures are written to `reports/xai/`. Model files are not overwritten.
The notebook uses the same `api/xai.py` helper as the application.

The app now shows all eight signed TreeSHAP contributions, the baseline and output
probability, and a decomposition of the score gap against the runner-up. Explanations
remain visible for free and quota-limited accounts. Missing or older explanations
receive an explicit message. The frontend uses the backend's origin, so the documented
port 8000 works without editing JavaScript.

TreeSHAP is **model-specific, post-hoc feature attribution** for numerical tabular
inputs. Local explanations are class-specific; the notebook aggregates 120
class-balanced held-out cases for a global diagnostic. Model-agnostic KernelSHAP
is a notebook comparison, not a deployed endpoint. The experimental interventional
TreeSHAP comparison in the pinned environment fails the stated numerical tolerance
and is explicitly excluded from application use. Deployed path-dependent TreeSHAP
and KernelSHAP have separate required reconstruction checks.

The data are synthetic. Model probabilities and SHAP values do not establish
farm success, causal effects, fertilizer needs, or validated profitability.
Run the regression checks from the repository root with `python -m pytest tests -q`.

### Existing application files

```
crop-random-forest-model/
├── api/
│   ├── main.py              # FastAPI backend server
│   ├── barangay_data.py      # 23 Tagum barangay soil profiles
│   └── weather_service.py    # OpenWeatherMap + monthly presets
├── data/
│   ├── generate_dataset.py   # Dataset generation script
│   ├── philippine_crop_dataset.csv  # 120,000-row training data
│   └── sources.md            # Data source citations
├── frontend/
│   ├── index.html            # Premium dark-mode UI
│   ├── styles.css            # Design system
│   ├── app.js                # Frontend logic
│   └── logo.png              # LuntiAI product logo
├── model/
│   ├── crop_model.pkl        # Trained Random Forest model
│   ├── label_encoder.pkl     # Label encoder
│   └── model_metadata.json   # Model performance metrics
├── pitch/
│   └── README.md             # Complete pitch materials
├── train_model.py            # Model training pipeline
├── requirements.txt          # Python dependencies
├── .env.example              # Safe environment-variable template
└── README.md                 # This file
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Rank crop classes and explain scores from eight numeric inputs |
| GET | `/barangays` | List all 23 barangay soil profiles |
| GET | `/weather/{name}` | Optional live temperature/humidity and labeled monthly rainfall preset |
| GET | `/health` | System health check |
| GET | `/docs` | Interactive Swagger documentation |

Account endpoints accept a non-sensitive `username`, display alias, and password.
The SQLite runtime database is generated locally and excluded from Git and Docker
build contexts.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| ML Model | scikit-learn Random Forest (200 trees) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML5 / CSS3 / Vanilla JS + Chart.js |
| Weather API | OpenWeatherMap (free tier) |
| Data provenance | Synthetic generator; broad agricultural references listed in data/sources.md |

---

## Model Performance

- **Synthetic held-out accuracy:** 85.62% (24,000 test rows; not field accuracy)
- **Top Features:** Potassium (K), Nitrogen (N), Rainfall, Organic Matter (OM)
- **Dataset:** 120,000 synthetic rows; 96,000 training and 24,000 test rows, 12 crops, 8 inputs
- **Methodology:** Clipped normal sampling from hand-coded crop profiles; source claims require independent validation

---

## Team

**LuntiAI Team** — University of Mindanao, Tagum City
Technopreneurship Course — Academic Festival 2026

---

## License

This project is for academic purposes. Source notes record the original agricultural
references; they do not establish a verified source for every numeric assumption.
No field validity or third-party dataset license is implied by those citations.

