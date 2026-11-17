
"""Feature engineering for road-choice prediction."""

import numpy as np
import pandas as pd


TURN_KEYS = ["incoming", "intersection", "outgoing"]
APPROACH_KEYS = ["incoming", "intersection"]

HISTORICAL_FEATURES = [
    "historical_count",
    "historical_total",
    "historical_probability",
    "K",
]


def build_candidates(
    movements: pd.DataFrame,
    turn_options: pd.DataFrame,
    reference_baseline: pd.DataFrame,
) -> pd.DataFrame:
    """Expand observed movements into candidate outgoing roads."""

    # Assign a unique ID to each observed movement.
    base = (
        movements[APPROACH_KEYS + ["outgoing", "hour"]]
        .rename(columns={"outgoing": "actual_outgoing"})
        .reset_index(drop=True)
    )

    base["movement_id"] = np.arange(len(base), dtype=np.int32)

    # Generate all possible outgoing choices.
    candidates = base.merge(
        turn_options,
        on=APPROACH_KEYS,
        how="left",
        validate="many_to_many",
    )

    # Label the observed outgoing choice.
    candidates["chosen"] = (
        candidates["outgoing"] == candidates["actual_outgoing"]
    ).astype(np.int8)

    # Attach reference-based historical features.
    candidates = candidates.merge(
        reference_baseline[TURN_KEYS + HISTORICAL_FEATURES],
        on=TURN_KEYS,
        how="left",
        validate="many_to_one",
    )

    # Check that every movement has exactly one correct choice.
    chosen_counts = candidates.groupby("movement_id")["chosen"].sum()

    if (
        len(chosen_counts) != len(base)
        or not chosen_counts.eq(1).all()
    ):
        raise ValueError(
            "Each movement must have exactly one chosen candidate."
        )

    if candidates[HISTORICAL_FEATURES].isna().any().any():
        raise ValueError("Missing historical features detected.")

    return candidates

HOURLY_FEATURES = [
    "hourly_count",
    "hourly_total",
    "hourly_probability",
    "adaptive_probability",
]


def attach_hourly_features(
    candidates: pd.DataFrame,
    reference_hourly: pd.DataFrame,
) -> pd.DataFrame:
    """Attach reference-based hourly turning features to candidates."""

    result = candidates.merge(
        reference_hourly[
            TURN_KEYS + ["hour"] + HOURLY_FEATURES
        ],
        on=TURN_KEYS + ["hour"],
        how="left",
        validate="many_to_one",
    )

    for col in HOURLY_FEATURES:
        result[col] = result[col].astype("float32")

    if result[HOURLY_FEATURES].isna().any().any():
        raise ValueError("Missing hourly features detected.")

    return result

def build_trajectory_history(
    movements: pd.DataFrame,
) -> pd.DataFrame:
    """Add previous-road features within chronologically ordered trips."""

    result = movements.copy()

    trip_groups = result.groupby(
        ["VehicleID", "TripID"],
        sort=False,
    )

    result["previous_road_1"] = (
        trip_groups["incoming"].shift(1)
    )

    result["previous_road_2"] = (
        trip_groups["incoming"].shift(2)
    )

    result["trip_position"] = trip_groups.cumcount()

    result[["previous_road_1", "previous_road_2"]] = (
        result[["previous_road_1", "previous_road_2"]]
        .fillna(-1)
        .astype("int32")
    )

    return result

HISTORY_FEATURES = [
    "previous_road_1",
    "previous_road_2",
    "trip_position",
]


def attach_history_features(
    candidates: pd.DataFrame,
    movement_history: pd.DataFrame,
) -> pd.DataFrame:
    """Attach trajectory-history features to candidate-level data."""

    result = candidates.merge(
        movement_history[
            ["movement_id"] + HISTORY_FEATURES
        ],
        on="movement_id",
        how="left",
        validate="many_to_one",
    )

    for col in HISTORY_FEATURES:
        result[col] = result[col].astype("int32")

    if result[HISTORY_FEATURES].isna().any().any():
        raise ValueError("Missing trajectory-history features detected.")

    return result