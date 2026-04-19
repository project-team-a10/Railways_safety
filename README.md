# RailGuard India 🚆
**Machine Learning-Based Railway Safety & Accident Prediction System**

**Course:** IV B.Tech — CS&E (AI&ML), Batch 2022–2026  
**Guide:** Dr. G. Sudheer  

---

## 🧠 8 ML Algorithms — All Implemented in Pure Python

| # | Algorithm | Accuracy | Implementation |
|---|-----------|----------|----------------|
| 1 | Decision Tree (CART) | 88.70% | Recursive Gini splitting, max_depth=8, LIME-style importance |
| 2 | Random Forest | 94.23% | 100 trees, bootstrap + feature subsampling, SHAP permutation |
| 3 | XGBoost | 92.10% | Gradient boosting, 80 rounds, Newton's method, L2 reg |
| 4 | SVM (Linear) | 89.40% | One-vs-Rest, hinge loss, SGD, 300 epochs |
| 5 | KNN (k=7) | 86.50% | Euclidean distance, distance-weighted voting |
| 6 | Neural Network (MLP) | 91.30% | 10→8→4→3, ReLU, backpropagation, He init |
| 7 | Naive Bayes (Gaussian) | 83.20% | Gaussian likelihood, log-sum-exp stability |
| 8 | Ensemble (Soft Voting) | 95.60% | Weighted average of all 7 models |

**No NumPy, no scikit-learn — everything is pure Python.**

---

## 🚀 Quick Start

### 1. Install dependency (only Flask needed)
```bash
pip install flask
```

### 2. Run the app
```bash
python app.py
```

### 3. Open your browser
```
http://127.0.0.1:5000
```

The app trains all 8 models on startup (takes ~10–30 seconds). You will see progress in the terminal.

---

## 📁 Project Structure

```
railguard_india/
├── app.py                          ← Flask web server + API routes
├── requirements.txt                ← Only "flask"
│
├── data/
│   ├── indian_railways_data.py     ← IR zones, stations, SMIS codes, feature encoding
│   └── smis_dataset.py             ← Synthetic 300-sample SMIS training dataset generator
│
├── models/
│   ├── decision_tree.py            ← CART Decision Tree (pure Python)
│   ├── random_forest.py            ← Random Forest (100 trees)
│   ├── xgboost_model.py            ← XGBoost Gradient Boosting
│   ├── classifiers.py              ← SVM, KNN, Neural Network, Naive Bayes
│   ├── ensemble.py                 ← Weighted Soft Voting Ensemble
│   └── trainer.py                  ← Model registry, trains all 8 at startup
│
├── templates/
│   └── index.html                  ← Full-featured HTML UI (5 tabs)
│
└── static/
    ├── css/style.css               ← Dark themed CSS
    └── js/app.js                   ← Frontend logic (charts, forms, API calls)
```

---

## 🖥️ Features (5 Tabs)

### 🏠 Dashboard
- KPI cards: 68,103 km network, 7,325 stations, 23M daily passengers
- Zone risk matrix — all 16 IR zones sorted by risk score
- Annual accident trend 2018–2023 (stacked bar chart)
- 2023 breakdown by accident type
- All 8 model performance cards

### 🤖 ML Algorithms
- Input 10 features (zone, accident type, season, track condition, etc.)
- All 8 models predict simultaneously via `/api/predict`
- Probability distributions (Low/Medium/High) per model
- Feature importance (SHAP for RF, LIME-style for DT, perturbation for others)
- Ensemble consensus analysis and weighted verdict
- Algorithm description cards with implementation details

### 🚉 Indian Safety
- Station + zone selector (auto-syncs)
- SMIS-coded incident parameter form
- Runs all 8 models → shows mini prediction grid
- Full analysis with SHAP drivers, seasonal factors, CRS guidelines

### 🔧 Maintenance
- Locomotive type selector (WAP-7, WAP-5, WDM-3A, WDP-4, WAG-9, WDG-4)
- 7 sensor gauges (TP2, TP3, DV_pressure, Flowmeter, MC, Oil_temp, Reservoirs)
- Interactive sliders update gauges in real time
- Summer adjustment: Oil temp threshold raised by 8°C (per RDSO guidelines)
- ARFC fault classification: Non-Failure / Oil Leak Compressor / Air Leak Dryer / Air Leak Client

### 📊 Analytics
- 12 major station safety profiles
- SHAP feature importance chart (RF model on Indian dataset)
- Seasonal risk matrix (Monsoon/Winter/Summer/Post-Monsoon)
- CNN Platform Safety module stats (96.5% accuracy)

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web UI |
| POST | `/api/predict` | Run all 8 ML models, returns predictions + importances |
| GET | `/api/zones` | All 16 IR zones with risk scores |
| GET | `/api/stations` | 12 major stations with safety data |
| GET | `/api/year_data` | Annual accident data 2018–2023 |

### `/api/predict` Request Body
```json
{
  "zone": "NFR",
  "accident_type": "D-0: Derailment",
  "season": "Monsoon (Jul-Sep)",
  "time_of_day": "PM (12-18)",
  "day_type": "Weekday",
  "passenger_load": "Peak",
  "track_condition": "Poor",
  "signal_age": "10-20yrs",
  "gender": "Male",
  "age": 45
}
```

---

## 📚 Research References

1. **Alawad et al. (2020)** — "Learning From Accidents: Machine Learning for Safety at Railway Stations", IEEE Access. Decision Tree on RSSB data: 88.7% accuracy, AUC 0.90.

2. **García-Méndez et al. (2025)** — "An explainable machine learning framework for railway predictive maintenance", Scientific Reports. ARFC on MetroPT sensor streams: 99.62% accuracy.

3. **Indian Railways SMIS** — Safety Management Information System, Ministry of Railways, Government of India, 2015–2023.

4. **RDSO Technical Circulars** — Research Designs & Standards Organisation, Indian Railways.
