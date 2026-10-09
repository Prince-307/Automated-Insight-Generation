import pandas as pd


def detect_correlations(df, threshold=0.70):
    indicators = [
        "anc_coverage",
        "institutional_delivery",
        "immunization",
        "high_risk_cases",
    ]

    # Calculate Pearson correlation matrix
    corr_matrix = df[indicators].corr(method="pearson")

    results = []

    # Examine each unique pair only once
    for i in range(len(indicators)):
        for j in range(i + 1, len(indicators)):
            indicator1 = indicators[i]
            indicator2 = indicators[j]

            correlation = corr_matrix.loc[
                indicator1, indicator2
            ]

            # Skip undefined correlations
            if pd.isna(correlation):
                continue

            if abs(correlation) >= threshold:
                results.append({
                    "type": "Correlation",
                    "indicator_1": indicator1,
                    "indicator_2": indicator2,
                    "correlation": round(correlation, 3),
                    "direction": (
                        "Positive"
                        if correlation > 0
                        else "Negative"
                    ),
                })

    return corr_matrix, pd.DataFrame(results)
