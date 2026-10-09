import json
import pandas as pd


def generate_insights(trends, outliers, correlations):
    insights = []
    insight_counter = 1

    # Part B: Convert trends into insights
    if trends is not None and not trends.empty:
        for _, row in trends.iterrows():
            change = float(row["change_pct"])
            direction = row["direction"]
            curr_val = row["current_value"]
            prev_val = row["previous_value"]

            severity = (
                "High" if abs(change) >= 20
                else "Medium" if abs(change) >= 10
                else "Low"
            )

            explanation = (
                f"{row['indicator']} in {row['district']} "
                f"{direction.lower()}d by {abs(change):.1f}% "
                f"in {row['month']}, compared with the "
                f"previous observation ({prev_val})."
            )

            insights.append({
                "insight_id": f"INS-{insight_counter:04d}",
                "type": "trend",
                "indicator": row["indicator"],
                "entity": row["district"],
                "period": row["month"],
                "value": curr_val,
                "prev_value": prev_val,
                "change_pct": round(change, 1),
                "severity": severity,
                "explanation": explanation,
            })
            insight_counter += 1

    # Part C: Convert outliers into insights
    if outliers is not None and not outliers.empty:
        for _, row in outliers.iterrows():
            direction = row["direction"]
            val = row["value"]
            mean_val = row.get("baseline_mean", "n/a")
            z_score = row.get("z_score", 0.0)
            change_pct = row.get("change_pct", "n/a")

            # Outlier severity: High if extreme (z >= 2.5 or change >= 30%), else Medium
            severity = (
                "High" if (abs(z_score) >= 2.5 or (isinstance(change_pct, (int, float)) and abs(change_pct) >= 30))
                else "Medium"
            )

            if mean_val != "n/a":
                explanation = (
                    f"{row['indicator']} in {row['district']} "
                    f"was unusually {direction.lower()} at {val} "
                    f"during {row['month']} vs state mean of {mean_val}."
                )
            else:
                explanation = (
                    f"{row['indicator']} in {row['district']} "
                    f"was unusually {direction.lower()} at {val} "
                    f"during {row['month']}."
                )

            insights.append({
                "insight_id": f"INS-{insight_counter:04d}",
                "type": "outlier",
                "indicator": row["indicator"],
                "entity": row["district"],
                "period": row["month"],
                "value": val,
                "prev_value": mean_val if mean_val != "n/a" else "n/a",
                "change_pct": round(change_pct, 1) if isinstance(change_pct, (int, float)) else "n/a",
                "severity": severity,
                "explanation": explanation,
            })
            insight_counter += 1

    # Part D: Convert correlations into insights
    if correlations is not None and not correlations.empty:
        for _, row in correlations.iterrows():
            corr = float(row["correlation"])
            direction = row["direction"]
            pair_name = f"{row['indicator_1']}:{row['indicator_2']}"

            severity = (
                "High" if abs(corr) >= 0.90
                else "Medium"
            )

            explanation = (
                f"{row['indicator_1']} and {row['indicator_2']} "
                f"have a strong {direction.lower()} Pearson correlation "
                f"of {corr:.2f}."
            )

            insights.append({
                "insight_id": f"INS-{insight_counter:04d}",
                "type": "correlation",
                "indicator": pair_name,
                "entity": "All districts",
                "period": "Dataset-wide",
                "value": f"r={corr:.2f}",
                "prev_value": "n/a",
                "change_pct": "n/a",
                "severity": severity,
                "explanation": explanation,
            })
            insight_counter += 1

    columns = [
        "insight_id",
        "type",
        "indicator",
        "entity",
        "period",
        "value",
        "prev_value",
        "change_pct",
        "severity",
        "explanation",
    ]

    return pd.DataFrame(insights, columns=columns if insights else columns)


def export_insights(insights):
    # Export to CSV
    insights.to_csv("generated_insights.csv", index=False)

    # Export to JSON
    records = insights.to_dict(orient="records")

    with open("generated_insights.json", "w") as file:
        json.dump(records, file, indent=4, default=str)

    print("\nInsights exported successfully.")
    print("CSV: generated_insights.csv")
    print("JSON: generated_insights.json")

