import numpy as np
import pandas as pd


def detect_outliers(df, method="iqr", threshold=1.5):
    indicators = [
        "anc_coverage",
        "institutional_delivery",
        "immunization",
        "high_risk_cases",
    ]

    results = []

    for indicator in indicators:
        if indicator not in df.columns:
            continue

        values = df[indicator].dropna()

        if values.empty:
            continue

        mean_val = float(values.mean())
        std_val = float(values.std(ddof=1)) if len(values) > 1 else 0.0

        if method.lower() == "zscore":
            if std_val == 0 or np.isnan(std_val):
                continue

            z_scores = (df[indicator] - mean_val) / std_val
            mask = df[indicator].notna() & (z_scores.abs() > threshold)

            for _, row in df[mask].iterrows():
                val = row[indicator]
                z = (val - mean_val) / std_val
                diff_pct = (
                    ((val - mean_val) / mean_val * 100)
                    if mean_val != 0
                    else 0.0
                )

                results.append({
                    "type": "outlier",
                    "method": "zscore",
                    "district": row["district"],
                    "indicator": indicator,
                    "month": str(row["month"])[:7],
                    "value": val,
                    "baseline_mean": round(mean_val, 2),
                    "std": round(std_val, 2),
                    "z_score": round(z, 2),
                    "change_pct": round(diff_pct, 2),
                    "direction": "High" if z > 0 else "Low",
                })

        else:  # IQR method (default)
            q1 = float(values.quantile(0.25))
            q3 = float(values.quantile(0.75))
            iqr = q3 - q1

            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr

            mask = (
                df[indicator].notna()
                & (
                    (df[indicator] < lower_bound)
                    | (df[indicator] > upper_bound)
                )
            )

            for _, row in df[mask].iterrows():
                val = row[indicator]
                diff_pct = (
                    ((val - mean_val) / mean_val * 100)
                    if mean_val != 0
                    else 0.0
                )
                z = ((val - mean_val) / std_val) if std_val > 0 else 0.0

                results.append({
                    "type": "outlier",
                    "method": "iqr",
                    "district": row["district"],
                    "indicator": indicator,
                    "month": str(row["month"])[:7],
                    "value": val,
                    "baseline_mean": round(mean_val, 2),
                    "lower_bound": round(lower_bound, 2),
                    "upper_bound": round(upper_bound, 2),
                    "z_score": round(z, 2),
                    "change_pct": round(diff_pct, 2),
                    "direction": (
                        "High" if val > upper_bound else "Low"
                    ),
                })

    return pd.DataFrame(results)

