"""LightGBM training for next-road prediction."""

import lightgbm as lgb
import pandas as pd


MODEL_FEATURES = [
    "incoming",
    "intersection",
    "outgoing",
    "hour",
    "historical_probability",
    "historical_count",
    "historical_total",
    "K",
    "hourly_count",
    "hourly_total",
    "hourly_probability",
    "adaptive_probability",
    "previous_road_1",
    "previous_road_2",
]

CATEGORICAL_FEATURES = [
    "incoming",
    "intersection",
    "outgoing",
    "previous_road_1",
    "previous_road_2",
]


def train_lightgbm(
    train_candidates: pd.DataFrame,
) -> lgb.LGBMClassifier:
    """Train the final candidate-level road-choice model."""

    model = lgb.LGBMClassifier(
        objective="binary",
        num_leaves=31,
        learning_rate=0.1,
        n_estimators=200,
        verbosity=-1,
        n_jobs=-1,
        random_state=42,
    )

    model.fit(
        train_candidates[MODEL_FEATURES],
        train_candidates["chosen"],
        categorical_feature=CATEGORICAL_FEATURES,
    )

    return model