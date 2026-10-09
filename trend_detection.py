
import pandas as pd


def detect_trends(df, threshold=10):
    indicators = [
        "anc_coverage",
        "institutional_delivery",
        "immunization",
        "high_risk_cases",
    ]

    results = []

    # Sort data by district and month
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])

    df = df.sort_values(["district", "month"])

    for indicator in indicators:

        # Compare each month with the previous month
        df["previous"] = df.groupby("district")[indicator].shift(1)

        df["change_pct"] = (
            (df[indicator] - df["previous"])
            / df["previous"].replace(0, float("nan"))
        ) * 100

        # Select significant changes
        significant = df[
            df["change_pct"].abs() >= threshold
        ]

        for _, row in significant.iterrows():

            results.append({
                "type": "Trend",
                "district": row["district"],
                "indicator": indicator,
                "month": row["month"].strftime("%Y-%m"),
                "previous_value": row["previous"],
                "current_value": row[indicator],
                "change_pct": round(row["change_pct"], 2),
                "direction": (
                    "Increase"
                    if row["change_pct"] > 0
                    else "Decrease"
                ),
            })

    return pd.DataFrame(results)
