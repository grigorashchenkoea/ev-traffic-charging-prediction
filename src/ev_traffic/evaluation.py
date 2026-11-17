"""Evaluation utilities for next-road prediction."""

import numpy as np
import pandas as pd


def normalize_candidate_scores(
    candidates: pd.DataFrame,
    scores: np.ndarray,
) -> pd.DataFrame:
    """Normalize candidate scores into probabilities per movement."""

    if len(candidates) != len(scores):
        raise ValueError("Candidate and score counts must match.")

    result = candidates[
        ["movement_id", "chosen"]
    ].copy()

    result["raw_score"] = scores

    result["score_total"] = (
        result.groupby("movement_id")["raw_score"]
        .transform("sum")
    )

    result["candidate_count"] = (
        result.groupby("movement_id")["raw_score"]
        .transform("size")
    )

    result["probability"] = np.where(
        result["score_total"] > 0,
        result["raw_score"]
        / result["score_total"].replace(0, 1),
        1.0 / result["candidate_count"],
    )

    probability_sums = (
        result.groupby("movement_id")["probability"].sum()
    )

    if not np.allclose(probability_sums, 1.0):
        raise ValueError(
            "Candidate probabilities do not sum to 1."
        )

    return result


def calculate_log_loss(
    evaluation: pd.DataFrame,
) -> float:
    """Calculate mean negative log probability of chosen roads."""

    actual_probabilities = evaluation.loc[
        evaluation["chosen"] == 1,
        "probability",
    ].clip(lower=1e-15)

    return float(-np.log(actual_probabilities).mean())

def bootstrap_trip_improvement(
    test_loss_data: pd.DataFrame,
    n_bootstrap: int = 1000,
    random_state: int = 42,
) -> tuple[float, float]:
    """Calculate a trip-level bootstrap CI for relative log-loss improvement."""

    trip_losses = (
        test_loss_data
        .groupby(["VehicleID", "TripID"])
        .agg(
            baseline_sum=("baseline_loss", "sum"),
            model_sum=("model_loss", "sum"),
            n=("movement_id", "count"),
        )
    )

    values = trip_losses[
        ["baseline_sum", "model_sum", "n"]
    ].to_numpy()

    rng = np.random.default_rng(random_state)
    bootstrap_improvements = []

    for _ in range(n_bootstrap):
        indices = rng.integers(
            0,
            len(values),
            size=len(values),
        )
        sampled = values[indices]

        baseline = sampled[:, 0].sum() / sampled[:, 2].sum()
        model = sampled[:, 1].sum() / sampled[:, 2].sum()

        bootstrap_improvements.append(
            (baseline - model) / baseline * 100
        )

    lower, upper = np.percentile(
        bootstrap_improvements,
        [2.5, 97.5],
    )

    return float(lower), float(upper)