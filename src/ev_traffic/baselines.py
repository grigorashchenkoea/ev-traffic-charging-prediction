
"""Historical turning-probability baselines."""

import pandas as pd


TURN_KEYS = ["incoming", "intersection", "outgoing"]
APPROACH_KEYS = ["incoming", "intersection"]


def build_reference_baseline(
    reference_movements: pd.DataFrame,
    turn_options: pd.DataFrame,
    alpha: float = 1.0,
) -> pd.DataFrame:
    """Calculate Laplace-smoothed static turning probabilities."""

    if alpha <= 0:
        raise ValueError("alpha must be positive")

    counts = (
        reference_movements.groupby(TURN_KEYS)
        .size()
        .rename("historical_count")
        .reset_index()
    )

    baseline = turn_options.merge(
        counts,
        on=TURN_KEYS,
        how="left",
        validate="one_to_one",
    )

    baseline["historical_count"] = (
        baseline["historical_count"].fillna(0)
    )

    baseline["K"] = (
        baseline.groupby(APPROACH_KEYS)["outgoing"]
        .transform("size")
    )

    baseline["historical_total"] = (
        baseline.groupby(APPROACH_KEYS)["historical_count"]
        .transform("sum")
    )

    baseline["historical_probability"] = (
        (baseline["historical_count"] + alpha)
        / (baseline["historical_total"] + alpha * baseline["K"])
    )

    return baseline


def build_reference_hourly(
    reference_movements: pd.DataFrame,
    reference_baseline: pd.DataFrame,
    hours,
    alpha: float = 1.0,
    lambda_value: float = 100.0,
) -> pd.DataFrame:
    """Calculate hourly and adaptive turning probabilities."""

    if alpha <= 0 or lambda_value <= 0:
        raise ValueError("Smoothing parameters must be positive")

    hourly_counts = (
        reference_movements
        .groupby(TURN_KEYS + ["hour"])
        .size()
        .rename("hourly_count")
        .reset_index()
    )

    hourly = (
        reference_baseline[
            TURN_KEYS + ["historical_probability", "K"]
        ]
        .merge(
            pd.DataFrame({"hour": sorted(set(hours))}),
            how="cross",
        )
    )

    hourly = hourly.merge(
        hourly_counts,
        on=TURN_KEYS + ["hour"],
        how="left",
        validate="one_to_one",
    )

    hourly["hourly_count"] = hourly["hourly_count"].fillna(0)

    hourly["hourly_total"] = (
        hourly.groupby(APPROACH_KEYS + ["hour"])["hourly_count"]
        .transform("sum")
    )

    hourly["hourly_probability"] = (
        (hourly["hourly_count"] + alpha)
        / (hourly["hourly_total"] + alpha * hourly["K"])
    )

    hourly["adaptive_probability"] = (
        hourly["hourly_count"]
        + lambda_value * hourly["historical_probability"]
    ) / (hourly["hourly_total"] + lambda_value)

    return hourly
