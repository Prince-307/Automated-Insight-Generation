# Automated Insight Generation — AI/ML Analytics Engine

An automated analytics engine built with Python and Streamlit that ingests district-level healthcare performance CSV datasets and automatically identifies **trends**, **outliers**, and **correlations**, producing human-readable, structured insights.

---

## 🚀 Features

- **Data Ingestion & Validation:** Validates required schema, parses time-series dates, casts indicators to numeric types, and checks for missing values.
- **Trend Detection:** Computes month-over-month percentage change per district and indicator `(current - previous) / previous * 100` and flags changes exceeding the configurable threshold (default: $\pm 10\%$).
- **Outlier Detection:** 
  - **IQR Method (Default):** Flags values outside $[Q_1 - 1.5 \times \text{IQR},\, Q_3 + 1.5 \times \text{IQR}]$.
  - **Z-Score Method:** Flags observations exceeding $Z$-threshold (default: $|z| > 3.0$).
- **Correlation Analysis:** Computes Pearson correlation across indicators, identifying strong positive and negative relationships ($|r| \ge 0.70$).
- **Dynamic Structured Insights:** Generates standardized outputs with `insight_id` (`INS-0001`), `type`, `indicator`, `entity`, `period`, `value`, `prev_value`, `change_pct`, `severity` (`High`, `Medium`, `Low`), and auto-generated natural language explanations.
- **Interactive Streamlit UI:** Includes live district/month filters, threshold sliders, per-district time-series charts, severity distribution bar chart, Pearson heatmap, and CSV/JSON downloads.

---

## 📦 Installation & Setup

1. **Clone or Navigate to the Repository:**
   ```bash
   cd "Automated Insight Generation"
   ```

2. **Install Dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

---

## 🖥️ Running the Application

### 1. Launch the Streamlit Web Dashboard
```bash
python3 -m streamlit run app.py
```
Open your browser at `http://localhost:8501` and upload the sample CSV located at `data/original_assignment_sample.csv`.

### 2. Run Standalone CLI Tests
```bash
python3 test_loader.py       # Validates data ingestion
python3 test_trends.py       # Tests month-over-month trend detection
python3 test_outliers.py     # Tests IQR & Z-score outlier detection
python3 test_correlation.py  # Tests Pearson correlation matrix
python3 test_insights.py     # Generates and exports insights to CSV & JSON
```

---

## 📊 Output Schema (CSV & JSON)

Generated insights follow the required 10-field specification:

| Field | Description | Example |
|---|---|---|
| `insight_id` | Auto-numbered unique identifier | `INS-0001` |
| `type` | Insight category (`trend`, `outlier`, `correlation`) | `trend` |
| `indicator` | Healthcare metric or metric pair | `anc_coverage` |
| `entity` | District name or `All districts` | `Ahmedabad` |
| `period` | Month or period span | `2026-08` |
| `value` | Observed current value / correlation ($r$) | `69` |
| `prev_value` | Baseline or previous period value | `85.0` |
| `change_pct` | Relative change percentage | `-18.8` |
| `severity` | Impact level (`High`, `Medium`, `Low`) | `High` |
| `explanation` | Natural language summary | `"anc_coverage in Ahmedabad decreased by 18.8% in 2026-08, compared with the previous observation (85.0)."` |

---

## ⚠️ Note on Sample Size & Correlation Instability

> **Statistical Limitation Notice:**
> The sample dataset contains 12 observations ($2\text{ months} \times 6\text{ districts}$). While Pearson correlations are computed and visualized honestly according to assignment rules, correlation coefficients derived from small sample sizes ($N < 10$) are statistically sensitive to individual outliers. For stable real-world deployment, $\ge 10\text{ districts}$ and $\ge 3\text{ months}$ are recommended.
